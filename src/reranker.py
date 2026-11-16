class BasitReranker:

    def __init__(self):
        self.kelime_agirliklari = {
            # İşlem ve Maaş/Özluk Odaklı
            "maaş": 8, "maas": 8, "ücret": 7, "ucret": 7, "bordro": 8, "ödeme": 6, "odeme": 6,
            "banka": 5, "hesap": 5, "izin": 7, "gün": 5, "günleri": 5,

            # BT & Teknik
            "vpn": 7, "ssl-vpn": 6, "mfa": 5, "parola": 5, "sertifika": 4,

            # İSG
            "baret": 7, "kkd": 7, "yaralanma": 7, "revir": 7, "kaza": 6
        }

    def sirala(self, soru, belgeler, en_iyi=3):
        soru = soru.lower()
        puanli = []

        for doc in belgeler:
            metin = doc.page_content.lower()
            skor = 0

            # Kelime ağırlıkları kontrolü
            for kelime, agirlik in self.kelime_agirliklari.items():
                if kelime in soru and kelime in metin:
                    skor += agirlik

            # Şirket kılavuzu geçen parçalara ekstra puan ver
            if "kilavuz" in doc.metadata.get("dosya", "").lower():
                skor += 5

            # Adım anlatan kısımlara puan ver
            if "3. adim" in metin or "maaş" in metin:
                skor += 4

            puanli.append({
                "doc": doc,
                "skor": skor
            })

        puanli.sort(
            key=lambda x: x["skor"],
            reverse=True
        )
        return puanli[:en_iyi]