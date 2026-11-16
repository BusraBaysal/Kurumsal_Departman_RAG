# Kurumsal Departman RAG Sistemi

Kurumsal departmanlara ait dokümanlardan yararlanarak kullanıcı sorularını yanıtlayan, soruları ilgili departmana yönlendiren ve yapay zekâ destekli yanıtlar üreten bir bilgi yönetim sistemidir.

## Proje Hakkında

Bu proje, kurum içi bilgiye erişimi kolaylaştırmak ve departmanlara yönelik soruları daha verimli şekilde yanıtlamak amacıyla geliştirilmiştir.

Sistem, kullanıcıdan gelen sorunun kurumsal kapsamda olup olmadığını kontrol eder. Uygun soruları ilgili departmana yönlendirir ve kurumsal dokümanlardan elde edilen bilgiler doğrultusunda yanıt oluşturur.

## Özellikler

- **Kurumsallık Kontrolü:** Kurum dışı soruların sistem tarafından filtrelenmesi.
- **Akıllı Departman Yönlendirme:** Soruların ilgili departmana otomatik yönlendirilmesi.
- **Doküman Tabanlı Yanıt Üretimi:** Kurumsal dokümanlardan yararlanarak yanıt oluşturulması.
- **Yapay Zekâ Entegrasyonu:** LLM destekli yanıt üretimi.
- **Manuel Departman Seçimi:** Kullanıcının belirli bir departmanı seçebilmesi.
- **Kaynak Gösterimi:** Yanıtlarda yararlanılan dokümanların ve sayfaların gösterilmesi.
- **Performans Takibi:** Sorgu sayısı, güven skoru ve yanıt süresinin görüntülenmesi.
- **Geri Bildirim:** Kullanıcıların yanıtları değerlendirebilmesi.
- **Veritabanı Kaydı:** Soru ve yanıt bilgilerinin MSSQL veritabanına kaydedilmesi.

## Kullanılan Teknolojiler

| Teknoloji | Kullanım Alanı |
|---|---|
| Python | Ana programlama dili |
| Streamlit | Kullanıcı arayüzü |
| LangChain | LLM ve doküman işleme altyapısı |
| Ollama | Yerel dil modeli entegrasyonu |
| PyPDF | PDF dokümanlarının işlenmesi |
| Microsoft SQL Server | Veritabanı yönetimi |
| PyODBC | Veritabanı bağlantısı |

## Proje Yapısı

```text
Kurumsal_Departman_RAG/
│
├── dokumanlar/          # Kurumsal PDF dokümanları
│
├── src/
│   ├── __init__.py
│   ├── cevaplayici.py
│   ├── db_yoneticisi.py
│   ├── llm_cevaplayici.py
│   ├── reranker.py
│   ├── soru_kontrol.py
│   └── yonlendirici.py
│
├── app.py
├── main.py
├── requirements.txt
├── veri_artirma_motoru.py
│
├── test_arama.py
├── test_router.py
└── test_soru_kontrol.py
```

## Sistemin Çalışma Mantığı

1. Kullanıcı, Streamlit arayüzü üzerinden sorusunu iletir.
2. Soru, kurumsallık kontrolünden geçirilir.
3. Kurumsal olmayan sorular filtrelenir.
4. Uygun sorular otomatik yönlendirme veya manuel seçim yoluyla ilgili departmana aktarılır.
5. İlgili dokümanlardan yararlanılarak yapay zekâ destekli yanıt oluşturulur.
6. Yanıt, ilgili kaynak bilgileriyle kullanıcıya sunulur.
7. Soru ve yanıt bilgileri veritabanına kaydedilir.

## Kurulum

Projeyi bilgisayarınıza indirin:

```bash
git clone https://github.com/BusraBaysal/Kurumsal_Departman_RAG.git
```

Proje klasörüne geçin:

```bash
cd Kurumsal_Departman_RAG
```

Sanal ortam oluşturun:

```bash
python -m venv .venv
```

Sanal ortamı etkinleştirin (Windows):

```bash
.venv\Scripts\activate
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
streamlit run app.py
```

Uygulamanın çalışabilmesi için Ollama ve Microsoft SQL Server bağlantılarının ilgili proje yapılandırmalarına göre hazırlanması gerekir.

## Testler

Projede farklı işlevleri kontrol etmek amacıyla test dosyaları bulunmaktadır:

- `test_arama.py`: Arama işlemlerinin test edilmesi.
- `test_router.py`: Departman yönlendirme işlemlerinin test edilmesi.
- `test_soru_kontrol.py`: Kurumsallık kontrolünün test edilmesi.

## Geliştirici

**Büşra Baysal**

GitHub: [@BusraBaysal](https://github.com/BusraBaysal)

---

Bu proje, Python kullanılarak geliştirilmiş yapay zekâ destekli kurumsal bilgi yönetimi ve doküman tabanlı soru-cevap sistemidir.