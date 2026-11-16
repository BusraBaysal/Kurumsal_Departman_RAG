from src.yonlendirici import KolayRouter

router = KolayRouter()

sorular = [
    "CNC makinesi arızalandı bakım ekibi ne yapmalı?",
    "VPN bağlantısı açılmıyor",
    "Maaş bordromu nereden görebilirim?",
    "Baret kullanımı zorunlu mu?",
    "Yangın durumunda tahliye prosedürü nedir?",
    "Yeni tedarikçi nasıl açılır?",
    "Fatura ödeme süreci nasıl işler?",
    "Depoda stok sayımı nasıl yapılır?",
    "Üretim kapasitesi nasıl hesaplanır?",
    "Şirket yemekhanesi hakkında bilgi",
    "doğum izni ne kadar",
    "beş yıl ve üzeri kişilerin yıllık izni ne kadar",
    "maaş bordromu nasıl alırım",
    "vpn nasıl bağlanırım"
]
for soru in sorular:

    sonuc = router.rotayi_belirle(soru)

    print("--------------------------------")
    print("Soru:", soru)
    print("Departman:", sonuc["departman"])
    print("Alt Başlık:", sonuc["alt_baslik"])