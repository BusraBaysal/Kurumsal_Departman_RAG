import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

PDF_KLASORU = "dokumanlar"
if not os.path.exists(PDF_KLASORU):
    os.makedirs(PDF_KLASORU, exist_ok=True)

KORDSA_MEVZUATLAR = {
    "Hukuk_Kilavuz.pdf": (
        "Kordsa Hukuk Departmani - Sirket Sozlesmeleri, Uyum, Kişisel Veriler ve Mevzuat Yonergesi\n\n"
        "1. Adim (Ticari Sozlesmeler ve Hukuki Onay): Kordsa tarafindan ucuncu taraflarla akdedilecek tum ticari "
        "sozlesmeler, protokoller ve Gizlilik Taahhutnameleri (NDA) imza oncesinde Hukuk Departmaninin incelemesine ve "
        "onayina sunulur. Hukuk onayi alinmayan hicbir sozlesme sirketi baglayici sekilde imzalanamaz.\n\n"
        "2. Adim (KVKK ve Veri Gizliligi Uyum Proseduru): Sirket bunyesinde islenen tum kisisel veriler KVKK mevzuatina "
        "uygun olarak saklanir ve Islenir. Ucuncu taraflara veri aktariminda Hukuk birimince hazirlanan acik riza ve "
        "aydinlatma metinlerinin kullanilmasi zorunludur.\n\n"
        "3. Adim (Mevzuat Takibi ve Dava Surecleri): Sirketi ilgilendiren yasal degisiklikler, dava, icra ve ihtilaflar "
        "Hukuk Departmani tarafindan takip edilir. Resmi kurumlardan gelen adli tebligatlar derhal Hukuk birimine iletilir."
    ),
    "BT_Kilavuz.pdf": (
        "Kordsa BT Departmani - Siber Guvenlik, VPN, E-Posta, Parola ve Donanim Proseduru\n\n"
        "1. Adim (Donanim Uyumluluk ve Sertifikasyon): Kordsa bilgi sistemlerine, yerel sunuculara veya ERP (SAP) "
        "altyapisina sirket disindan erisim talep eden personelin kullanacagi bilgisayar veya mobil donanim, BT Altyapi "
        "Guvenlik ekipleri tarafindan uc nokta (Endpoint Security) taramasina tabi tutulur. Cihaz uzerinde lisansli ve guncel "
        "bir antivirus yaziliminin bulunmasi, isletim sisteminin guncel olmasi ve Kordsa Active Directory alan adi mimarisine "
        "entegre dijital sertifika barindirmasi zorunludur. Yetkisiz cihazlar kurumsal aga baglanamaz.\n\n"
        "2. Adim (Sifreli Tunel ve VPN Kullanimi): Tum dis baglantilar, ag katmaninda uctan uca sifrelenmis SSL-VPN veya IPsec VPN "
        "tunelleri uzerinden gerceklestirilir. VPN baglantisi kurmak isteyen personel, BT tarafindan tanimlanan VPN istemcisini "
        "acarak kurumsal kullanici adi ve sifresini girer. Statik veya dinamik IP kisitlamalari uyarinca sadece yetkilendirilmis "
        "cografi bolgelerden gelen baglantilar kabul edilir. Baglanti sorunlarinda BT Destek masasina talep acilmalidir. VPN sunuculari 7/24 izlenir.\n\n"
        "3. Adim (Cok Asamali Kimlik Dogrulama - MFA, Parola ve E-Posta): Kullanicilarin VPN veya kurumsal e-posta sistemine dahil olabilmesi "
        "icin MFA (Authenticator / TOTP) onayi zorunludur. Kurumsal e-posta ve portal parolalari en az 90 gunde bir yenilenmeli, "
        "parolalar en az 8 karakter, buyuk-kucuk harf, rakam ve ozel karakter icermelidir. Eski 3 parola tekrar kullanilamaz."
    ),
    "HR_Kilavuz.pdf": (
        "Kordsa HR Departmani - Servis, Yemekhane, Calisma Saatleri, Izin, Ucretlendirme ve Maas Yonetmeligi\n\n"
        "1. Adim (Personel Servis Hizmeti ve Ulasim Hakki): Kordsa, tum kadrolu ve stajyer personeline fabrika ve idari "
        "binalara ulasim icin ucretsiz personel servis hizmeti sunar. Servis imkanindan tum Kordsa calisanlari yararlanabilir. "
        "Servis guzergahlari, durak saatleri ve hat bilgileri Insan Kaynaklari Portali uzerinden duyurulur. Servis kalkis "
        "saatleri idari mesai ve vardiya degisim saatlerine gore duzenlenir.\n\n"
        "2. Adim (Calisma Saatleri, Yemekhane ve Sosyal Imkanlar): Idari personel icin standart mesai saatleri hafta ici 08:00 - 17:00 arasindadir. "
        "Fabrika yemekhanesinde ogle yemegi servisi 12:00 - 13:30 saatleri arasinda sunulur. Vardiyali personeller icin "
        "gece ve günduz yemek servisleri vardiya molalarina gore duzenlenir. Tum calisanlar yemekhane imkanindan ucretsiz faydalanir.\n\n"
        "3. Adim (Ucretlendirme, Maas, Prim ve Performans Haklari): Kordsa bunyesinde calisan personelin ucretlendirme, maas "
        "artislari, performans primleri ve yan haklari kurumsal Insan Kaynaklari politikaları ve yillik performans degerlendirme "
        "surecleri dogrultusunda belirlenir. Maas odemeleri her ayin son is gunu personelin resmi banka hesabina yatirilir. "
        "Ucret bordrolari ve detayli maas bilginiz icin HR Ozluk Portali uzerinden inceleme yapabilir veya HR yetkilisi ile gorusellersiniz.\n\n"
        "4. Adim (Kidem Bazli Yillik, Mazeret, Dogum ve Idari Izinler): Kordsa bunyesinde calisan personelin yillik ucretli izin sureleri "
        "4857 sayili Is Kanunu uyarinca hesaplanir. Hizmet suresi 1 yildan 5 yila kadar olan personelin yasal izin hakki 14 is gunudur. "
        "Izin talepleri en az 5 is gunu oncesinden HR Ozluk Sistemi uzerinden dijital olarak onay mekanizmasina iletilir. "
        "Mazeret, analik ve dogum izinleri kapsaminda kadin calisanlarin dogum izni suresi toplam 16 haftadir (dogum oncesi 8 hafta, dogum sonrasi 8 hafta). "
        "Erkek calisanlar icin babalik izni suresi ise 5 is gunudur."),
    "ISG_Kilavuz.pdf": (
        "Kordsa ISG Departmani - Fabrika Uretim Sahasi KKD, Acil Durum, Revir ve Ilk Yardim Yonetmeligi\n\n"
        "1. Adim (Yaralanma, Acil Durum ve Revir Ilk Yardim Proseduru): Fabrika sahasinda veya idari binalarda bir personelin "
        "yaralanmasi veya ani saglik sorunu yasamasi durumunda; derhal en yakin Sertifikali Ilk Yardimci personele ve "
        "Fabrika Revirine (Is Yeri Hekimi / Hemsire) haber verilmelidir. Olay yeri guvenligi saglanmadan yaraliya yetkisiz "
        "kisilerce mudahale edilmemelidir. Ciddi yaralanmalarda Guvenlik Vardiya Amiri uzerinden acil durum 112 Ambulans "
        "ekibi tesise davet edilir ve ISG birimine anlik bilgi verilir.\n\n"
        "2. Adim (Saha Risk Analizi ve Baret Kullanim Zorunlulugu): Kordsa fiili uretim sahalarina, kimyasal hammadde depolarina, "
        "ambar bolgelerine ve makine hatlarinin bulundugu alanlara koruyucu ekipman olmaksizin giris yapilmasi kesinlikle yasaktir. "
        "Uretim sahasinda baret kullanimi KESINLIKLE ZORUNLUDUR. Giris yapacak her personel, darbelere karsi koruyucu endustriyel baret, "
        "celik burunlu emniyet ayakkabisi, kulak koruyucu ve yuksek gorunurluklu reflektorlu yelek giymekle yukumludur.\n\n"
        "3. Adim (Ramak Kala ve Kaza Bildirim Islemleri): Meydana gelen her turlu yaralanma, is kazasi veya kaza atlatma durumu "
        "en gec 24 saat icinde ISG Birimine bildirilmeli ve Dijital Ramak Kala / Kaza Bildirim Formu doldurulmalidir."
    ),
    "Finans_Kilavuz.pdf": (
        "Kordsa Finans Departmani - Yurtiçi/Yurtdisi Is Seyahatleri, Masraf ve Avans Proseduru\n\n"
        "1. Adim (Seyahat On Onay ve Avans Talebi): Is seyahatleri seyahat tarihinden en az 7 is gunu oncesinden Seyahat Talep Formu "
        "ile amir ve Finans Direktorlugu onayina sunulur. Onaylanan seyahatler icin avans talebi Dijital Masraf Sistemi uzerinden yapilabilir.\n\n"
        "2. Adim (Fatura, Harcama ve Belge Giris Suresi): Konaklama, ulasim, taksi ve temsil agirlama harcamalarina ait e-fatura veya fisler "
        "seyahat bitisinden itibaren en gec 7 takvim gunu icinde Dijital Masraf Sistemine taranarak yuklenir. Fis kesim tarihi 30 gunu gecen harcamalar reddedilir.\n\n"
        "3. Adim (Muhasebe Kontrolu, Harcirah ve Odemeler): Muhasebe denetiminden gecen gecerli masraf tutarlari ve harcirah odemeleri "
        "her ayin belirlenen toplu odeme gunlerinde personelin banka maas hesabina EFT/Havale yoluyla yatirilir."
    ),
    "Planlama_Kilavuz.pdf": (
        "Kordsa Planlama Departmani - Talep Tahmini, Stok Kontrolu ve MRP Yonergesi\n\n"
        "1. Adim (Talep Analizi ve Tahmin Modelleri): Satis ve Pazarlama birimlerinden gelen siparis tahminleri konsolide edilerek "
        "gelecek 6 aylik hammadde, yari mamul ve kapasite planlamasi yapilir.\n\n"
        "2. Adim (MRP Stok Kontrolu ve Kritik Seviyeler): Net malzeme ihtiyaclari MRP (Malzeme Ihtiyac Planlamasi) sistemiyle gunluk "
        "takip edilir. Guvenli stok seviyesinin altina dusen kritik kimyasallar icin tedarik surecleri derhal tetiklenir.\n\n"
        "3. Adim (Uretim Emri ve SAT Olusturma): Eksik malzemeler icin sistem tarafindan otomatik Satin Alma Talebi (SAT) "
        "ve haftalik Uretim Emirleri (WO - Work Order) olusturularak üretime iletilir."
    ),
    "SatinAlma_Kilavuz.pdf": (
        "Kordsa Satin Alma Departmani - Tedarikci Yonetimi, RFP ve Onay Prosedurleri\n\n"
        "1. Adim (Tedarikci Kayit ve Kalite Incelemesi): Yeni tedarikciler teknik, mali yeterlilik, ISO 9001 ve ISO 14001 "
        "kalite belgelendirmeleri acisindan Kalite Kontrol birimiyle koordine sekilde incelemeye tabi tutulur.\n\n"
        "2. Adim (Teklif Toplama, RFP ve Karsilastirma): Satın alma talepleri (SAT) doğrultusunda en az 3 onayli tedarikciden "
        "teknik ve mali teklif istenerek (RFP) Teklif Karsilastirma Matrisi hazirlanir ve pazarlik yapilir.\n\n"
        "3. Adim (Sozlesme, NDA ve Hukuk Onayi): Anlasma saglanan tedarikcilerle Hukuk Departmani onayindan gecen ticari "
        "sozlesmeler ve Gizlilik Taahhutnamesi (NDA) resmi olarak imzalanir."
    ),
    "Uretim_Kilavuz.pdf": (
        "Kordsa Uretim Yonetimi - Kalite Kontrol, Vardiya, Ariza ve Bakim Talimati\n\n"
        "1. Adim (Kalite Numune Alimi ve Esik Degerler): Hatlardan cikan her 100 bitmis urunden 5 adet numune alinarak kalite testine tabi tutulur. "
        "Kusur orani kritik esik olan %2'yi gecerse ilgili uretim lotu (Batch) bloke edilir ve 8D raporu baslatilir.\n\n"
        "2. Adim (Vardiya Sistemi ve Ariza Bildirimi): Üretim sahasi 3 vardiya halinde kesintisiz calisir. CNC veya robotik hatlarda "
        "makine arizasi durumunda operator panelden acil bildirim yapar, Merkezi Bakim-Onarim ekibi en gec 15 dakika icinde mudahale eder.\n\n"
        "3. Adim (Bakim Gunlugu ve Parca Degisimi): Degisen kritik parçalar, teknik mudahaleler ve rutin bakimlar "
        "Makine Bakim Gunlugu veritabanina anlik olarak islenir."
    ),
    "Ambar_Kilavuz.pdf": (
        "Kordsa Ambar ve Depo Departmani - Stok Giris-Cikis, Mal Kabul ve Kargo Proseduru\n\n"
        "1. Adim (Mal Kabul, Kargo ve İrsaliye Kontrolu): Dis tedarikcilerden veya kargodan gelen hammaddeler Mal Kabul alaninda "
        "fatura, irsaliye ve Siparis Emri (PO) eslestirilerek teslim alinir. Kalite kontrol onayi sonrasi depoya aktarilir.\n\n"
        "2. Adim (FIFO Kurali ve Raf Stoklama): Depo raf sistemindeki malzeme cikislarinda ve uretim hattina hammadde beslemesinde "
        "stok omru kayiplarini engellemek amaciyla Ilk Giren Ilk Cikar (FIFO) kurali uygulanir.\n\n"
        "3. Adim (Periyodik Kor Sayim ve Stok Mutabakati): Ay sonlari kor sayim yontemiyle fiziki depo stoklari denetlenir. "
        "Sistem stoklari ile fiziki sayim arasinda sapma varsa Finans ve Depo Mudurlugu ortak inceleme yapar."
    )
}

def pdf_uret():
    styles = getSampleStyleSheet()
    style_justified = ParagraphStyle(
        name='Justified', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_JUSTIFY
    )
    print("Kurumsal PDF'ler yeni detaylarla zenginleştiriliyor...")
    for dosya_adi, metin in KORDSA_MEVZUATLAR.items():
        dosya_yolu = os.path.join(PDF_KLASORU, dosya_adi)
        doc = SimpleDocTemplate(dosya_yolu, pagesize=letter)
        story = []
        for p in metin.split("\n\n"):
            story.append(Paragraph(p, style_justified))
            story.append(Spacer(1, 12))
        doc.build(story)
        print(f" Başarıyla Oluşturuldu: {dosya_yolu}")

if __name__ == "__main__":
    pdf_uret()