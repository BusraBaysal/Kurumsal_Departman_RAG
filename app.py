import os
import sys
import time
import streamlit as st

# Proje ana dizinini ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.yonlendirici import KolayRouter
from src.soru_kontrol import SoruKontrol
from src.llm_cevaplayici import LlamaCevaplayici
from src.db_yoneticisi import MSSQLYoneticisi

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Kordsa | Bilgi Yönetim Portalı",
    page_icon="https://cdn-icons-png.flaticon.com/512/8649/8649595.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GÜÇLENDİRİLMİŞ KURUMSAL CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: #0b1329;
        color: #e2e8f0;
    }

    .stChatMessage {
        background: #16223b !important;
        border: 1px solid #233554 !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
        padding: 16px !important;
    }

    /* STATS METRİK KARTLARI */
    .metric-card {
        background: #111d33;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .metric-title { font-size: 0.75rem; color: #94a3b8; font-weight: 500; }
    .metric-value { font-size: 1.15rem; color: #38bdf8; font-weight: 700; margin-top: 2px; }

    /* ETİKETLER */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #233554;
    }

    .info-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .badge-dept { background: #1e293b; color: #38bdf8; border: 1px solid #334155; }
    .badge-sub { background: #1e293b; color: #94a3b8; border: 1px solid #334155; }
    .badge-time { background: #1e293b; color: #cbd5e1; border: 1px solid #334155; }

    .badge-conf-high { background: #064e3b; color: #34d399; border: 1px solid #047857; }
    .badge-conf-mid { background: #78350f; color: #fbbf24; border: 1px solid #b45309; }
    .badge-conf-low { background: #7f1d1d; color: #f87171; border: 1px solid #b91c1c; }

    .portal-header {
        text-align: center;
        padding: 5px 0 15px 0;
    }
    .portal-title {
        color: #f8fafc;
        font-weight: 700;
        font-size: 2rem;
        letter-spacing: -0.5px;
    }
    .portal-subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 4px;
    }

    [data-testid="stSidebar"] {
        background-color: #070d19 !important;
        border-right: 1px solid #1e293b;
    }

    .sidebar-history-item {
        background: #111d33;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 6px;
        font-size: 0.85rem;
        color: #cbd5e1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
""", unsafe_allow_html=True)


# --- 3. RESOURCE / STATE BAŞLATMA ---
@st.cache_resource
def modulleri_yukle():
    db = MSSQLYoneticisi()
    r = KolayRouter()
    sk = SoruKontrol()
    llm = LlamaCevaplayici()
    return db, r, sk, llm


db_yonetici, router, soru_kontrol, cevaplayici = modulleri_yukle()

if "gecmis_konusmalar" not in st.session_state:
    st.session_state.gecmis_konusmalar = []

# --- 4. SIDEBAR (FİLTRELER VE GEÇMİŞ) ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=400&q=80",
             width="stretch")

    st.markdown(
        "<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight:600; margin-top:10px;'>Arama Filtreleri</h4>",
        unsafe_allow_html=True)

    # YENİLİK 1: Manuel Departman Seçim Seçeneği
    hedef_departman = st.selectbox(
        "Arama Modu / Departman:",
        ["Otomatik Routing",
         "İnsan Kaynakları",
         "İş Sağlığı ve Güvenliği",
         "IT / Bilişim Teknolojileri",
         "Üretim / Operasyon"]
    )

    st.markdown("---")
    st.markdown("<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight:600;'>Arama Geçmişi</h4>",
                unsafe_allow_html=True)

    if len(st.session_state.gecmis_konusmalar) > 0:
        for idx, chat in enumerate(reversed(st.session_state.gecmis_konusmalar)):
            st.markdown(f"<div class='sidebar-history-item'>{chat['soru']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Geçmişi Temizle", use_container_width=True):
            st.session_state.gecmis_konusmalar = []
            st.rerun()
    else:
        st.caption("Henüz yapılmış bir arama yok.")

# --- 5. ANA PORTAL BAŞLIĞI ---
st.markdown("""
    <div class='portal-header'>
        <div class='portal-title'>Kordsa Yapay Zeka Bilgi Merkezi</div>
        <div class='portal-subtitle'>Kurumsal Doküman Analiz ve Yanıt Asistanı</div>
    </div>
""", unsafe_allow_html=True)

# YENİLİK 2: Performans ve Analitik Metrik Kartları
toplam_sorgu = len(st.session_state.gecmis_konusmalar)
ort_skor = int(sum([c.get('guven_skoru', 0) for c in
                    st.session_state.gecmis_konusmalar]) / toplam_sorgu * 100) if toplam_sorgu > 0 else 0
ort_sure = round(sum([c.get('sure', 0) for c in st.session_state.gecmis_konusmalar]) / toplam_sorgu,2)\
    if toplam_sorgu > 0 else 0.0

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(
        f"<div class='metric-card'><div class='metric-title'>Toplam Sorgu</div><div class='metric-value'>{toplam_sorgu}</div></div>",
        unsafe_allow_html=True)
with col_m2:
    st.markdown(
        f"<div class='metric-card'><div class='metric-title'>Ort. Doğruluk Skoru</div><div class='metric-value'>%{ort_skor}</div></div>",
        unsafe_allow_html=True)
with col_m3:
    st.markdown(
        f"<div class='metric-card'><div class='metric-title'>Ort. Yanıt Süresi</div><div class='metric-value'>{ort_sure} sn</div></div>",
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. GEÇMİŞ MESAJLARI EKRANA BASMA ---
for idx, chat in enumerate(st.session_state.gecmis_konusmalar):
    with st.chat_message("user"):
        st.write(chat["soru"])

    with st.chat_message("assistant"):
        guven_yuzde = int(chat.get("guven_skoru", 0) * 100)
        if guven_yuzde >= 75:
            conf_class = "badge-conf-high"
        elif guven_yuzde >= 40:
            conf_class = "badge-conf-mid"
        else:
            conf_class = "badge-conf-low"

        st.markdown(f"""
            <div class='badge-container'>
                <span class='info-badge badge-dept'>Departman: {chat.get('dept', 'Genel')}</span>
                <span class='info-badge badge-sub'>Kategori: {chat.get('sub', 'Genel')}</span>
                <span class='info-badge {conf_class}'>Doğruluk Skoru: %{guven_yuzde}</span>
                <span class='info-badge badge-time'>Yanıt Süresi: {chat.get('sure', 0.0)} sn</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(chat["cevap"])

        # Referanslar (Tekilleştirme)
        if chat.get("kaynaklar"):
            with st.expander("Referans Dokümanlar ve Kılavuz Metni"):
                st.markdown("**Kaynak Dosyalar:**")

                gorulen_kaynaklar = set()
                tekil_kaynaklar = []
                for k in chat["kaynaklar"]:
                    dosya_adi = os.path.basename(k.get("dosya", "Doküman"))
                    sayfa_no = int(k.get('sayfa', 0)) + 1
                    dept_adi = k.get('dept', 'Genel')
                    anahtar = (dosya_adi, dept_adi, sayfa_no)

                    if anahtar not in gorulen_kaynaklar:
                        gorulen_kaynaklar.add(anahtar)
                        tekil_kaynaklar.append({
                            "dosya": dosya_adi,
                            "dept": dept_adi,
                            "sayfa": sayfa_no,
                            "metin": k.get("metin", "")
                        })

                for k in tekil_kaynaklar:
                    st.markdown(f"* `{k['dosya']}` | Departman: **{k['dept']}** | Sayfa: **{k['sayfa']}**")

                if tekil_kaynaklar:
                    st.markdown("---")
                    st.markdown("**Alıntılanan İlgili Parça:**")
                    st.caption(f"\"{tekil_kaynaklar[0]['metin'].strip()}\"")

        # YENİLİK 3 & 4: Geri Bildirim ve Dışa Aktar Butonları
        c_fb1, c_fb2, c_exp = st.columns([1, 1, 6])
        with c_fb1:
            if st.button("👍", key=f"like_{idx}"):
                if hasattr(db_yonetici, "geri_bildirim_kaydet"):
                    db_yonetici.geri_bildirim_kaydet(chat["soru"], chat["cevap"], 1)
                st.toast("Geri bildiriminiz kaydedildi, teşekkürler!", icon="✅")
        with c_fb2:
            if st.button("👎", key=f"dislike_{idx}"):
                if hasattr(db_yonetici, "geri_bildirim_kaydet"):
                    db_yonetici.geri_bildirim_kaydet(chat["soru"], chat["cevap"], -1)
                st.toast("Geri bildiriminiz alındı. Model geliştirilecek.", icon="⚠️")
        with c_exp:
            st.download_button(
                label="📄 Yanıtı İndir (.txt)",
                data=f"KORDSA BİLGİ MERKEZİ YANIT RAPORU\nSoru: {chat['soru']}\n\nYanıt:\n{chat['cevap']}\n\nDepartman: {chat.get('dept')}\nDoğruluk Skoru: %{guven_yuzde}",
                file_name=f"kordsa_yanit_{idx + 1}.txt",
                mime="text/plain",
                key=f"dl_{idx}"
            )

# --- 7. SOHBET GİRİŞ ALANI ---
user_input = st.chat_input("Kordsa prosedürleri ve süreçleri hakkında bir soru yazınız...")

if user_input:
    ham_soru = str(user_input).strip()

    with st.chat_message("user"):
        st.write(ham_soru)

    with st.chat_message("assistant"):
        baslangic_zamani = time.time()

        with st.status("Dokümanlar inceleniyor ve yanıt hazırlanıyor...", expanded=True) as status_box:
            col_txt, col_btn = st.columns([3, 1])
            with col_btn:
                durdur_butonu = st.button("🛑 İşlemi Durdur", key="stop_process_btn")

            if durdur_butonu:
                status_box.update(label="İşlem kullanıcı tarafından durduruldu.", state="error", expanded=False)
                st.warning("Yanıt üretimi durduruldu. Yeni bir soru girebilirsiniz.")
                st.stop()

            # Bağlam Oluşturma
            baglamli_soru = ham_soru
            if (st.session_state.gecmis_konusmalar
                    and len(ham_soru.split()) < 3
                    and not any(k in ham_soru.lower() for k in
                                ["izin", "vpn", "maaş", "maas", "baret", "ücret", "ucret", "saat", "gün"])):
                onceki_soru = st.session_state.gecmis_konusmalar[-1]["soru"]
                baglamli_soru = f"{onceki_soru} {ham_soru}"

            # Kurumsallık Kontrolü
            if not soru_kontrol.kurumsal_mi(baglamli_soru):
                status_box.update(label="Sorgu tamamlandı.", state="complete", expanded=False)
                cevap_text = ("Bu sistem yalnızca Kordsa kurumsal bilgi ve dokümanları kapsamında hizmet vermektedir. "
                              "Lütfen şirket süreçleri, prosedürleri veya departmanlarla ilgili bir soru yazınız.")

                sonuc = {
                    "soru": ham_soru,
                    "cevap": cevap_text,
                    "kaynaklar": [],
                    "guven_skoru": 0.0,
                    "dept": "Genel",
                    "sub": "Kurumsal Dışı Soru",
                    "sure": 0.1,
                    "timestamp": time.time()
                }
                st.session_state.gecmis_konusmalar.append(sonuc)
                st.rerun()

            # Departman Yönlendirmesi (Routing veya Manuel Seçim)
            if hedef_departman != "Otomatik Routing":
                tahmin_dept = hedef_departman
                tahmin_sub = "Manuel Seçim"
            else:
                try:
                    rota = router.rotayi_belirle(baglamli_soru)
                    tahmin_dept = rota.get("departman", "Genel")
                    tahmin_sub = rota.get("alt_baslik", "Genel")
                except Exception:
                    tahmin_dept, tahmin_sub = "Genel", "Genel"

            # LLM Yanıtı ve Referans Çekimi
            try:
                yapay_zeka_cevabi, kaynaklar, guven_skoru = cevaplayici.cevap_uret(
                    ham_soru,
                    tahmin_dept,
                    st.session_state.gecmis_konusmalar
                )
            except Exception as e:
                yapay_zeka_cevabi = f"Yanıt üretilirken bir hata oluştu: {e}"
                kaynaklar = []
                guven_skoru = 0.0

            status_box.update(label="Yanıt başarıyla oluşturuldu.", state="complete", expanded=False)

        bitis_zamani = time.time()
        gecen_sure = round(bitis_zamani - baslangic_zamani, 2)

        sonuc = {
            "soru": ham_soru,
            "cevap": yapay_zeka_cevabi,
            "kaynaklar": kaynaklar,
            "guven_skoru": guven_skoru,
            "dept": tahmin_dept,
            "sub": tahmin_sub,
            "sure": gecen_sure,
            "timestamp": time.time()
        }
        st.session_state.gecmis_konusmalar.append(sonuc)

        # MSSQL Veritabanına Loglama
        try:
            db_yonetici.log_kaydet(
                ham_soru,
                yapay_zeka_cevabi,
                tahmin_dept,
                tahmin_sub,
                guven_skoru,
                gecen_sure
            )
        except Exception as db_err:
            print(f"MSSQL Log Hatası: {db_err}")

        st.rerun()