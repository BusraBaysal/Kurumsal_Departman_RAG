import unicodedata

class KolayRouter:
    def __init__(self):
        pass

    def rotayi_belirle(self, soru: str) -> dict:
        soru_lower = unicodedata.normalize("NFKD", soru)
        soru_lower = soru_lower.encode("ASCII", "ignore").decode("ASCII").lower()

        # 1. HR / İnsan Kaynakları (Öncelikli)
        if any(kelime in soru_lower for kelime in [
            "insan kaynaklari", "insan", "kaynaklari", "hr", "ik", "ulasabilirim", "ulasim",
            "iletisim", "telefon", "mail", "eposta", "izin", "yillik", "yil", "bes", "uzeri",
            "kidem", "dogum", "babalik", "bordro", "maas", "ucret", "ozluk", "personel",
            "ise alim", "kariyer", "yemek", "yemekhane", "servis", "yan hak"
        ]):
            return {
                "departman": "HR", "alt_baslik": "İzin & Özlük Hakları / İletişim"
            }

        # 2. Hukuk
        elif any(kelime in soru_lower for kelime in [
            "kanun", "mevzuat", "anayasa", "tuzuk", "yargi", "teftis",
            "dijital mecra", "mke", "nukleer", "sigortacilik", "telgraf",
            "hukuk", "davalar", "madde", "resmi gazete"
        ]):
            return {
                "departman": "Hukuk", "alt_baslik": "Mevzuat & Hukuki Düzenlemeler"
            }

        # 3. BT
        elif any(kelime in soru_lower for kelime in [
            "vpn", "mfa", "bilgisayar", "eposta", "mail", "siber", "yetki", "parola"
        ]):
            return {
                "departman": "BT", "alt_baslik": "Siber Güvenlik & Yetkilendirme"
            }

        # 4. İSG
        elif any(kelime in soru_lower for kelime in [
            "isg", "is guvenligi", "is sagligi", "guvenlik", "kkd", "baret", "ayakkabi",
            "is ayakkabisi", "ramak", "kaza", "yangin", "tahliye", "acil durum", "koruyucu",
            "egitim", "risk", "tehlike"
        ]):
            return {
                "departman": "İSG", "alt_baslik": "İş Sağlığı ve Güvenliği"
            }

        # 5. Finans
        elif any(kelime in soru_lower for kelime in [
            "masraf", "fatura", "odeme", "avans", "butce"
        ]):
            return {
                "departman": "Finans", "alt_baslik": "Masraf & Avans Onayları"
            }

        # 6. Üretim
        elif any(kelime in soru_lower for kelime in [
            "ariza", "bakim", "cnc", "makine"
        ]):
            return {
                "departman": "Üretim", "alt_baslik": "Makine Bakım-Onarım"
            }

        return {
            "departman": "Genel", "alt_baslik": "Genel Konular"
        }