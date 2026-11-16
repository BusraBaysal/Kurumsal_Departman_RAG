import pyodbc


class MSSQLYoneticisi:
    def __init__(self):
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-P3JDOOV\\SQLEXPRESS;"
            "DATABASE=KordsaRAGDB;"
            "Trusted_Connection=yes;"
        )
        self.tablolari_kontrol_et_ve_olustur()

    def baglanti_al(self):
        return pyodbc.connect(self.connection_string)

    def tablolari_kontrol_et_ve_olustur(self):
        """GeriBildirimler tablosu veritabanında yoksa otomatik oluşturur."""
        try:
            conn = self.baglanti_al()
            cursor = conn.cursor()

            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'GeriBildirimler')
                BEGIN
                    CREATE TABLE GeriBildirimler (
                        ID INT IDENTITY(1,1) PRIMARY KEY,
                        KullaniciSorusu NVARCHAR(MAX),
                        UretilenCevap NVARCHAR(MAX),
                        Puan INT, -- 1: Beğendi (👍), -1: Beğenmedi (👎)
        
                    );
                END
            """)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("MSSQL Tablo Kontrol/Oluşturma Hatası:", e)

    def dokuman_ve_parca_kaydet(self, dosya_adi: str, departman: str, parcalar: list):
        """PDF dosyasını ve parçalarını MSSQL'e kaydeder."""
        try:
            conn = self.baglanti_al()
            cursor = conn.cursor()

            # 1. Dokümanı ekle
            cursor.execute("""
                INSERT INTO Dokumanlar (DosyaAdi, Departman) 
                OUTPUT INSERTED.DokumanID 
                VALUES (?, ?)
            """, (dosya_adi, departman))

            dokuman_id = cursor.fetchone()[0]

            # 2. Metin Parçalarını (Chunks) ekle
            for parca in parcalar:
                sayfa = parca.metadata.get("page", 0)
                metin = parca.page_content

                cursor.execute("""
                    INSERT INTO MetinParcalari (DokumanID, SayfaNo, MetinIcerik)
                    VALUES (?, ?, ?)
                """, (dokuman_id, sayfa, metin))

            conn.commit()
            cursor.close()
            conn.close()
            print(f"MSSQL Kayıt Başarılı: {dosya_adi} (ID: {dokuman_id})")
        except Exception as e:
            print(f"MSSQL Doküman Kayıt Hatası ({dosya_adi}):", e)

    def log_kaydet(self, soru: str, cevap: str, dept: str, sub: str, skor: float, sure: float):
        """Kullanıcı aramalarını ve yanıt loglarını MSSQL'e kaydeder."""
        try:
            conn = self.baglanti_al()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO SistemLoglari (KullaniciSorusu, UretilenCevap, TahminDepartman, TahminAltBaslik, DogrulukSkoru, YakitSuresiSn)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (soru, cevap, dept, sub, skor, sure))

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("MSSQL Log Kayıt Hatası:", e)

    def geri_bildirim_kaydet(self, soru: str, cevap: str, puan: int):
        """
        Kullanıcıların üretime verdiği geri bildirimleri (👍: 1, 👎: -1) MSSQL'e kaydeder.
        """
        try:
            conn = self.baglanti_al()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO GeriBildirimler (KullaniciSorusu, UretilenCevap, Puan)
                VALUES (?, ?, ?)
            """, (soru, cevap, puan))

            conn.commit()
            cursor.close()
            conn.close()
            print(f"MSSQL Geri Bildirim Başarıyla Kaydedildi (Puan: {puan})")
            return True
        except Exception as e:
            print("MSSQL Geri Bildirim Kayıt Hatası:", e)
            return False