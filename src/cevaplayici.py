import re
from src.db_yoneticisi import MSSQLYoneticisi
from src.reranker import BasitReranker


class KurumsalCevaplayici:
    def __init__(self):
        self.db_yonetici = MSSQLYoneticisi()
        self.reranker = BasitReranker()

        # Arama değerini düşüren etkisiz kelimeler (Stop Words)
        self.durak_kelimeler = {
            "nasıl", "nasil", "nedir", "ne", "neden", "niçin", "nicin", "kim", "kime", "kimden",
            "hangisi", "hangi", "kaç", "kac", "ne zaman", "ulaşabilirim", "ulasabilirim",
            "ulaşırım", "ulasirim", "alabilirim", "öğrenebilirim", "ogrenebilirim", "için", "icin",
            "göre", "gore", "ile", "veya", "ve", "de", "da", "ki", "hakkında", "hakkinda",
            "ilgili", "üzerine", "uzerine", "olan", "olduğu", "oldugu", "kadar", "adım", "adim",
            "peki", "normal", "calisan", "çalışan", "sistemleri", "sistemi", "oluyor"
        }

        # Eş anlamlı / İlişkili kelime haritası
        self.es_anlamlilar = {
            "maaş": ["ücret", "ucret", "bordro", "ödeme", "odeme", "hakediş"],
            "maas": ["ücret", "ucret", "bordro", "ödeme", "odeme"],
            "ücret": ["maaş", "maas", "ödeme", "odeme", "bordro"],
            "ucret": ["maaş", "maas", "ödeme", "odeme"],
            "izin": ["tatil", "mazeret", "rapor", "dinlenme"]
        }

    def turkce_kok_bul(self, kelime: str) -> str:
        """Kelimenin kökünü bozmadan eklerini temizler."""
        korunan_kelimeler = {
            "maaş", "maas", "ücret", "ucret",
            "izin", "vpn", "ip", "sgk"}
        if kelime.lower() in korunan_kelimeler:
            return kelime.lower()

        ekler = r'(larına|lerine|larından|lerinden|leriyle|larıyla|ından|inden|ında|inde|lara|lere|ları|leri|dan|den|tan|ten|nın|nin|nun|nün|ın|in|un|ün|ya|ye|a|e|ı|i|u|ü)$'
        temiz_kelime = re.sub(r'[^a-zA-ZçğıöşüÇĞİÖŞÜ]', '', kelime)
        if len(temiz_kelime) <= 3:
            return temiz_kelime

        kok = re.sub(ekler, '', temiz_kelime)
        return kok if len(kok) >= 3 else temiz_kelime

    def mssql_dokuman_ara(self, soru: str, departman_filtresi: str = None) -> tuple:
        bulunan_parcalar = []
        hesaplanan_skor = 0.0

        try:
            conn = self.db_yonetici.baglanti_al()
            cursor = conn.cursor()

            # 1. Kelimeleri ayıkla ve genişlet
            ham_kelimeler = [
                k.strip().lower()
                for k in soru.replace("?", "").replace("'", " ").split()
                if len(k) > 2]

            anlamli_kelimeler = [
                k for k in ham_kelimeler
                if k not in self.durak_kelimeler]
            kullanilacak_kelimeler = (
                anlamli_kelimeler) if anlamli_kelimeler else ham_kelimeler

            if not kullanilacak_kelimeler:
                return [], 0.0

            kok_kelimeler = list(set(
                [self.turkce_kok_bul(k)
                 for k in kullanilacak_kelimeler]))

            genisletilmis_kelimeler = list(kok_kelimeler)
            for k in kok_kelimeler:
                if k in self.es_anlamlilar:
                    genisletilmis_kelimeler.extend(self.es_anlamlilar[k])

            genisletilmis_kelimeler = list(set(genisletilmis_kelimeler))

            # 2. Ana SQL Arama Sorgusu
            query = """
                SELECT TOP 20 
                D.DosyaAdi,
                D.Departman, 
                M.SayfaNo, 
                M.MetinIcerik
        FROM MetinParcalari M
        JOIN Dokumanlar D 
             ON M.DokumanID = D.DokumanID
        WHERE 1=1
            """
            params = []

            if departman_filtresi and departman_filtresi not in ["Genel", "Otomatik Routing"]:
                query += " AND (D.Departman = ? OR D.Departman = 'Genel')"
                params.append(departman_filtresi)

            if genisletilmis_kelimeler:
                word_conditions = " AND (" + " OR ".join(
                    ["M.MetinIcerik LIKE ?" for _ in genisletilmis_kelimeler]) + ")"
                query += word_conditions
                for k in genisletilmis_kelimeler:
                    params.append(f"%{k}%")

            query += """
                ORDER BY 
                    CASE 
                        WHEN D.DosyaAdi LIKE '%Kilavuz%' THEN 1
                        WHEN D.DosyaAdi LIKE '%Prosedur%' THEN 2
                        ELSE 3
                    END ASC
            """

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # 3. Fallback Arama
            if not rows and departman_filtresi and departman_filtresi not in ["Genel", "Otomatik Routing"]:
                fallback_query = """
                    SELECT TOP 20 D.DosyaAdi, D.Departman, M.SayfaNo, M.MetinIcerik
                    FROM MetinParcalari M
                    JOIN Dokumanlar D ON M.DokumanID = D.DokumanID
                    WHERE (""" + " OR ".join(["M.MetinIcerik LIKE ?" for _ in genisletilmis_kelimeler]) + """)
                    ORDER BY 
                        CASE 
                            WHEN D.DosyaAdi LIKE '%Kilavuz%' THEN 1
                            WHEN D.DosyaAdi LIKE '%Prosedur%' THEN 2
                            ELSE 3
                        END ASC
                """

                fallback_params = [f"%{k}%" for k in genisletilmis_kelimeler]
                cursor.execute(fallback_query, fallback_params)
                rows = cursor.fetchall()

            if not rows:
                cursor.close()
                conn.close()
                return [], 0.0

            class TempDoc:
                def __init__(self, content, metadata):
                    self.page_content = content
                    self.metadata = metadata

            ham_belgeler = []
            for row in rows:
                ham_belgeler.append(TempDoc(
                    content=row.MetinIcerik,
                    metadata={"dosya": row.DosyaAdi, "dept": row.Departman, "sayfa": row.SayfaNo}
                ))

            # 4. Reranker
            sirali_sonuclar = self.reranker.sirala(
                soru,
                ham_belgeler,
                en_iyi=5
            )

            for item in sirali_sonuclar:
                doc = item["doc"]
                bulunan_parcalar.append({
                    "dosya": doc.metadata["dosya"],
                    "dept": doc.metadata["dept"],
                    "sayfa": doc.metadata["sayfa"],
                    "metin": doc.page_content
                })

            cursor.close()
            conn.close()

            # Güven Skoru
            if sirali_sonuclar:
                en_iyi_skor = sirali_sonuclar[0]["skor"]

                hesaplanan_skor = 0.55 + (
                        min(en_iyi_skor, 20) / 20
                ) * 0.35
                sonuc_bonusu = min(len(sirali_sonuclar), 4) * 0.01
                hesaplanan_skor += sonuc_bonusu

                hesaplanan_skor = min(hesaplanan_skor, 0.95)

                hesaplanan_skor = round(hesaplanan_skor, 2)

            else:
                hesaplanan_skor = 0.00

        except Exception as e:
            print("MSSQL Arama Hatası:", e)

        return bulunan_parcalar, hesaplanan_skor