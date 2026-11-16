import sys
import os

# Proje dizinini ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.db_yoneticisi import MSSQLYoneticisi

def arama_testi(soru: str, departman_filtresi: str = None):
    db = MSSQLYoneticisi()
    conn = db.baglanti_al()
    cursor = conn.cursor()

    print(f"\n================ TEST BAŞLADI ================")
    print(f"Gelen Soru: '{soru}'")
    print(f"Departman Filtresi: '{departman_filtresi}'")

    # 1. Kelime Ayıklama Kontrolü
    kelimeler = [k.strip().lower()
    for k in soru.replace("?", "").replace("'", " ").split()
    if len(k) > 2]

    print(f"\n1. Ayıklanan Arama Kelimeleri ({len(kelimeler)} adet): {kelimeler}")

    # 2. SQL Sorgusu Oluşturma
    query = """
        SELECT TOP 10 
        D.DokumanID, 
        D.DosyaAdi, 
        D.Departman, 
        M.SayfaNo, 
        LEFT(M.MetinIcerik, 100) AS OzetMetin
        FROM MetinParcalari M
        JOIN Dokumanlar D ON M.DokumanID = D.DokumanID
        WHERE 1=1
    """
    params = []

    if departman_filtresi and departman_filtresi != "Genel":
        query += " AND (D.Departman = ? OR D.Departman = 'Genel')"
        params.append(departman_filtresi)

    if kelimeler:
        word_conditions = " AND (" + " OR ".join(
            ["M.MetinIcerik LIKE ?" for _ in kelimeler]
        ) + ")"
        query += word_conditions
        for k in kelimeler:
            params.append(f"%{k}%")

    print(f"\n2. Çalıştırılacak SQL Sorgusu:\n{query}")
    print(f"Parametreler: {params}")

    # 3. Sorgu Sonuçları
    cursor.execute(query, params)
    rows = cursor.fetchall()

    print(f"\n3. Dönen Sonuç Sayısı: {len(rows)}")
    if rows:
        print("\n--- Yakalanan Dokümanlar ---")
        for idx, row in enumerate(rows, 1):
            print(f"[{idx}] DokumanID: {row.DokumanID} | Departman: {row.Departman} | Dosya: {row.DosyaAdi}")
            print(f"    Özet İçerik: {row.OzetMetin}...\n")
    else:
        print("HİÇ BİR SONUÇ BULUNAMADI!")

    # 4. Hangi Kelimenin Doküman ID 9'u Getirdiğini Tespit Etme
    print("\n4. Kelime Bazlı Detaylı Eşleşme Analizi:")
    for k in kelimeler:
        check_query = """
            SELECT COUNT(*) 
            FROM MetinParcalari 
            WHERE MetinIcerik LIKE ? AND DokumanID = 9
        """
        cursor.execute(check_query, (f"%{k}%",))
        count = cursor.fetchone()[0]
        print(f"   -> '{k}' kelimesi Doküman ID 9 içinde {count} kez geçiyor.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Test etmek istediğim soru
    arama_testi("insan kaynaklarına nasıl ulaşabilirim", departman_filtresi="HR")