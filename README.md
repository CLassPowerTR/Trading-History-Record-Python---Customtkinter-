Proje Adı
Gelir-Gider Takip Uygulaması

Açıklama
Bu proje, Python dili kullanılarak geliştirilmiş basit bir masaüstü “Gelir-Gider Takip” uygulamasıdır.

GUI: customtkinter kütüphanesi ile tasarlanmıştır.

Veri Tabanı: Uygulama içi tüm gelir ve gider verileri SQLite ile saklanır.

Uygulama üç ana sayfadan oluşur:

Temel Görünüm (Ana Sayfa)

Gider Ekleme Sayfası

Gelir Ekleme Sayfası

Kullanıcı, gelir ve giderlerini ekleyebilir; eklenmiş verileri görüntüleyebilir, düzenleyebilir veya silebilir. Böylece aylık/haftalık bazda finans takibi yapılabilir.

Özellikler
Temel Görünüm

Tüm gelir ve gider kalemleri listelenir.

Toplam gelir, toplam gider ve net bakiye bilgisi gösterilir.

Gider Ekleme

Yeni bir gider kaydı eklenebilir.

Gider başlığı, miktarı, tarihi ve kategori bilgisi girilir.

Gelir Ekleme

Yeni bir gelir kaydı eklenebilir.

Gelir başlığı, miktarı, tarihi ve kaynak bilgisi girilir.

Veri Yönetimi

Mevcut gelir/gider kayıtları düzenlenebilir (başlık, miktar, tarih vb. güncellenebilir).

Yanlış girilen kayıtlar silinebilir.

SQLite veritabanı sayesinde tüm kayıtlar kalıcı olarak saklanır.

Teknolojiler
Python 3.13.3

customtkinter (Graphical User Interface)

sqlite3 (Veritabanı)

Standart Python kütüphaneleri: os, datetime, sqlite3, Calendar, locale, customtkinter, tkinter, threading

Kurulum ve Çalıştırma
Aşağıdaki adımları izleyerek projeyi kendi bilgisayarında çalıştırabilirsin:

1- Depoyu Klonla;
git clone https://github.com/kullaniciadi/proje-adi.git
cd proje-adi

2- Sanal Ortam (Virtual Environment) Oluştur (Önerilir);
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3- Gerekli Paketleri Yükle
pip install customtkinter

4- Uygulamayı Çalıştır
python main.py

Kullanım
Ana Sayfa (Temel Görünüm)

Uygulama açıldığında burası görüntülenir.

Üst menüden “Gider Ekle” veya “Gelir Ekle” sayfalarına geçiş yapabilirsin.

Ekranda Yıl, ay ve güne göre filtereyip mevcut durumda ki Kar, Gelir ve Gider toplamlarını görebilirsiniz.

Gider Ekleme Sayfası

“Gider Başlığı”, “Miktar”, “Tarih” ve “Tutar” alanlarını doldurarak yeni bir gider kaydedebilirsin.

“Kaydet” butonuna tıkladığında, bilgiler veritabanına eklenir ve ana sayfaya dönersin.

Kayıtları filtreleyip girilen inputa göre filtreleyebilirsiniz.

Kayıt üzerine tıklayıp güncelleyebilir veya silebilirsiniz.

Gelir Ekleme Sayfası

“Gelir Başlığı”, “Miktar”, “Tarih” ve “Tutar” alanlarını doldurarak yeni bir gelir kaydedebilirsin.

“Kaydet” butonuna tıkladığında, bilgiler veritabanına eklenir ve ana sayfaya dönersin.

Kayıtları filtreleyip girilen inputa göre filtreleyebilirsiniz.

Kayıt üzerine tıklayıp güncelleyebilir veya silebilirsiniz.


Anasayfa
![Ekran görüntüsü 2025-06-01 210002](https://github.com/user-attachments/assets/e5b3c8a5-c5a4-4dd3-b393-6322a4916bf4)

Kayıtlar
![Ekran görüntüsü 2025-06-01 210002](https://github.com/user-attachments/assets/bf71d36e-54e3-49f2-bbac-07a0481c5a8d)

Kayıt Ekranı
![Ekran görüntüsü 2025-06-01 210002](https://github.com/user-attachments/assets/04b530c7-e170-483c-a249-084fed19132f)

Kayıt Düzenleme
![Ekran görüntüsü 2025-06-01 210002](https://github.com/user-attachments/assets/886f48dd-b7e1-4ebf-86ed-7742c4d7e6e6)


