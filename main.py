import os
import sys

# Proje ana dizinini ve 'src' dizinini Python yoluna ekle
PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJE_DIZINI)
sys.path.insert(0, os.path.join(PROJE_DIZINI, "src"))

try:
    from db_yoneticisi import MSSQLYoneticisi
except ModuleNotFoundError:
    from src.db_yoneticisi import MSSQLYoneticisi

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_KLASORU = "dokumanlar"


def departman_belirle(dosya_adi: str) -> str:
    isim = dosya_adi.lower()

    # 1. Öncelikli Özel İSG ve Finans Kuralları
    if any(k in isim for k in ["radyasyon", "kbrn", "tehlikeli_madde", "cevre_ajansi", "isg", "is_sagligi"]):
        return "İSG"

    if any(k in isim for k in ["issizlik_sigortasi_fonu", "butce", "muhasebe", "finans", "gelir_vergisi"]):
        return "Finans"

    # 2. İnsan Kaynakları (HR) Kuralları
    if any(k in isim for k in [
        "sendikalar", "toplu_is", "kadin", "gece_postasi", "kidem", "isci_alinmasi",
        "issizlik_sigortasi_kanunu", "is_kanunu", "calisma_sureleri", "hr", "ik",
        "asgari_ucret", "emeklilik", "analik", "tuseb", "ulusal_ajansi", "ucret_prim",
        "uluslararasi_isgucu", "uzaktan_calisma", "yillik_ucretli_izin"
    ]):
        return "HR"

    # 3. Hukuk Kuralları
    if any(k in isim for k in [
        "nukleer_duzenleme", "sigortacilik", "sosyal_hizmetler", "telgraf", "anayasa",
        "hukuk", "mahkeme", "teftis", "deik", "dijital_mecra", "yonetmeligi", "mke",
        "kanun", "turk_standartlari", "insan_haklari"
    ]):
        return "Hukuk"

    # 4. Diğer Kurumsal Departmanlar
    if "bt" in isim: return "BT"
    if "uretim" in isim or "bakim" in isim: return "Üretim"
    if "planlama" in isim: return "Planlama"
    if "satin" in isim: return "Satın Alma"
    if "ambar" in isim or "depo" in isim: return "Ambar"

    return "Genel"


def main():
    print("=========================================================")
    print(" MSSQL VERİ TABANINA DOKÜMAN YÜKLEME BAŞLADI...")
    print("=========================================================")

    if not os.path.exists(PDF_KLASORU):
        print(f" Hata: '{PDF_KLASORU}' klasörü bulunamadı!")
        return

    db_yonetici = MSSQLYoneticisi()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60,
        length_function=len
    )

    pdf_bulundu = False
    toplam_parca = 0

    for dosya in os.listdir(PDF_KLASORU):
        if dosya.endswith(".pdf"):
            pdf_bulundu = True
            dosya_yolu = os.path.join(PDF_KLASORU, dosya)
            departman = departman_belirle(dosya)

            print(f"\nİşleniyor: {dosya} -> Departman: {departman}")

            try:
                loader = PyPDFLoader(dosya_yolu)
                sayfalar = loader.load()

                parcalar = text_splitter.split_documents(sayfalar)
                for parca in parcalar:
                    parca.metadata["departman"] = departman


                # Yalnızca MSSQL'e kaydetme
                db_yonetici.dokuman_ve_parca_kaydet(dosya, departman, parcalar)
                toplam_parca += len(parcalar)

            except Exception as e:
                print(f" Hata ({dosya}): {e}")

    if not pdf_bulundu:
        print(" Hata: PDF dosyası bulunamadı!")
        return

    print("=========================================================")
    print(f" İŞLEM TAMAMLANDI: Toplam {toplam_parca} metin parçası MSSQL veritabanına kaydedildi!")
    print("=========================================================")


if __name__ == "__main__":
    main()