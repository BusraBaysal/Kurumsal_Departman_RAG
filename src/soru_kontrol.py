import unicodedata

class SoruKontrol:

    def __init__(self):
        self.kurumsal_kelimeler = [
            # İletişim & Ulaşım & Genel Başvuru
            "ulasabilirim", "ulaşabilirim", "ulasing", "ulaşım", "ulasim", "iletisim", "iletişim",
            "irtibat", "telefon", "numara", "numarasi", "numarası", "mail", "eposta", "e-posta",
            "adres", "konum", "bina", "ofis", "destek", "yardim", "yardım", "nasil", "nasıl",

            # İnsan Kaynakları & İK & HR
            "insan kaynaklari", "insan kaynakları", "insan", "kaynaklari", "kaynakları",
            "hr", "ik", "ozluk", "özlük", "personel", "ise alim", "işe alım", "staj", "stajyer",
            "kariyer", "ucret", "ücret", "maas", "maaş", "bordro", "prim", "izin", "izni",

            # Çevre & Ajans & Mevzuat
            "cevre", "çevre", "ajans", "ajansi", "ajansı", "cevre ajansi", "çevre ajansı",
            "nukleer", "nükleer", "düzenleme", "duzenleme", "lisans", "kurulus", "kuruluş",

            # Hukuk & Mevzuat
            "kanun", "mevzuat", "anayasa", "tuzuk", "tüzük", "yargi", "yargı", "teftis", "teftiş",
            "dijital mecra", "mke", "sigortacilik", "sigortacılık", "telgraf", "hukuk", "davalar",
            "madde", "resmi gazete", "yürürlük", "mülga", "hüküm", "tse", "insan haklari",

            # Genel kurumsal ifadeler & Çalışma Saatleri
            "prosedur", "prosedür", "talimat", "dokuman", "doküman", "form", "surec",
            "süreç", "politika", "yonetmelik", "yönetmelik", "calisan", "çalışan",
            "departman", "onay", "mesai", "saat", "saatleri", "giris", "giriş", "cikis",
            "çıkış", "vardiya", "servis", "mola", "bilgi",

            # BT & Sistemler
            "vpn", "parola", "mfa", "yetki", "bilgisayar", "sistem", "bt",

            # Üretim & Bakım
            "cnc", "makine", "bakim", "bakım", "ariza", "arıza", "kalite", "numune", "uretim", "üretim",

            # İSG & Acil Durum & Revir
            "isg", "baret", "kkd", "yangin", "yangın", "tahliye", "kaza", "risk", "tehlike",
            "yaralanma", "yaralandiginda", "yaralandığında", "ilk yardim", "ilkyardim", "ilk yardım",
            "revir", "doktor", "hekim", "mudahale", "müdahale", "acil", "ambulans",

            # Satın Alma & Finans & Ambar & Planlama
            "tedarik", "teklif", "sozlesme", "sözleşme", "rfp", "nda", "fatura", "masraf",
            "avans", "butce", "bütçe", "seyahat", "stok", "ambar", "depo", "sayim", "sayım",
            "fifo", "planlama", "kapasite", "mrp", "talep", "sat", "wo"
        ]

    def kurumsal_mi(self, soru: str) -> bool:
        if not soru:
            return False

        soru_alt = soru.lower()
        soru_ascii = unicodedata.normalize("NFKD", soru_alt).encode("ASCII", "ignore").decode("ASCII")

        return any(
            kelime in soru_alt or kelime in soru_ascii
            for kelime in self.kurumsal_kelimeler
        )