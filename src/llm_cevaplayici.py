import re
import time
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from src.cevaplayici import KurumsalCevaplayici
from src.db_yoneticisi import MSSQLYoneticisi


class LlamaCevaplayici:
    def __init__(self):
        self.llm = Ollama(model="llama3", temperature=0.15)
        self.arama_motoru = KurumsalCevaplayici()
        self.db_yonetici = MSSQLYoneticisi()

        self.prompt_template = PromptTemplate(
            input_variables=["soru", "dokuman"],
            template="""Sen Kordsa şirketinin kurumsal yapay zeka asistanısın. Görevin, aşağıda verilen doküman parçasına dayanarak soruyu SADECE TÜRKÇE olarak yanıtlamaktır.

KRİTİK DİL KURALI: 
- YANITIN TAMAMI KESİNLİKLE TÜRKÇE OLMALIDIR. 
- İNGİLİZCE KELİME, CÜMLE VEYA AÇIKLAMA KULLANMAK KESİNLİKLE YASAKTIR.
- "According to the document", "You can reach", "You can contact" GİBİ İNGİLİZCE KALIPLAR ASLA KULLANILMAYACAKTIR.

DOKÜMAN PARÇASI:
{dokuman}

SORU:
{soru}

SİSTEM TALİMATLARI:
1. Yanıtı doğrudan Türkçe ver. "Merhaba", "Sorunuza istinaden", "Kullanıcının sorusunu cevaplamak için" gibi giriş cümleleri kullanma.
2. Dokümandaki bilgileri net ve anlaşılır bir Türkçe ile özetle.
3. Dokümanda kesinlikle bilgi yoksa sadece "İlgili kılavuzlarda bu konuyla ilgili detay bilgi yer almamaktadır." de.

TÜRKÇE CEVAP:"""
        )

    def cevap_uret(self, soru: str, departman_filtresi: str = None, gecmis_mesajlar: list = None) -> tuple:
        try:
            # 1. İletişim / Ulaşım İsteği Ön Kontrolü
            iletişim_anahtarlari = ["ulaşabilirim", "ulasabilirim", "ulaşırım", "ulasirim", "iletişim", "iletisim", "telefon", "mail", "numara", "eposta", "e-posta"]
            soru_lower = soru.lower()

            iletisim_bilgisi = ""
            if any(k in soru_lower for k in ["insan kaynakları", "ik", "hr", "iletisim", "iletişim"]) and any(k in soru_lower for k in iletişim_anahtarlari):
                iletisim_bilgisi = (
                    "\n\n**Kordsa İnsan Kaynakları & Genel İletişim Bilgileri:**\n"
                    "- **Telefon:** +90 (262) 316 10 00\n"
                    "- **E-Posta:** hr@kordsa.com / info@kordsa.com\n"
                    "- **İç İletişim & HR Portal:** [Kordsa HR Portal](https://hr.kordsa.com)"
                )

            # 2. MSSQL Arama Motoru
            ilgili_dokumanlar, skor = self.arama_motoru.mssql_dokuman_ara(soru, departman_filtresi)

            if not ilgili_dokumanlar and not iletisim_bilgisi:
                return "Veri tabanında bu konuyla ilgili eşleşen doküman bulunamadı.", [], 0.0

            dokuman_metni = "\n---\n".join([f"{d['metin']}" for d in ilgili_dokumanlar[:3]]) if ilgili_dokumanlar else "Genel İletişim Bilgileri"

            prompt = self.prompt_template.format(
                soru=soru,
                dokuman=dokuman_metni
            )

            cevap = self.llm.invoke(prompt)
            cevap_metni = cevap.strip()

            # Türkçe dışı açılış/meta ifadelerini temizleme
            cevap_metni = re.sub(r'^(Kullanıcının|Soru|Cevap|Merhaba|According to|In the document).*?:\s*',
            '', cevap_metni,
             flags=re.IGNORECASE
             ).strip()
            cevap_metni = re.sub(r'\(Note:.*?\)', '', cevap_metni, flags=re.DOTALL | re.IGNORECASE)
            cevap_metni = re.sub(r'\(Not:.*?\)', '', cevap_metni, flags=re.DOTALL | re.IGNORECASE)

            # Yanıt ile iletişim bilgisini birleştirme
            nihai_cevap = cevap_metni + iletisim_bilgisi

            return nihai_cevap.strip(), ilgili_dokumanlar, (skor if skor > 0 else 0.85)

        except Exception as e:
            print("LLM Cevap üretme hatası:", e)
            return "Yanıt hazırlanırken bir teknik aksaklık oluştu, lütfen tekrar dener misiniz?", [], 0.0