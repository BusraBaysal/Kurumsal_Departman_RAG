from src.soru_kontrol import SoruKontrol

kontrol = SoruKontrol()

sorular = [

    "VPN bağlantım açılmıyor",

    "Baret kullanımı zorunlu mu?",

    "Yeni tedarikçi nasıl oluşturulur?",

    "Python'da liste nasıl oluşturulur?",

    "Galatasaray kaç puan aldı?"
]

for soru in sorular:

    sonuc = kontrol.kurumsal_mi(soru)

    print("-------------------------")
    print("SORU:", soru)
    print("KURUMSAL MI:", sonuc)