<div align="center">

# GAZİ ÜNİVERSİTESİ

</div>

Mühendislik Fakültesi – Bilgisayar Mühendisliği Bölümü

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495493.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=0wLxSsAH%2F%2BSzEif5fsMD4z8MXKc%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

# BM314 Yazılım Mühendisliği

</div>

<div align="center">

# SOFTWARE DESIGN DESCRIPTION (SDD)

</div>

FocuSync

Hazirlayanlar:

- Mehmet Koksal - 23118080060

- Yunus Recepoğlu - 23118080019

- Zeynep Yamaç - 23118080080

- Kerem Kapısız - 22118080009

- Mehmet Akif Türk - 23118080702

22 Nisan 2026, Ankara

## Revizyon Sayfası

<table border="1"><tr><td>Sürüm</td><td>Tarih</td><td>Yazar(lar)</td><td>Açıklama</td></tr><tr><td>1.0</td><td>18 Nisan 2026</td><td>Mehmet Köksal, Yunus Recepoğlu, Zeynep Yamaç, Kerem Kapısız, Mehmet Akif Türk</td><td>SDD (Yazılım Tasarım Tanımlaması) ilk taslağı oluşturuldu</td></tr><tr><td>1.1</td><td>22 Nisan 2026</td><td>Mehmet Köksal, Yunus Recepoğlu</td><td>Kimlik Doğrulama Tasarımı bölümü güncellendi</td></tr></table>

## İçindekiler

1. Kapsam ... 7

1.1 Tanım ... 7

1.2 Sisteme Genel Bakış ... 7

1.3 Dokümana Genel Bakış ... 8

2. İlgili Dokümanlar ... 9

2.1 Software Requirements Specification (SRS) ... 9

2.2 Software Project Management Plan (SPMP) ... 9

2.3 Kullanılan Teknolojiler ve Harici Kaynaklar ... 9

2.4 Referans Standartlar ... 10

3. Sistem Çapında Tasarım Kararları ... 11

3.1 Genel Mimari Yaklaşım ... 11

3.2 Katmanlı Yapı ve Modüler Tasarım Kararı ... 11

3.3 Masaüstü Uygulama Tasarım Kararları ... 12

3.4 Mobil Uygulama Tasarım Kararları ... 12

3.5 Veritabanı Tasarım Kararları ... 14

    3.5.1 Mimari Tercih ve Merkezi Erişim (Gateway) Pattern ... 14

    3.5.2 Güvenlik ve Yetkilendirme Stratejisi ... 14

    3.5.3 Veri Bütünlüğü ve Koruma Mekanizmaları ... 14

3.6 Gerçek Zamanlı İşleme ve Multithreading Kararları ... 15

    3.6.1 Görüntü İşleme ve Arayüz Optimizasyonu (Kafa Takibi Modülü): ... 15

    3.6.2 Aktif Uygulama İzleme ve Win32 API İzolasyonu (Whitelist Modülü): ... 15

    3.6.3 Asenkron OCR ve Yapay Zeka İstekleri (Program/Sınav Modülü): ... 16

3.7 Güvenlik ve Kimlik Doğrulama Tasarımı ... 16

    3.7.1 Kriptografik Şifreleme ve Veri Saklama ... 16

    3.7.2 Oturum Güvenliği ve Kalıcılık ... 17

3.8 Gizlilik ve Kamera Verisi İşleme Yaklaşımı ... 17

    3.8.1 Yerel İşleme İlkesi (Local-Only Processing) ... 17

    3.8.2 Görüntü Verisinin Kalıcılığı ... 17

    3.8.3 Sayısal Veriye Dönüştürme (Anonymization) ... 17

    3.8.4 Kullanıcı Farkindalığı ve Kontrolü ... 18

    3.8.5 Üçuncü Taraf Kütüphanelerin Güvenliği ... 18

3.9 Hata Yönetimi ve Dayanıklılık Tasarımı: ... 18

    3.9.1 Donanım Hataları ve İstisna Yönetimi ... 18

    3.9.2 Ağ Bağlantısı ve Veri Tutarlılığı (Offline/Online Resilience) ... 18

3.9.3 Yapay Zeka (OCR) Hata Toleransı ...19

4. FocuSync Sisteminin Yapısal Tasarımı ...20

4.1 Sistem Bileşenleri ...20

4.2 Üst Düzey Mimari Diyagramı (Açıklamalı) ...20

4.3 Bileşenler Arası İlişkiler ...21

4.4 Veri Akışı Genel Yapısı ...21

4.5 Arayüz Tasarımı ...22

5. Ayrıntılı Tasarım ...23

5.1 Kullanıcı Giriş ve Profil Modülü ...23

    5.1.1 Amaç ...23

    5.1.2 Girdi / Çıktılar ...23

    5.1.3 Kimlik Doğrulama ve İşleyiş Mantığı ...23

    5.1.4 Hata Durumları ...24

    5.1.5 Veritabanı Etkileşimi ...24

5.2 Ders Yönetimi Modülü ...24

    5.2.1 Amaç ...24

    5.2.2 Girdi / Çıktılar ...24

    5.2.3 Temel İş Süreçleri (CRUD Operasyonları) ...25

    5.2.4 Algoritmik Parametre Yönetimi ...25

    5.2.5 Veritabanı Etkileşimi ...25

5.3 Program ve Sınav Yönetimi Modülü ...26

    5.3.1 Amaç ...26

    5.3.2 Manuel Giriş Tasarımı ...26

    5.3.3 PDF / OCR Tabanlı Veri Alma Tasarımı ...26

    5.3.4 Veri Doğrulama ve Kullanıcı Onayı ...27

    5.3.5 Hata Yönetimi ...27

5.4 Odak Oturumu Yönetimi Modülü ...28

    5.4.1 Amaç ...28

    5.4.2 Oturum Başlatma / Durdurma / Duraklatma Akışı ...28

    5.4.3 Zamanlayıcı Yönetimi ...28

    5.4.4 Oturum Verisi Oluşturma ...28

    5.4.5 Diğer Modüllerle Etkileşim ...29

5.5 Kafa Takibi ve Odak Skoru Modülü ...29

    5.5.1 Amaç ...29

    5.5.2 Kamera Akışı İşleme Tasarımı ...29

    5.5.3 Yüz Tespiti ve Landmark Kullanımı ...29

    5.5.4 Pitch / Yaw / Roll Hesaplama ...30

5.5.5 Referans Açı Belirleme ...30

5.5.6 Dikkat Dağılması Tespit Mantığı ...30

5.5.7 Odak Skoru Hesaplama ...30

5.5.8 Performans ve Hata Yönetimi ...30

5.6 Beyaz Liste (Whitelist) Kontrol Modülü ...31

5.6.1 Amaç ...31

5.6.2 Whitelist Veri Yapısı Tasarımı ...31

5.6.3 Uygulama Ekleme / Silme / Listeleme Süreci ...31

5.6.4 Aktif Pencere ve Süreç İzleme Mekanizması ...32

5.6.5 İhlal Tespit Mantığı ...32

5.6.6 Sesli ve Görsel Uyarı Tasarımı ...32

5.6.7 İhlal Süresi Hesaplama ...33

5.6.8 Oturum Sonu İhlal Özeti Oluşturma ...33

5.6.9 Veritabanı Etkileşimi ...33

5.7 Adaptif Zorluk Güncelleme Modülü ...34

5.7.1 Amaç ...34

5.7.2 Kullanılan Girdiler ...34

5.7.3 Zorluk Güncelleme Algoritması ...34

5.7.4 Yeni Çalışma Planı Üretimi ...35

5.7.5 Sınırlar ve Kısıtlar ...35

5.8 İstatistik ve Raporlama Modülü ...35

5.8.1 Amaç ...35

5.8.2 Toplanan Veriler ...35

5.8.3 İstatistik Hesaplama Yöntemi ...36

5.8.4 Kullanıcıya Sunulan Raporlar ...36

5.8.5 Görselleştirme Tasarımı ...36

5.9 Mobil Senkronizasyon Modülü ...36

5.9.1 Amaç ...36

5.9.2 Senkronizasyon Mantığı ...37

5.9.3 Masaüstü–Mobil Veri Akışı ...37

5.9.4 Tutarlılık ve Çakışma Yönetimi ...38

5.10 Veritabanı Tasarımı ...38

5.10.1 Genel Veritabanı Mimarisi ...38

5.10.2 Koleksiyonlar / Tablolar ...39

5.10.3 Kullanıcı (Users) Koleksiyonu ...39

5.10.4 Ders (Courses) Koleksiyonu ...39

5.10.5 Sabit Program (Schedules) Koleksiyonu ...40

5.10.6 FocuSync Önerilen Program (StudyPlans) Koleksiyonu ...41

5.10.7 Çalışma Oturumu (Focus Sessions) Kolekisyonu ...41

5.10.8 Uygulama İzleme (WhiteList) Koleksiyonu ...42

5.10.9 Sınavlar (Exams) Koleksiyonu ...42

5.10.10 İlişkiler ve Veri Bütünlüğü ...43

5.11 Mobil Kullanıcı Giriş Modülü ...43

5.11.1 Amaç ...43

5.11.2 Girdiler ve Çıktılar ...43

5.11.3 İşleyiş Mantığı ...44

5.11.4 Hata Durumları ...45

5.11.5 Veritabanı Etkileşimi ...45

5.12 Kullanıcı Arayüzü Tasarımı ...46

5.12.1 Giriş / Kayıt Ekranı ...46

5.12.2 Dashboard Ekranı ...47

5.12.3 Ders Programı Ekranı ...49

5.12.4 Notlar Ekranı ...51

5.12.5 Odak Modu Ekranı: ...53

5.12.6 Whitelist Yönetim Ekranı ...54

5.12.7 İstatistikler Ekranı ...57

5.12.8 Mobil Arayüz Ekranları ...58

6. Gereksinimlerin İzlenebilirliği ...63

6.1 SRS Gereksinimlerinden Tasarım Bileşenlerine İzlenebilirlik ...63

6.2 Modüllerden Gereksinimlere Geri İzlenebilirlik ...67

6.3 Gereksinim–Modül Eşleştirme Tablosu ...69

7. Notlar ...71

7.1 Kısaltmalar ...71

7.2 Terimler Sözlüğü ...71

7.3 Tasarım Varsayımları ...72

7.4 Gelecek Sürümler İçin Genişletme Notları ...72

8. Ekler ...74

## 1. Kapsam

## 1.1 Tanim

FocuSync; özellikle bilgisayar başında uzun süre çalışan lise ve üniversite öğrencilerinin akademik verimliliklerini ölçmek, dikkat dağınklığını minimize etmek ve çalışma alışkanlıklarını dinamik olarak optimize etmek amacıyla geliştirilen entegre bir odaklanma ekosistemidir. Sistem, temel olarak iki uçlu bir mimari üzerine kuruludur: Kullanıcının fiziksel odaklanma düzeyini gerçek zamanlı görüntü işleme teknikleriyle takip eden bir masaüstü uygulaması ve bu verilerin istatistiksel analizlerine her an erişim imkanı sunan bir mobil uygulama.

FocuSync’i geleneksel zaman yönetimi araçlarından ayiran temel fark; kafa yönü takibi (headtracking) ve aktif pencere denetimi (whitelist) gibi objektif verileri kullanarak, kullanıcının o anki dikkat seviyesine göre ders çalışma stratejilerini "Adaptif Zorluk" algoritmasıyla anlık olarak güncelleyebilmesidir.

## 1.2 Sisteme Genel Bakış

FocuSync sistemi, operasyonel yükün yerelde paylaştırıldığı ve veri buttünlüğünün bulutta sağlandığı "Kalın İstemci - Bulut Arka Uç" (Thick Client - Cloud Backend) mimarisini benimser. Sistemin çalışma döngüsü su ana bileşenler etrafında sekillenir:

- Veri Girişi ve OCR Modülü: Kullanıcılar akademik takvimlerini manuel olarak girebildiği gibi, OBS (Ögrenci Bilgi Sistemi) üzerinden temin ettikleri PDF formatindaki ders programlarını Google Gemini AI destekli OCR mekanizmasıyla sisteme otomatik olarak entegre edebilirler.

- Analiz ve Denetim Katmanı: Masaüstü istemcisi, OpenCV ve MediaPipe kütüphanelerini kullanarak web kamerası üzerinden kafa pozisyonu (Pitch, Yaw, Roll) analizi yapar. Eş zamanlı olarak çalışan "Whitelist" modülü, işletim sistemi seviyesindeki prosesleri dinleyerek odak seansı sırasında sadece izin verilen uygulamaların kullanılmasına müsaade eder.

- Adaptif Karar Motoru: Kafa takibi ve uygulama ihlallerinden elde edilen veriler, oturum sonunda bir "Odak Skoru"na dönüştürülür. Sistem, düşük performans gözlemlenen derslerin zorluk katsayılarını otomatik olarak artırarak mola ve çalışma sürelerini kullanıcıyla özel yeniden optimize eder.

- Bulut Senkronizasyonu ve Mobil Erişim: Yerel makinede üretilen tüm metrikler, Google Firebase Firestore NoSQL veritabanına anlık olarak aktarılır. Mobil uygulama (Flutter), bu merkezi veritabanı üzerinden kullanıcının performans grafiklerine, sınav tarihlerine ve güncel çalışma planına uzaktan erişimini sağlar.

## 1.3 Dokümana Genel Bakış

Bu Yazılım Tasarım Dokümanı (SDD), SRS dokümanında belirtilen gereksinimlerin teknik olarak nasıl hayata geçirildiğini detaylandırmak üzere yapılandırılmıştır. Doküman; sistemin genel mimari katmanlarından (UI, İş Mantığı, Veri Erişim), veritabanı şemasına; multithreading kullanımından, göruntü işleme algoritmalarının matematiksel detaylarına kadar tüm tasarım kararlarını içerir.İlgili bölümlerde ayrıca, kullanıcı gizliliğini korumak adına kamera verilerinin neden ve nasıl sadece yerel cihazda işlendigi (Local-Only Processing) gibi kritik güvenlik ve etik tasarım ilkeleri de teknik gerekçeleriyle sunulmuştur. Doküman, geliştirme ekibi için bir uygulama rehberi niteligi taşidığı gibi, sistemin bakım yapılabilirliğini ve ölçeklenebilirliğini de dokümante etmeyi amaçlar.

## 2. İlgili Dokümanlar

## 2.1 Software Requirements Specification (SRS)

Software Requirements Specification (SRS) dokümanı, FocuSync sistemine ait fonksiyonel ve fonksiyonel olmayan gereksinimlerin tanımlandığı temel başvuru dokümanıdır. Bu dokümanda kullanıcı arayüzleri, donanım arayüzleri, yazılım arayüzleri, iletişim arayüzleri, kullanıcı giriş sistemi, ders yönetimi, program ve sınav yönetimi, odak oturumu yönetimi, kafa takibi ve odak skoru, beyaz liste kontrolü, adaptif zorluk güncelleme, istatistik ve raporlama ile mobil senkronizasyon gereksinimleri ayrntılı olarak belirtilmiştir. Bu Yazılım Tasarım Dokümanı (SDD), söz konusu gereksinimlerin mimari, modüler ve teknik düzeyde nasıl karşılandığını açıklamak amacıyla SRS dokümanı esas alınarak hazirlanmıştır.

## 2.2 Software Project Management Plan (SPMP)

Software Project Management Plan (SPMP), FocuSync projesinin geliştirme sürecinde izlenecek yönetim yaklaşımını, proje organizasyonunu, roller ve sorumlulukları, görev dağılımını, zaman çizelgesini ve teslimatları tanımlayan yönetim dokümanidır. SPMP dokümanında proje için çevik geliştirme yaklaşımı olarak Scrum modelinin benimsendiği, ekip üyelerinin göruntü işleme, algoritma geliştirme, mobil uygulama, masaüstü arayüz tasarımı ile veritabanı ve otomasyon gibi sorumluluk alanlarına ayrıldığı belirtilmiştir. Ayrıca masaüstü uygulama, mobil uygulama ve SRS, SDD, STD gibi temel proje teslimatları bu dokümanda tanımlanmıştır. SDD'de yer alan tasarım kararları ve modüler yapı, SPMP'de tanımlanan süreç modeli ve görev organizasyon ile uyumlu biçimde hazirlanmıştır.

## 2.3 Kullanilan Teknolojiler ve Harici Kaynaklar

FocuSync projesinin masaüstü uygulaması Python tabanlı olarak geliştirilmiş olup kullanıcı arayüzü katmanında PyQt6 kullanılmaktadır. Gerçek zamanlı kafa takibi ve dikkat analizi için OpenCV ve MediaPipe tabanlı göruntü işleme yaklaşımı benimsenmiştir. Aktif pencere ve süreç denetimine dayalı whitelist işlevleri için Windows işletim sistemi araçları ve süreç izleme bileşenleri kullanılmaktadır. Ayrıca OCR tabanlı ders ve sınav programı aktarımı için PDF işleme ve yapay zeka destekli belge çözümleme yaklaşımı kullanılmaktadır.

Sistemin veri yönetimi ve cihazlar arası senkronizasyon altyapısı Google Firebase Firestore üzerinde kurulmuştur. Mobil uygulama tarafında Flutter framework’ü ve Dart programlama dili kullanılmaktadır. Mobil istemci, masaüstü uygulamasıyla aynı bulut veritabanı üzerinde çalışmakta ve kullanıcı verilerine bu ortak altyapı üzerinden erişmektedir. Geliştirme sürecinde sürüm kontrolü için Git/GitHub kullanılmakta; proje kapsamında ayrica Firebase Firestore, OpenCV, MediaPipe ve ilgili resmi teknik dokümantasyonlardan harici kaynak olarak yararlanılmaktadır.

## 2.4 Referans Standartlar

FocuSync projesinde gereksinimlerin tanımlanması sürecinde IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications standardı referans alınmıştır. SRS dokümanında bu standart açık biçimde belirtilmiş olup, gereksinimlerin yapılandırılması ve numaralandırılması bu standarda uygun biçimde hazirlanmıştır. Buna ek olarak, SDD dokümanında kullanılan modüler tasarım yaklaşımı, gereksinim–tasarım ilişkisi ve izlenebilirlik mantığı da IEEE tabanlı yazılım dokümantasyon anlayışı ile uyumlu olacak şekilde düzenlenmiştir. Teknik başvuru kaynağı olarak Firebase Firestore dokümantasyonu da SRS içerisinde referans verilmiş kaynaklar arasında yer almaktadır.

## 3. Sistem Çapında Tasarım Kararlari

## 3.1 Genel Mimari Yaklaşım

FocuSync sistemi, ağır işlem yükü gerektiren bilgisayarlı görü ve işletim sistemi düzeyindeki denetim (Whitelist) operasyonlarını yerel makinede (Client) çözerken, veri yönetimi ve senkronizasyon süreçlerini bulut (Cloud) tabanlı yöneten "Kalın İstemci - Bulut Arka Uç" (Thick Client - Cloud Backend) mimarisi üzerine insa edilmiştir.

Bu mimari yaklaşımda:

- Ağır İş Yükü Yerelde İşlenir: OpenCV ile kafa takibi, aktif pencere dinleme ve OCR (Yapay Zeka destekli PDF okuma) gibi yüksek işlem gücü gerektiren görevler istemci makinede çalıştırılarak sunucu maliyetleri ve ağ gecikmeleri (latency) sifira indirilmiştir.

- Merkezi Bulut Senkronizasyonu: Yerelde üretilen özet veriler (Odak skoru, ihlal süreleri, ders ağırlıkları), cihazlar arası (Masaüstü ve Mobil) kesintisiz eşzamanlılık sağlamak amacıyla NoSQL tabanlı Google Firebase Firestore'a iletilir. Bu sayede sistem, "Tek Doğru Kaynağı" (Single Source of Truth) prensibiyle çalışır.

## 3.2 Katmanlı Yapı ve Modüler Tasarım Karari

Uygulamanın sürdürülebilirligini artırmak, kod tekrarını önlemek ve ekip ici paralel geliştirmeyi mümkün kılmak amacıyla katmanlı ve modüler bir mimari benimsenmiştir. Sistem mantıksal olarak üç ana katmana ayrılmıstir:

1. Sunum ve Arayüz Katmani (UI Layer): PyQt6 kullanılarak geliştirilen bu katman, yalnızca kullanıcı ile etkileşimi yönetir. (Örn: courses_page.py, schedule_page.py). Veri işleme veya veritabanı sorgulama mantığı bu katmandan kesinlikle soyutlanmıştır.

2. İş Mantığı Katmanı (Business Logic Layer): Uygulamanın beyni olan bu katman; kafa yönü hesaplama, adaptif zorluk belirleme algoritması ve OCR metin çözümleme gibi çekirdek servisleri barındırir.

3. Veri Erişim Katmanı (Data Access Layer - DAL): Veritabanı ile iletişim kuran tek ve yalıtılmış katmandır. Mimaride katı bir kural olarak "Gateway Pattern" (Geçit Tasarım Deseni) uygulanmıştır. Hiçbir arayüz veya iş mantığı modülü Firestore ile doğrudan iletişim kuramaz; tüm CRUD (Create, Read, Update, Delete) operasyonları merkezi DatabaseManager (db_manager.py) sınıfı üzerinden yetkilendirilerek gerçekleştirilir.

## 3.3 Masaüstü Uygulama Tasarım Kararlari

Masaüstü istemcisinin kararlı çalışması ve en iyi kullanıcı deneyimini (UX) sunması için aşağıdaki kritik mimari tasarım kararlari alınmıştır:

- Çoklu İş Parçacığı (Multithreading) Mimarisi: PyQt6 gibi GUI (Grafiksel Kullanıcı Arayüzü) kütüphanelerinde ana iş parçacığının (Main Thread) bloklanması uygulamanın donmasına ("Not Responding") yol açar. Bu kilitlenmeyi önlemek için; OCR taramaları (QThread tabanlı OCRWorker), OpenCV kafa takibi döngüleri ve Whitelist aktif pencere dinleyicileri ana arayüzden koparılarak asenkron arka plan işçileri (Background Threads) olarak tasarlanmıştır.

- Tek Sayfa Uygulama (SPA) Benzetimi ve QStackedWidget: Menüler arası geçişlerde yeni pencerelerin (Window) açılıp kapanması bellek sızintılarına ve görsel gecikmelere yol açar. Bunu önlemek adına main_window.py içerisinde QStackedWidget yapısı kullanılmıştır. Tüm modüller tek bir ana pencere (MainWindow) üzerine katmanlar halinde önceden yüklenir ve menü etkileşimlerinde sadece ilgili katmanın görünürlüğü değiştirilir. Bu karar, geçişleri anlık hale getirir ve RAM kullanımını optimize eder.

- Çevrimdışı (Offline) Tolerans ve Hata Yönetimi: Uygulamanın ağ kesintilerinde çökmemesi için defansif programlama kararları alınmıştır. Herhangi bir okuma/yazma işleminden önce Düşük Seviyeli Soket (Socket) testleri ile internet durumu denetlenir. Veritabanına yazılamayan veya eksik olan veriler için anlık hata yönetim mekanizmaları devreye girerek veri kirliliği engellenir.

## 3.4 Mobil Uygulama Tasarım Kararlari

Mobil uygulama, Flutter framework'ü kullanılarak geliştirilmiştir. Bu tercih, tek bir kod tabanından hem Android hem iOS platformlarına derleme yapilabilmesini sağlamakta ve geliştirme sürecini kısaltmaktadir. Programlama dili Dart'tir.

## Veritabanı ve Senkronizasyon Mimarisi

Mobil uygulama, masaüstü uygulamasıyla aynı Firebase Firestore bulut veritabanı üzerinde çalışmaktadır. Bu tasarım kararının temel gerekçesi, platform bağımsız gerçek zamanlı veri erişimidir. Masaüstü uygulaması bir veriyi Firestore'a yazdığında mobil uygulama aynı koleksiyonu sorgulayarak güncel veriye ulaşır. İki platform arasında ayrı bir senkronizasyon servisi ya da API katmanı bulunmamaktadır, senkronizasyon doğrudan ortak veritabanı üzerinden sağlanır.

## Kimlik Doğrulama Yaklaşımı

Firebase Authentication SDK kullanılmamıştır. Bunun yerine özel (custom) bir kimlik doğrulama mekanizması tercih edilmiştir. Kullanıcı kimlik bilgileri doğrudan Firestore'daki Users koleksiyonunda sorgulanmakta ve başarılı giriş sonrasında dönen userID değeri cihazın yerel deposuna (SharedPreferences) kaydedilmektedir. Uygulama her açılışta bu yerel kaydı kontrol ederek kullanıcının oturumunu yeniden doğrular, kayıt mevcutsa giriş ekranı atlanır ve doğrudan ana sayfaya yönlendirme yapılır.

## Ağ Bağlantısı Yönetimi

Tüm uygulama ekranları NetworkWrapper adındaki bileşenle kuşatılır. Bu bileşen MaterialApp.builder parametresine bağlanmış olup uygulama içindeki tüm sayfaları otomatik olarak kapsar. connectivity_plus paketi aracılığıyla bağlantı durumunu anlık olarak dinler ve internet bağlantısı kesildiğinde ekranın üst kısmında AnimatedPositioned ile animasyonlu bir uyarı bandı gösterir. Giriş (LoginScreen) ve kayıt (RegisterScreen) ekranları ek olarak kendi yerel bağlantı kontrollerini de yürütmekte ve bağlantı yokken ilgili butonları devre dışı birakmaktadır. Bu iki katmanlı yaklaşım, kullanıcının bağlantısız durumda işlem başlatmasını hem görsel hem de fonksiyonel olarak engeller.

## Veri Erişim Katmanı

Tüm Firestore okuma ve yazma işlemleri DatabaseManager sınıfı üzerinden yürütülmektedir. Ekranlar doğrudan Firestore API'sine erişemez. Bu merkezi yapı, veri erişim mantığın UI katmanından ayırır ve bakım kolaylığı sağlar.

## Oturum Yönetimi

Kullanıcı oturumu SharedPreferences ile cihaz yerelinde saklanmaktadır. Uygulama kapansa dahi user_ID değeri korunur ve kullanıcınin tekrar giriş yapması gerekmez. Çıkış işlemi bu yerel kaydı silerek oturumu sonlandırır.

## Performans İzleme Modülü

Bu ekran, kullanıcınin geçmiş odak oturumlarını (FocusSessions koleksiyonu) görselleştiren bir performans panosu sunar. fl_chart kütüphanesi kullanılarak çizgi grafik ve özet istatistik kartları (toplam seans, ortalama skor, en yüksek skor) gösterilmektedir. Ekrana HomePage üst çubuğundaki grafik simgesi aracılığıyla erişilmektedir.

## Profil Yönetimi Modülü

ProfileScreen ekranı, kullanıcının ad, soyad, okul bilgilerini düzenlemesine ve şifre değişikliği yapmasına olanak tanır. E-posta alanı salt okunur (read-only) olarak sunulmakta ve şifre güncelmesi mevcut şifre doğrulamasına tabi tutulmaktadır.

## 3.5 Veritabanı Tasarım Kararlari

FocuSync projesi, adaptif çalışma algoritmalarının ürettiği dinamik verileri ve anlık sensör (kamera) istatistiklerini gecikmesiz işleyebilmek amacıyla, geleneksel ilişkisel veritabanları yerine bulut tabanlı bir NoSQL çözümü olan Google Firebase Firestore üzerinde insa edilmiştir. Veritabanı mimarisi, esneklik, güvenlik ve veri buttünlüğü temel alınarak üç ana tasarım kararı etrafında sekillendirilmiştir.

## 3.5.1 Mimari Tercih ve Merkezi Erişim (Gateway) Pattern

Sistem, hiyerarşik Koleksiyon (Collection) ve Doküman (Document) yapısına dayanır. Uygulamanın modülerliğini artırmak ve güvenlik açıklarını önlemek amacıyla Merkezi Erişim (Gateway) Mimarisi benimsenmiştir.

- Uygulama içerisindeki hiçbir modül (arayüzler, yapay zeka veya kamera) veritabanı ile doğrudan iletişim kuramaz.

- Tüm veri okuma, yazma ve güncelleme (CRUD) işlemleri sadece izole edilmiş DatabaseManager (db_manager.py) sınıfı üzerinden gerçekleştirilir. Bu yapı, veritabanı sorgularının tek bir merkezden yönetilmesini ve kod tekrarının önlenmesini sağlar.

## 3.5.2 Güvenlik ve Yetkilendirme Stratejisi

Masaüstü uygulamasının geliştirme süreçlerindeki yetki bariyerlerini aşmak için standart istemci doğrulaması yerine Private Key (Admin SDK) yöntemi tercih edilmiştir.

- Tam Yetki ve İzolasyon: Firebase veritabanı dış dünyaya ve standart HTTP isteklerine tamamen kapatılmıştır. Sisteme sadece yerel ortamda şifrenmiş olarak barındırılan serviceAccountKey.json dosyasına sahip olan istemciler (Uygulama) erişebilir.

- Bağlantı Kontrolü: Veritabanının bulut tabanlı olması sebebiyle, uygulamanın çökmesini engellemek adına tüm okuma/yazma işlemleri öncesinde düşük seviyeli soket (socket) bağlantı testleri yapılarak ağ durumu (Offline/Online) denetlenir.

## 3.5.3 Veri Bütünlüğü ve Koruma Mekanizmaları

NoSQL esnekliğini kontrol altında tutmak ve kullanıcı verilerinin birbirine karışmasını engellemek için sistem düzeyinde katı kurallar tanımlanmıştır.

- Bileşik Anahtar (Composite Key) Mimarisi: Dersler veya programlar gibi eşsiz olması gereken koleksiyonlarda doküman kimlikleri (Doc ID), rastgele UUID'ler yerine mantıksal birleşimlerle (Örn: {user_id}_{course_id}) oluşturulur. Bu mimari, farklı kullanıcıların aynı verileri yüklemesi durumunda oluşabilecek çakışmaları (collision) donanımsal olarak engeller.

- Yumuşak Silme (Soft Delete) Stratejisi: Sistemin geçmişe dönük makine öğrenmesi analizlerinin (StudyPlans, FocusSessions) bozulmaması için veriler fiziksel olarak

kalıcı sekilde silinmez (Hard Delete). Bunun yerine, ilgili verinin is_active bayrağı değiştirilerek veri arayüzden gizlenir ancak algoritmik referans buttünlüğü korunur.

## 3.6 Gerçek Zamanlı İşleme ve Multithreading Kararları

## 3.6.1 Göruntü İşleme ve Arayüz Optimizasyonu (Kafa Takibi Modülü):

FocuSync sisteminde, gerçek zamanlı kamera akışının alınması ve MediaPipe/OpenCV ile işlenmesi yüksek işlemci (CPU) gücü gerektirmektedir. Bu ağır matematiksel operasyonların uygulamanın Ana Arayüz (Main UI Thread) işleyişini dondurmasını (freeze) engellemek amacıyla katı bir Multithreading (Çoklu İş Parçacığı) mimarisi benimsenmiştir.

- Asenkron İş Parçacığı (QThread) Mimarisi: Göruntü işleme ve açı hesaplama (solvePnP) döngüleri, PyQt6'nın QThread sınıfindan türetilen bağlmsız bir HeadTracker sınıfı içerisinde izole edilmiştir. Bu tasarım kararı, arka planda saniyede onlarca kare işlenirken bile arayüzdeki dijital zamanlayıcının (QTimer) ve butonların kesintisiz ve akıcı çalışmasını güvence altına alır.

- Signal-Slot (Sinyal-Yuva) Tabanlı Haberleşme: Farklı iş parçacıkları (Thread) arasında doğrudan değişken erişiminin sebep olabileceği yarış durumlarını (Race Conditions) ve bellek hatalarını önlemek için PyQt'nin yerleşik Sinyal-Yuva mekanizması kullanılmıştır. İşlenen kamera kareleri (frame_processed), anlık odak durumu değişimleri (focus_status_changed) ve oturum sonu veri paketleri (session_completed) sadece bu sinyaller aracılığıyla asenkron olarak Ana Arayüze iletilir.

- Kare Hızı (FPS) Sınırlandırması (Throttling): İşlemci üzerindeki gereksiz termal yükü hafifletmek ve performansı optimize etmek amacıyla, kamera okuma döngüsü serbest bırakılmamış; time.sleep algoritmaları kullanılarak saniyede maksimum 15 kare (15 FPS) işleyecek sekilde sınırlandırılmıştır. Bu oran, gerçek zamanlı odak tespiti için yeterli hassasiyeti sağlarken sistem kaynaklarını verimli kullanır.

## 3.6.2 Aktif Uygulama İzleme ve Win32 API İzolasyonu (Whitelist Modülü):

Odak seansı boyunca kullanıcının hangi uygulamalarda gezindiğini tespit etmek, işletim sistemi çekirdeği ile (OS Kernel) sürekli haberleşmeyi gerektirir. win32gui ve psutil gibi kütüphanelerle saniyede bir yapılan bu donanım/sistem kesintileri (interrupts) arayüzde takılmalara yol açmaması için bağımsız bir iş parçacığına taşınmıştir.

- MonitorWorker Mimarisi: QThread sınıffindan türetilen MonitorWorker, kendi while döngüsü icerisinde çalışır. İşlemciyi yormamak adına, bekleme süreleri tek ve uzun bir blok yerine msleep(200) (200 milisaniye) parçalarına bölünerek uyutulur; bu sayede iş parçacıgı dışarından gelen "durdur" komutlarına (stop) anında tepki verebilir.

- Güvenli Durum Aktarımı: İhlal durumu değiştiğinde (violation_found veya no_violation), worker thread doğrudan arayüz müdahale etmez; sinyaller aracılığıyla ana iş parçacığına (Main Thread) mesaj gönderir, görsel ve işitsel uyariların patlatılması (Pop-up, Ses) güvenli bir şekilde Ana Arayüz tarafindan üstlenilir.

## 3.6.3 Asenkron OCR ve Yapay Zeka İstekleri (Program/Sınav Modülü):

Kullanıcıların PDF veya görsel olarak yüklediği ders programlarının yapay zeka (Google Gemini AI) ile çözümlenmesi süreci, ağ gecikmelerine (Network Latency) ve dosya boyutu limitlerine bağlı olarak saniyelerce sürebilen senkron (bloklayıcı) bir işlemdir.

- Arka Plan İşcisi (OCRWorker): Bu ağır yük, Ana Arayüzü kilitleyip "Uygulama Yanıt Vermiyor" (ANR - Application Not Responding) hatasına düşürmemek için OCRWorker adında ayrı bir QThread içerisine hapsedilmiştir.

- Görsel Geri Bildirim ve Kilit mekanizmasi: Dosya yüklendiği ana arayüzdeki yükleme butonu deaktif edilip "Lütfen bekleyin..." durumuna çekilir. Arka plandaki OCRWorker dosya analizi ve yapay zeka API haberleşmesini bitirdiğinde finished_signal sinyalini tetikler; bu sinyal, ayrıştırılmış JSON verisini veya hata durumunu (success, doc_type, result_data) güvenli bir şekilde arayüze taşıyarak dinamik tabloların (QTableWidget) doldurulmasını sağlar.

## 3.7 Güvenlik ve Kimlik Doğrulama Tasarımı

Sistemde üçüncü parti kimlik doğrulama servisleri (örneğin Firebase Authentication) kullanılmamış olup özel bir kimlik doğrulama mimarisi kurgulanmıstır. Sistem güvenliği kriptografik şifreleme ve istemci tabanlı oturum yönetimi olmak üzere iki ana katmanda sağlanmaktadır:

## 3.7.1 Kriptografik Şifreleme ve Veri Saklama

Kullanıcı güvenliğini en kritik katmanı olan şifre yönetimi, veritabanında plaintext şeklinde saklanmasını engelleyen Salted Hash mimarisi ile tasarlanmıştır.

Algoritma Tercihi: Şifre hashleme işlemi için kaba kuvvet (brute force) saldırilarına karşı dirençli olan PBKDF2 (Password-Based Key Derivation Function 2) algoritması HMAC-SHA256 hash fonksiyonu ile birlikte kullanılmaktadır.

Kayıt (Sign Up) Akışı: Yeni bir kullanıcı oluşturulduğunda DatabaseManager sınıfı tarafından bu kullanıcıya özel ve rastgele bir salt değeri üretilir. Kullanıcının belirlediği şifre bu tuz değeriyle birleştirilerek PBKDF2 algoritmasına verilir.

Veritabanı Şeması: Firestore üzerindeki Users koleksiyonuna şifrenin kendisi yerine yalnızca hashedPassword ve salt alanları tutulur. Bu yaklaşım, veritabanı sizintısı durumunda rainbow table saldırilarını yapısal olarak imkansız kılar.

Giriş (Sign In) Akışı: Giriş talebinde bulunulduğunda sistem e-posta adresi üzerinden kullanıcıın salt değerini veritabanından okur. Kullanıcıın o an girdiği şifre bu salt ile anlık olarak PBKDF2 algoritmasından geçirilir. Üretilen yeni özet değer veritabanındaki hashedPassword değeri ile birebir eşleşirse kimlik doğrulanmış kabul edilir.

## 3.7.2 Oturum Güvenliği ve Kalıcılık

Sistem, durumsuz bir arka uç yapısı üzerinde çalıştığı için oturum kalıcılığı mobil uygulama tarafından yönetilmektedir.

Başarılı bir kimlik doğrulamasının ardından kullanıcıının benzersiz userID değeri cihazın yerel deposuna (SharedPreferences) yazılır. Uygulama her başlatıldığında bu yerel anahtar kontrol edilir. "Çıkış Yap" (Sign Out) işlemi tetiklendiğinde yerel depodaki userID anahtarı kalıcı olarak silinerek oturum güvenli bir sekilde sonlandırılır.

## 3.8 Gizlilik ve Kamera Verisi İşleme Yaklaşımı

## 3.8.1 Yerel İşleme Ilkesi (Local-Only Processing)

FocuSync sisteminde gizlilik, "verinin kaynağında işlenmesi" prensibine dayanır. Kameradan alınan ham görüntü kareleri, hiçbir aşamada uzak bir sunucuya (Cloud) gönderilmez. Tüm görüntü işleme operasyonları kullanıcınin yerel cihazındaki işlemci (CPU) ve bellek üzerinde gerçekleştirilir.

## 3.8.2 Göruntü Verisinin Kalıcılığı

Sistem, kameradan gelen görüntüleri kalıcı olarak disk üzerine kaydetmez veya video kaydı almaz. cv2.VideoCapture ile bellek üzerine alınan her bir kare, MediaPipe Landmarker tarafindan analiz edildikten ve gerekli sayısal veriler (koordinatlar) üretildikten hemen sonra bellekten (RAM) temizlenir. Oturum sonunda veritabanına sadece bu analizlerden elde edilen istatistiksel sonuçlar (skorlar ve süreler) aktarılır.

## 3.8.3 Sayısal Veriye Dönüştürme (Anonymization)

Kamera verisi işleme süreci, kişisel görüntüyü anonim matematiksel verilere dönüştürme odaklıdır:

- Landmark Katmani: Görüntüden sadece yüz hatlarını temsil eden koordinat noktaları (X, Y, Z) çıkarılır.

- Açısal Veri: Bu koordinatlar üzerinden Pitch, Yaw ve Roll açılar hesaplanır.

- Sonuç: Veritabanına kaydedilen veri "bir insan yüzü görüntüsü" değil, "bir zaman dilimindeki açısal sapma değeridir". Bu sayede, veritabanına erişimi olan yetkisiz bir kişi dahi kullanıcınin fiziksel görüntüsüne ulaşamaz.

## 3.8.4 Kullanıcı Farkindalığı ve Kontrolü

Gizlilik tasarım, kullanıcıya şeffaf bir kontrol mekanizması sunar:

- Görsel Göstergeler: Arayüz üzerinde kameranın aktif olup olmadığını belirten canlı bir durum göstergesi (cam_status_lbl) bulunur.

- Canlı Önizleme: Kullanıcı, kamera tarafından tam olarak neyin görüldüğünü arayüzdeki canlı önizleme kutusundan takip edebilir, bu sayede arka plan gizliliğini kendisi denetleyebilir.

- Donanimsal Kesinti: Oturum bitirildiği anda (tracker.stop()), kamera donanımı işletim sistemi seviyesinde serbest bırakılır ve veri akışı anında kesilir.

## 3.8.5 Üçuncü Taraf Kütüphanelerin Güvenliği

Görüntü işleme motoru olarak kullanılan Google MediaPipe, "on-device ML" (cihaz üstü makine öğrenmesi) kütüphanesidir. Bu kütüphane, veriyi analiz etmek için harici bir bulut servisine ihtiyaç duymaz; tüm model (face_landmarker.task) yerel olarak yüklenir ve çalıştırılır.

## 3.9 Hata Yönetimi ve Dayanıklılik Tasarımı:

## 3.9.1 Donanım Hataları ve İstisna Yönetimi

FocuSync, kamera ve mikrofon gibi dış donanımlara bağımlı bir sistem olduğu için "Graceful Degradation" (Kademeli Hizmet Düşümü) prensibiyle tasarlanmıştır.

- Kamera Denetimi: Odak seansı başlatılmadan önce donanım seviyesinde (cv2.VideoCapture) bir ön kontrol yapılır. Kamera bulunamaması veya başka bir uygulama tarafından meşgul edilmesi durumunda sistem seansı başlatmaz ve kullanıcı bilgilendirerek "donanım kaynaklı çökme" riskini ortadan kaldirir.

- Yüz Tespiti Kesintileri: Seans sırasında yüzün kameradan çıkması bir "sistem hatası" olarak değil, bir "odak ihlali" olarak kabul edilir ve face_missing sinyali üzerinden yönetilir; böylece uygulama akışı bozulmadan devam eder.

## 3.9.2 Ağ Bağlantısı ve Veri Tutarlılığı (Offline/Online Resilience)

Bulut tabanlı bir veritabanı (Firebase) kullanıldığı için internet kesintileri sistemin en büyük risk faktörüdür.

- Ağ Durum Denetimi: Herhangi bir kritik yazma (set, update) veya okuma işlemi öncesinde, düşük seviyeli soket bağlantılar (Google DNS 8.8.8.8) üzerinden internet varlığı denetlenir.

- Hata Yakalama (Try-Except): Veritabanı işlemleri (add_focus_session, save_whitelist_session) izolasyon blokları içine alınmıştır. Internet kopsa dahi

uygulama çökmez; seans verileri yerelde muhafaza edilir ve kullanıcıya "Bağlantı Hatası" uyarısı verilerek sistemin tutarlı kalması sağlanır.

## 3.9.3 Yapay Zeka (OCR) Hata Toleransi

OCR modülünde Google Gemini sunucularından kaynaklı gecikmeler veya yanlış belge yüklenmesi durumlarına karşı "Hata Toleranslı Çözümleme" uygulanır:

- Yeniden Deneme (Retry Logic): Sunucu taraflı geçici yoğunluklarda (503 Service Unavailable) sistem anında pes etmek yerine, belirlenen zaman aşımı süreleriyle işlemi arka planda tekrarlar.

- Belge Tipi Doğrulaması: Yanlış belge yüklenmesi durumunda AI sınırflandırıcıı bu durumu tespit eder ve veritabanına kirli veri yazılmasını engelleyerek süreci en başa (Dosya Yükleme Paneli) döndürür.

## 4. FocuSync Sisteminin Yapısal Tasarımı

FocuSync, yapay zeka destekli yerel işlem gücünü (On-Device Processing) bulut tabanlı bir veritabanı (BaaS - Backend as a Service) ile birleştiren Kalın İstemci (Fat Client) mimarisine sahiptir. Göruntü işleme, OCR ve işletim sistemi denetimleri gibi ağır hesaplama gerektiren işlemler istemci bilgisayarında yerel olarak yapılırken; veri kalıcılığı ve senkronizasyon Firebase üzerinden sağlanır.

## 4.1 Sistem Bileşenleri

Sistem modüler ve katmanlı bir yapida tasarlanmış olup şu ana bileşenlerden oluşmaktadir:

- Sunum Katmani (UI & View): PyQt6 kütüphanesi üzerine inşa edilmiştir. Kullanıcı ile etkileşime girer, asenkron sinyalleri yakalar ve verileri görselleştirir (main_window.py, focus_page.py, schedule_page.py vb.).

- Kamera ve Görüntü İşleme Motoru (head_tracker.py): Cihaz kamerasından aldığı RGB kareleri Google MediaPipe ve OpenCV kullanarak işler, matematiksel kafa açısı (Pitch, Yaw, Roll) ve odak skoru üretir.

- İşletim Sistemi Denetleyicisi (whitelist_functionality.py): Windows API'lerini (win32gui, psutil) kullanarak cihazdaki aktif pencereleri ve süreçleri (process) dinler, izin verilmeyen uygulamalari tespit eder.

- Yapay Zeka ve OCR Motoru (ocr_manager.py): PDF ve görsellerdeki karmaşık ders/sınav programlarını pdfplumber ile ayrıştırır, yapısal olmayan metni Google Gemini AI API'sine göndererek JSON formatında anlamlı veri setlerine dönüştürür.

- Veri Erişim Geçidi (db_manager.py): Sistemin Firestore veritabanı ile konuşan tek yetkili (Singleton benzeri) iletişim merkezidir (Gateway Pattern).

## 4.2 Üst Düzey Mimari Diyagramı (Açıklamalı)

FocuSync mimarisi, mantüksal olarak Katmanlı Mimari (Layered Architecture) ve Olay Yönelimli Mimari (Event-Driven Architecture) prensiplerini birleştirir:

- En Üst Katman (İstemci / Kullanıcı Arayüzü): Kullanıcının doğrudan etkileşim kurduğu tüm sayfa (Page) ve pencere (Window) bileşenleri.

- Orta Katman (Arka Plan İşçileri - Workers): Ana iş parçacıgını (Main Thread) dondurmamak için QThread üzerinde çalışan asenkron işleyiciler (HeadTracker, MonitorWorker, OCRWorker). Bu katman, donanim kaynaklarıyla (Kamera, CPU, Disk) ve dış API'lerle (Gemini) doğrudan temas kurar.

- En Alt Katman (Veri & Bulut): DatabaseManager sınıfı üzerinden ulaşılan Firebase Firestore. Tüm durum değişiklikleri ve istatistikler bu katmanda son bulur.

## 4.3 Bileşenler Arası İlişkiler

Sistem bileşenleri, birbirlerine sıkı sıkıya bağlı olmak (Tight Coupling) yerine Sinyal-Yuva (Signal-Slot) mekanizması ile Gevşek Bağlı (Loosely Coupled) bir ilişki kurar:

- focus_page.py (UI), HeadTracker ve WhitelistLogic modüllerinin doğrudan içine müdahale etmez; onları başlatır ve ürettikleri sinyalleri (focus_status_changed, violation_found) dinleyerek ekrandaki UI bileşenlerini günceller.

- Aynı sekilde dış kaynaklı işlemler (ocr_manager.py'nin AI sunucularından yanıt beklemesi), schedule_page.py içindeki OCRWorker sinyali (finished_signal) ile UI katmanına iletilir.

- Hiçbir arayüz (View) veya İşci (Worker) doğrudan veritabanına sorgu atamaz; veriler hazirlanır ve db_manager.py'deki fonksiyonlara parametre olarak geçilir. Bu sayede tüm veritabanı kuralları (Örn: prepare_focus_session_id) tek bir noktadan yönetilir.

## 4.4 Veri Akışı Genel Yapısı

Sistemde yoğun hesaplama ve dış iletişim gerektiren üç farklı ana veri boru hattı (Data Pipeline) bulunmaktadır:

## A. Belge Çözümleme Akışı (OCR Pipeline):

- Kullanıcı schedule_page.py veya exams_page.py üzerinden bir PDF dosyası yükler.

- OCRManager dosyayı alır, pdfplumber ile içindeki ham metinleri çıkartır.

- Ham metin, özel hazirlanmış Promtlar (istemler) ve RegEx kurallar ile birlikte Google Gemini AI sunucularına gönderilir.

- Gemini AI, belgenin türünü sınırflandırır (Sınav veya Program) ve ''''json` etiketiyle yapılandırılmış bir veri döndürür.

- Arayüz bu JSON dizisini tabloya (QTableWidget) aktarır; onay alındığında veriler Schedules veya Exams koleksiyonlarına işlenir.

## B. Gerçek Zamanlı Kafa Takibi Akışı:

- cv2 üzerinden 15 FPS hızında alınan RGB kareler FaceLandmarker'a beslenir.

- Yüzdeki 478 landmark noktasından 6 kritik olanı (gözler, burun, çene kenarlari) solvePnP algoritmasıyla 3D vektörlere dönüştürülür.

- Hesaplanan Pitch (Yukarı/Aşağı) ve Yaw (Sağa/Sola) açılar, kalibrasyon referansıyla karşılastırılır. Limit aşımı varsa (Debounce filtresinden geçtikten sonra) durum "Odak Bozuldu" olarak işaretlenir.

- Oturum sonunda toplam odaklı kalınan süre focus_score olarak hesaplanir ve FocusSessions tablosuna benzersiz bir ID ile kaydedilir.

## C. Beyaz Liste (Whitelist) İhlal Akışı:

- MonitorWorker saniyede bir Windows API üzerinden aktif pencere sürecinin ismini alır (psutil.Process(pid).name()).

- Alınan süreç adı, önbellekteki İzin Verilenler (_whitelist), Sistem süreçleri (SYSTEM_EXES) ve Uygulamanın kendisi (SELF_EXES) ile karşılastırılır.

- Eşleşme yoksa süreç bir violation (ihlal) olarak loglanır ve _total_violation_seconds sayacı artırılır.

- Oturum sonunda bu loglar JSON dizisi haline getirilerek o anki odak seansının ID'si (focus_session_id) ile birlikte WhitelistSessions koleksiyonuna gönderilir.

## 4.5 Arayüz Tasarımı

FocuSync kullanıcı arayüzü, PyQt6 tabanlı masaüstü uygulama mimarisi üzerinde tasarlanmış olup, sistem modülleri tek ana pencere altında sidebar ve QStackedWidget yapısı kullanılarak buttünleşik biçimde sunulmaktadır. Bu tasarım sayesinde Dashboard, Sabit Ders Programı, Notlar, Önerilen Ders Programı, Dersler, Odak Modu, Beyaz Liste ve Profil sayfaları arasında tutarlı ve sade bir gezinme yapısı sağlanmıştır. Arayüz tasarımında koyu tema, yüksek kontrast, ortak renk dili ve merkezi stil yönetimi benimsenmiş; butonlar, giriş alanları, kart yapıları ve gezinme bileşenleri tüm sistemde standartlaştırılmıştır. Böylece arayüz, kullanılabilirlik, görsel tutarlılık ve modülerlik açısından sürdürülebilir bir yapı sunmaktadır.

## 5. Ayrintili Tasarım

## 5.1 Kullanıcı Giriş ve Profil Modülü

## 5.1.1 Amaç

Bu modül, FocuSync sisteminin güvenlik katmanını ve kişiselleştirme altyapısını oluşturur. Temel amacı, kullanıcıların sisteme güvenli bir şekilde erişim sağlamalarını, oturumlarını yönetmelerini ve profil bilgilerini (isim, soyad, okul bilgisi, şifre yönetimi vb.) sisteme tanımlayarak uygulamada kullanılacak kullanıcı profilinin yönetimini sağlar.

## 5.1.2 Girdi / Çiktular

Sistem, veri alışverişini iki ana arayüz (LoginWindow ve ProfilePage) üzerinden yönetir:

- Giriş Girdileri: Kullanıcı e-posta adresi (QLineEdit) ve parola (QLineEdit - PasswordEchoOn).

- Profil Girdileri: Kullanıcının adı, soyadı, eğitim gördüğü kurum bilgisi ve şifre değişimi için çift doğrulamalı yeni şifre giriş alanları

- Çiktilar: Başarılı doğrulamada kullanıcıya özel oturum kimliği (user_id), ana pencereye (dashboard, istatistik gösterim ekranı) yönlendirme ve profil ekranında verilerin anlık görsel geri bildirimi.

## 5.1.3 Kimlik Doğrulama ve İşleyiş Mantığı

FocuSync, harici kimlik doğrulama servisleri yerine veri güvenliğini doğrudan Firestore üzerinden sağlayan özel bir doğrulama mantığı yürütür:

- Oturum Başlatma: LoginWindow üzerinden alınan bilgiler, DatabaseManager.login_user fonksiyonuna iletilir.

- Kimlik Eşleştirme: DatabaseManager, Users koleksiyonunda e-posta adresiyle eşleşen kullanıcı dokümanını arar. Doküman bulunduğunda veritabanından kullanıcıya özel salt değeri okunur. Kullanıcıının arayüzden girdigi düz metin şifre bu salt değeri kullanılarak anlık olarak PBKDF2 algoritmasından geçirilir. Üretilen yeni hash, veritabanında saklanan şifre özeti ile birebir eşleşirse doğrulama başarılı kabul edilir.

- Session (Oturum) Yönetimi: Doğrulama başarılışsa, kullanıcı dökümanındaki benzersiz kimlik (doc_id) global bir değişken olan user_id'ye atanır ve uygulamanın MainWindow bileşeni bu kimlik ile başlatılır.

- Profil Güncelleme: ProfilePage üzerinden yapılan değişiklikler, mevcut user_id referans alınarak Firestore üzerindeki ilgili kullanıcı dökümanına anlık olarak yansıtılır.

## 5.1.4 Hata Durumlari

Modül, kullanıcı hatalarını ve ağ problemlerini önlemek için şu denetimleri uygular:

- Eksik Veri Denetimi: Giriş veya kayıt sırasında herhangi bir alanın boş bırakılması durumunda işlem durdurulur ve kullanıcıya QMessageBox aracılığıyla uyarı verilir.

- Hatalı Kimlik Bilgisi: Kullanıcı adı veya parolanın eşleşmemesi durumunda, güvenlik gereği spesifik bir hata detayı verilmeden "Hatalı Giriş" uyarısı yapılır.

- Bağlantı Kesintileri: Veritabanı etkileşimi öncesinde ağ kontrolü yapılır; Google servislerine erişim sağlanamıyorsa "İInternet Bağlantısı Yok" uyarısı ile sistemin kararsız çalışması engellenir.

## 5.1.5 Veritabanı Ekkileşimi

Tüm veriler, Firebase Firestore üzerindeki Users koleksiyonunda asenkron olarak işlenir:

- Sorgulama (Read): Giriş sırasında e-posta tabanlı arama ve profil sayfasında mevcut bilgilerin çekilmesi.

- Güncelleme (Update): update_user_profile fonksiyonu ile kullanıcının adı, soyadı, okulu ve şifre değişimi varsa ilgili alanların güncellenmesi

- Veri Bütünlüğü: Profil bilgilerinde yapılan bir değişiklik, sistemdeki diğer modülleri (Dersler, Çalışma Planları) etkilemez; diğer modüller users koleksiyonundaki ilgili dokümanın benzersiz doküman adı ile eşleştirip bahsedilen bilgileri saklanan ilgili kullanıcıya erişimi bu şekilde sağlar. İlgili users koleksiyonundaki doküman, veri yönetimi açısından kullanıcılara ait en üst yapdır ve diğer tüm koleksiyonlardaki dokümanlar user_id ile bahsedilen en üst yapıyı işaretler. Bu sayede ilgili veriler ilgili kullanıcılar için saklanır.

## 5.2 Ders Yönetimi Modülü

## 5.2.1 Amaç

Ders Yönetimi Modülü, kullanıcınin sorumlu olduğu akademik dersleri sisteme tanımladığı, güncelledigi, bu derslere ait algoritmik kısıtlamaları (çalışma hedefleri, zorluk dereceleri) belirledigi ve bu derslere ait bilgilerin (derse ait sınav notları ve bu sınavların ağırlıkları, güncel not durumu) gösterildigi temel konfigürasyon merkezidir. Bu modülün ana işlevi, FocuSync'in dinamik çalışma planı üretici algoritması için gerekli olan yapısal meta veriyi (metadata) hatasız ve tutarlı bir şekilde toplamaktır

## 5.2.2 Girdi / Çıktılar

Modülün grafiksel kullanıcı arayüzü (GUI), kullanıcı deneyimini optimize etmek amacıyla "Veri Giriş Formu" ve "Dinamik Kart Görünümü (FlowLayout)" olmak üzere iki ana yatay panelden (Splitter) oluşur.

- Girdi Bileşenleri: Ders kodu (QLineEdit), ders adı, haftalık ders saati (QSpinBox), hedef not (QSpinBox) ve algoritma için öncelik belirleyen zorluk seviyesi ayarlayıcıı (QSlider). Ayrıca Vize, Final, Proje vb. sınav türlerinin ağırlık katsayılarını toplayan dinamik bir sözlük giriş alanı.

- Çiktı Bileşenleri: Sisteme kaydedilen her aktif ders, arayüzde özelleştirilmiş bir görsel kart (Course Card) olarak listelenir. Bu kartlar dersin temel bilgilerini (kod, ad, hedef not, zorluk seviyesi) ve yaklaşan sınav tarihlerini anlık olarak görselleştirir.

## 5.2.3 Temel İş Süreçleri (CRUD Operasyonları)

Sistem, veritabanı ile uygulama arayüzü arasındaki veri akışını şu dört operasyonla yönetir:

- Create & Update (Upsert Mimarisi): Sistem, yeni ders ekleme ve mevcut dersi güncelleme işlemleri için tek bir fonksiyonel yol (save_course) izler. Firestore üzerinde set(data, merge=True) metodu kullanılarak "Upsert" mantığı işletilir. Eğer girilen ders kodu ile eşleşen bir döküman yoksa yeni bir kayıt oluşturulur; eğer varsa mevcut döküman veri kaybı yaşanmadan güncellenir. Bu mimari, veri tekrarın önler.

- Read (Veri Okuma ve Filtreleme): db_manager, veritabanı seviyesinde herhangi bir filtreleme yapmadan, ilgili kullanıcıya ait tüm ders dökümanlarını (arşivlenmiş olanlar dahil) toplu olarak çeker. Veri işleme yükü uygulama katmanına bırakılmıştır; arayüz motoru gelen listedeki is_active bayrağını kontrol eder ve aktif olan ve aktif olmayan dersler birbirinden gösterimde ayrılır.

- Delete (Yumuşak Silme / Soft Delete): Geçmiş çalışma oturumlarının ve sınav takvimlerinin referans buttünlüğünü korumak için fiziksel silme (Hard Delete) uygulanmaz. Bunun yerine ilgili ders dökümanının is_active alanı false değerineçekilir. Böylece ders arayüzde aktif olmayan alana taşınırken, ilişkili veritabanı kayıtları sistemde saklanmaya devam eder.

## 5.2.4 Algoritmik Parametre Yönetimi

Modül, yapay zeka tabanlı planlayıcınin optimizasyon yaparken kullanacağı critik metrikleri belirler:

- Zorluk Derecesi (Difficulty Level): 1 ile 5 arasında değişen bu değer, algoritmanın ilgili derse atayacağı odaklanma seanslarının (FocusSessions) yoğunluğunu doğrudan etkiler.

- Sınav Ağırlıkları (Exam Weights): Kullanıcının sınav bileşenlerine atadığı yüzdelik ağırlıklar, algoritmanın yaklaşan sınav tarihlerine göre hangi dersin çalışma planına öncelik vereceğini hesaplamasinda temel alınır.

## 5.2.5 Veritabanı Ekkileşimi

- Bağlantı Doğrulama: Herhangi bir veri yazma veya okuma işlemi öncesinde socket tabanlı bir internet bağlantı testi (8.8.8.8 üzerinden) yapılarak sistemin kararlılığı denetlenir.

- Bileşik Anahtar (Composite Key): Veriler Courses koleksiyonuna kaydedilirken, kullanıcılar arası veri izolasyonunu sağlamak ve yetkisiz çakışmaları engellemek için döküman kimliği (Doc ID) user_id ve course_id birleştirilerek (f"{user_id}_{course_id}") composite key oluşturulur.

- Veri Senkronizasyonu: Arayüzden alınan tüm girdiler tekil bir JSON paketi (Dictionary) haline getirilerek asenkron bir şekilde Firestore'a iletilir. İşlem başarılı olduğunu UI otomatik olarak yenilenerk veritabanı ile tam senkronize hale gelir.

## 5.3 Program ve Sınav Yönetimi Modülü

## 5.3.1 Amaç

Program ve Sınav Yönetimi Modülü, kullanıcının akademik yükümlülüklerini (haftalık ders programı ve sınav takvimi) sisteme entegre etmekle görevlidir. Bu modülün temel amacı, adaptif çalışma planı algoritmasının (FocuSync Algoritması) ihtiyaç duydugu temel parametreleri belirlemektir. Kullanıcı deneyimini (UX) iyileştirmek amacıyla veri girişi; geleneksel manuel yöntemler ve yapay zeka destekli Optik Karakter Tanıma (OCR) olmak üzere iki farklı mimari yaklaşım ile tasarlanmıştır.

## 5.3.2 Manuel Giriş Tasarımı

Manuel giriş alt sistemi, kullanıcının doğrudan grafiksel kullanıcı arayüzü (GUI) üzerinden veri manipülasyonu yapabilmesini sağlar. Uygulamanın sunduğu yapilarla okunan kısım doğrulama için bu arayüz aracılığı ile gösterilir. Gösterilen okunan program üzerinde düzenlemeler yapılır. PyQt6 kütüphanesi üzerine insa edilen bu katmanda, veri buttünlüğünü korumak için dinamik bileşenler kullanılmıştır:

- Sabit Program (Schedules) Arayüzü: Haftanın yedi günü için ayrı ayrı dinamik tablolar sunulur. Kullanıcılar her satırda ders kodu, saati ve etkinlik türünü (Teorik, Pratik vb.) belirlerken, sistem arka planda toplam haftalık saati ve akademik yükü (kredi bazlı) otomatik olarak hesaplayarak arayüzze yansıtır.

- Sınav (Exams) Arayüzü: Kullanıcıların vizeler, finaller veya ödevler için tarih ve not girişi yapabildiği dinamik satır tabanlı bir yapidır. Akıllı bileşenler (ExamTypeWidget) sayesinde, aynı ders için tekrar eden sınav türlerinin (Örn: Vize 1, Vize 2) isimlendirmeleri otomatik yönetilir.

## 5.3.3 PDF / OCR Tabanlı Veri Alma Tasarımı

Kullanıcının okul sistemlerinden indirdiği PDF veya resim formatındaki akademik belgelerin manuel giriş gerektirmeden sisteme aktarılmasını sağlayan alt sistemdir. Bu mimari üç aşamalı bir veri işleme boru hattı (pipeline) olarak tasarlanmıştir:

- Asenkron İşleme (Threading): Arayüzün (Main Thread) kilitlenmesini önlemek amacıyla, dosya okuma işlemi QThread tabanlı bağımsız bir arka plan işçisine (OCRWorker) devredilir.

- Metin Çıkarım: Yüklenen PDF belgelerindeki ham metinler ve tablo yapilari pdfplumber kütüphanesi kullanılarak çıkarılır.

- Yapay Zeka Destekli Çözümleme: Çıkarılan yapısal olmayan ham metin, Google Gemini AI modellerine (hız optimizasyonu için gemini-1.5-flash-8b modeli tercih edilmiştir) JSON semaları zorunlu kılınarak gönderilir. Model, metnin bir ders programı mı yoksa sınav takvimi mi olduğunu otomatik sıniflandırır (Belge Tipi Tespiti) ve veriyi ilgili sistem modellerine (_parse_schedule veya _parse_exam) uygun yapısal JSON formatına çevirir.

## 5.3.4 Veri Doğrulama ve Kullanıcı Onayı

OCR modülünden dönen veya manuel olarak girilen verilerin doğrudan veritabanına yazılması güvenlik ve tutarlılık riski taşidıgından, "Kullanıcı Onaylı Katı Doğrulama (Strict Validation)" mimarisi benimsenmiştir:

- Kesişim Doğrulaması: Tabloya eklenen her ders kodu, sistemdeki Courses (Dersler) koleksiyonu ile anlık olarak çapraz kontrole (cross-reference) tabi tutulur. Sistemde kayıtlı olmayan bir ders kodu kullanan bir sınav sisteme kaydedilemez.

- Akıllı Seçim ve Filtreleme: OCR tamamlandığında, sistem okunan veriler ile kullanıcıin aktif derslerini karşılastırir. Sadece kullanıcıin mevcut ders havuzuyla eşleşen satırlar otomatik olarak işaretlenir (Checkbox).

- Girdi Sınırlandırması (Input Capping): Not girişleri gibi sayısal alanlar QIntValidator kullanılarak donanımsal olarak 0 ile 100 arasına sabitlenmiştir. Hatalı tuşlamalarda (Örn: 150 yazılması) sistem girdiyi anında üst sınira (100) çeker.

- Çakışma Kontrolü: Aynı ders için birden fazla aynı türde sınav (İki adet "Vize 1" gibi) girilmeye çalışıldığında sistem uyarı vererek işlemi engeller.

## 5.3.5 Hata Yönetimi

Modül, dış servislere ve dosya sistemlerine bağımlı çalıştığı için genişletilmiş bir hata tolerans

(Fault Tolerance) mimarisine sahiptir:

- API ve Sunucu Hataları: OCR yapay zeka sunucularındaki olası anlık yoğunlukları (503 Service Unavailable) aşmak için, hata durumunda sistem çökmesini engelleyen "Zaman Aşımı ve Yeniden Deneme" algoritması kodlanmıştır. İstek başarısız olursa sistem 3 saniye bekleyip arka planda isteği tekrarlar.

- Yanlış Belge Yükleme: Sınnav arayüzüne ders programı belgesi (veya tam tersi) yüklendişinde, yapay zeka sınıflandırıcıı bu durumu tespit eder ve işlemi durdurarak kullanıcıı doğru menüye yönlendiren uyarı mesajları üretir.

- Ağ Bağlantısı Kaybı: Veritabanına (Firebase) yazma veya okuma işlemleri öncesinde internet durumu denetlenir. Bağlantı yoksa işlemler iptal edilerek kullanıcı arayüzunde bilgilendirilir.

## 5.4 Odak Oturumu Yönetimi Modülü

## 5.4.1 Amaç

Bu modül, kullanıcınin çalışma seanslarını başlattığı, yönettiği ve bitirdigi ana kullanıcı arayüzü (UI) katmanıdır. Temel amacı; arka planda çalışan Göruntü İşleme (Kafa Takibi) modülünü asenkron olarak yönetmek, kullanıcıya gerçek zamanlı görsel/işitsel geri bildirimler sunmak ve oturum sonunda elde edilen analitik verileri güvenli bir şekilde Veritabanı Modülü'ne aktarmaktır.

## 5.4.2 Oturum Başlatma / Durdurma / Duraklatma Akışı

Oturum yönetimi, durum (state) tabanlı bir mimari üzerine inşa edilmiştir.

- Başlatma: Kullanıcı ders seçimini (QComboBox üzerinden) yapıp "Seansı Başlat" butonuna tıkladığında arayüz kilitlenir (veri tutarlılığı için ders seçimi pasif hale gelir). Arka planda HeadTracker sınifı yeni bir iş parçacığı (QThread) olarak başlatılır ve donanımsal kamera erişimi tetiklenir.

- Durdurma: Oturum sonlandırıldığında kamera serbest bırakılır, asenkron iş parçacıgı güvenli bir şekilde sonlandırılır (tracker.stop()) ve arayüz başlangıç durumuna (Idle State) döndürülür. Açık kalmış olabilecek tüm uyarı pencereleri (Distraction AlertDialog) temizlenir.

## 5.4.3 Zamanlayıcı Yönetimi

Modül, arayüzü kitlemeden gerçek zamanlı güncellemeler yapabilmek için QTimer sınnifını kullanır.

- Saniyede bir tetiklenen (_tick) bu zamanlayıcı, ekrandaki dijital saati (HH:MM:SS formatında) günceller.

- Dinamik Odak Skoru: Arayüz kendi içinde tahmini bir skor hesaplamak yerine, doğrudan HeadTracker üzerinden gelen salise bazlı total_focus_time ve total_session_time verilerini oranlar. Elde edilen anlık başarı yüzdesi, QPainter ile çizilmiş özel bir arayüz bileşeni olan FocusCircle üzerine aktarılır. Bu halkanın rengi, skora göre dinamik olarak değişir (<%50 Kırmızı, <%80 Turuncu, >%80 Yeşil).

## 5.4.4 Oturum Verisi Oluşturma

Seans sonlandırıldığında Göruntü İşleme modülü, hesapladığı kesin verileri (actual_focus_time, focus_score, head_tilt_degree) bir paket (dictionary) halinde session_completed sinyali üzerinden arayüze firlatır. Arayüz, bu veriyi kullanıcınin başa seçtiği spesifik course_id (Ders ID) ile birleştirerek Veritabanı yöneticisine (db_manager.add_focus_session) iletir.

- Offline Koruma: Veritabanına kayıt işlemi sırasında yaşanabilecek ağ kesintilerine karşı try-except blokları kullanılmış, veri gönderilemese dahi uygulamanın çökmesi engellenerek kullanıcıya "Bağlantı Hatası" bildirimi gösterilmesi sağlanmıştır.

## 5.4.5 Diğer Modüllerle Etkileşim

FocusPage modülü, sistemin "Controller" (Kontrolcü) bileşeni olarak birçok modülle doğrudan etkileşim halindedir:

- Veritabanı Senkronizasyonu (db_manager): Kullanıcı sayfaya her giriş yaptığında (showEvent metodu tetiklenerek) veritabanındaki aktif dersler çekilir ve listede gösterilir. Bu sayede durum senkronizasyonu (State Sync) sağlanır.

- Kamera Takibi (HeadTracker): Canlı kamera yayını, frame_processed sinyali ile yakalanıp QImage ve QPixmap dönüşümleri yapılarak arayüzdeki cam_placeholder alanına canlı yayın (Live Feed) olarak yansıtılır.

- Uyarı Modülü (Distraction Alert): Odak bozulduğunda, arka planda (küçültülmüş pencerelerde) dahi kullanıcının dikkatini çekebilmek için İşletim Sistemi seviyesinde "Her Zaman Üstte" (WindowStaysOnTopHint) duran ve sistem sesi (winsound.MessageBeep) çalışan bağımsız bir pop-up diyalog penceresi tetiklenir.

## 5.5 Kafa Takibi ve Odak Skoru Modülü

## 5.5.1 Amaç

Bu modülün temel amacı, kullanıcının bilgisayar karşısındaki fiziksel duruşunu gerçek zamanlı olarak analiz ederek ekrana odaklanıp odaklanmadığını tespit etmektir. Modül, karmaşık göruntü işleme tekniklerini kullanarak kafa hareketlerini sayısal verilere dönüştürür ve bu verilerden bir "Odak Skoru" üretir.

## 5.5.2 Kamera Akışı İşleme Tasarımı

Sistem, OpenCV kütüphanesi (cv2.VideoCapture) üzerinden cihazın varsayılan kamerasından ham görüntü akışını yakalar. Performans optimizasyonu ve işlemci yükünü dengede tutmak adına görüntü akışı saniyede 15 kare (15 FPS) ile sınırlandırılmıştır. Her bir kare, işlenmeden önce MediaPipe motorunun gereksinim duyduğu RGB formatına dönüstürülür.

## 5.5.3 Yüz Tespiti ve Landmark Kullanımı

Yüz tespiti için Google'in MediaPipe FaceLandmarker (v0.10.x) kütüphanesi kullanılmaktadır. Algoritma, yüz üzerinde 478 farklı nokta (landmark) tespit edebilse de, kafa pozisyonu tahmini (Pose Estimation) için belirlenmiş 6 kritik nokta (burun ucu, çene ucu, sol/sağ göz pınarları ve sol/sağ ağız kenarları) üzerinden işlem yapar.

## 5.5.4 Pitch / Yaw / Roll Hesaplama

Kafa pozisyonu, 2D görüntü düzlemindeki landmark noktaları ile standart bir 3D insan yüzü modeli arasındaki ilişkin çözülmesiyle hesaplanır. Bu aşamada:

- OpenCV solvePnP (Perspective-n-Point) algoritması kullanılarak rotasyon vektörleri elde edilir.

- Rodrigues dönüşümü ve RQDecomp3x3 metotları ile bu vektörler Euler açılarına (Pitch: Yukarı/Aşağı, Yaw: Sağ/Sol, Roll: Omuzlara Eğilme) dönüştürülür.

## 5.5.5 Referans Açı Belirleme

Her kullanıcının oturuş bozukluğu veya kamera açısı farklı olabileceği için statik limitler yerine "Dinamik Kalibrasyon" mekanizması tasarlanmıştır. Oturumun ilk 15 karesinde (yaklaşık 1 saniye) kullanıcının duruşu örneklenerek bir "Merkez Noktası" (Base Pitch ve Base Yaw) hesaplanır. Tüm odak kontrolleri bu kişiselleştirilmiş referans noktasına göre "göreceli" olarak yapılır.

## 5.5.6 Dikkat Dağılması Tespit Mantığı

Sistem, belirlenen esnek limitler üzerinden bir Durum Makinesi (State Machine) olarak çalışır:

- Sinir Değerler: PITCH_LIMIT = 16° ve YAW_LIMIT = 18° olarak set edilmiştir.

- Yumuşatma (Debounce): Anlık kafa sarsıntılarını "dikkat dağıldı" olarak algılamamak için 4 karelik bir tampon süresi (Required Frames) uygulanır. Kullanıcı belirlenen limitlerin dışında üst üste en az 4 kare kalmadığı sürece odak durumu değişmez.

## 5.5.7 Odak Skoru Hesaplama

Odak skoru, oturum süresince toplanan hassas zaman verileriyle hesaplanır. QThread döngüsü icinde her kareden sonra geçen "Delta Time" hesaplanarak total_session_time ve kullanıcıin odaklı olduğu total_focus_time değişkenlerine eklenir. Oturum sonunda (veya anlık olarak) bu iki değerin oranı üzerinden yüzde bazlı bir başarı skoru üretilir.

## 5.5.8 Performans ve Hata Yönetimi

Modül, ana kullanıcı arayüzünü (UI) dondurmamak için PyQt6 QThread yapısında asenkron olarak çalışır. Donanım erişim hataları (kamera bulunamaması vb.) veya model yükleme sorunları, özel tanımlanmış error_occurred sinyalleri ile yakalanarak üst katmanlara iletilir.

## 5.6 Beyaz Liste (Whitelist) Kontrol Modülü

## 5.6.1 Amaç

Beyaz Liste (Whitelist) Kontrol Modülü, kullanıcınin odak oturumu sırasında çalışmasına izin verdigi masaüstü uygulamalarını tanımlamasını ve aktif pencere düzeyinde bu uygulamaların denetlenmesini sağlar. Modülün temel amacı, odak seansı boyunca yalnızca izin verilen kullanıcı uygulamalarının kullanımını serbest bırakmak; bunun dışındaki aktif uygulamaları ihlal olarak algılayarak kullanıcıya anlık geri bildirim sunmak ve oturum sonunda bu ihlalleri özetleyip raporlamaktır. Modül, özellikle Focus Mode ekranı ile buttünleşik çalışacak şekilde tasarlanmıştır; odak oturumu başladığında izleme süreci başlatılır, oturum sonlandığında ise ihlal özeti üretilip veritabanına kaydedilir.

## 5.6.2 Whitelist Veri Yapısı Tasarımı

Whitelist modülünün çekirdek iş mantığı `WhitelistLogic` sınıfı içinde tutulmaktadır. İzin verilen uygulamalar `_whitelist: set[str]` veri yapısında saklanır. Set yapısının tercih edilme nedeni, aynı `.exe` adının birden fazla kez eklenmesini engellemesi ve üyelik kontrolünü hızlı gerçekleştirmesidir. Bunun yanında modül, ihlal yönetimi için ek durum alanları da barındırir: son ihlalin exe adı (`_last_violation_exe`), aktif ihlal edilen uygulama (`_active_violation_exe`), aktif ihlalin başlangıç zamanı (`_active_violation_start`), tüm ihlal bölümlerini tutan kayıt listesi (`_violation_log`) ve odak oturumu ile ilişki kurmak için `focus_session_id` bilgisi. Her ihlal kaydı sözlük biçiminde `app_name`, `duration_seconds`,

`duration_hms`, `started_at` ve `ended_at` alanlarını içerir. Bu yapı, hem anlık kontrol hem de oturum sonu raporlama için yeterli ayrınıyı sağlar.

## 5.6.3 Uygulama Ekleme / Silme / Listeleme Süreci

Whitelist yönetim ekranı, kullanıcıya üç farklı uygulama ekleme yöntemi sunar: kurulu uygulamalar listesinden seçme, dosya sisteminden `.exe` dosyası seçme ve elle exe adı girme. "Kurulu Uygulamalardan Ekle” akışında sistem, Windows Registry üzerinden kurulu uygulamaları tarar; `DisplayName`, `DisplayIcon`, `InstallLocation` ve `Publisher` gibi alanları okuyarak uygun exe dosyasını tahmin eder ve kullanıcıya filtrelenebilir bir seçim penceresi sunar. "Dosyadan .exe Seç” akışında kullanıcı doğrudan bir çalıştırılabilir dosya seçer. "Elle Ekle” akışında ise kullanıcı örneğin `chrome.exe` gibi doğrudan exe adı girer. Eklenen girişler normalize edilerek küçük harfe çevrilir ve whitelist set’ine eklenir. Silme işlemi, listede seçili olan exe girdisinin set’ten çıkarılmasıyla gerçekleştirilir. Listeleme işlemi ise whitelist içeriğinin sıralanarak arayüzde `QListWidget` üzerinde gösterilmesi şeklinde yürütülür. Ayrica “Son İhlale İzin Ver” fonksiyonu ile son tespit edilen ihlalli uygulama tek işlemle whitelist'e alınabilir.

## 5.6.4 Aktif Pencere ve Süreç İzleme Mekanizması

Aktif pencere takibi `MonitorWorker` adlı ayrı bir `QThread` içinde yürütülür. Bu tasarım, kullanıcı arayüzünün donmasını önlemek ve pencere denetimini arka planda sürekli sürdürebilmek için seçilmiştir. İşci thread, belirli aralıklarla aktif pencere bilgisini alır; bunun için Windows üzerinde `win32gui.GetForegroundWindow`, `win32process.GetWindowThreadProcessId` ve `psutil.Process(pid).name()` çağrılarıyla hem pencere başlığı hem de o pencereye ait exe adı elde edilir. İzleme çevrimi whitelist kopyasını alır, aktif exe’yi okur ve durumun “izinli” ya da “ihlal” olduğunu belirler. Kodda işci thread 1 saniyelik kontrol aralığıyla başlatılmıştır; fakat her çevrim içinde 200 ms’lik uyku adımları kullanılarak daha kontrollü bir bekleme uygulanır. Windows bağımlı kütüphaneler bulunmazsa izleme başlatılmaz ve kullanıcıyla uyarı verilir.

## 5.6.5 İhlal Tespit Mantığı

İhlal tespiti, aktif exe adının izin verilen gruplarla karşılastırılması prensibine dayanır. Sistem öncelikle aktif pencere bilgisi alınamadığında bunu ihlal saymaz. Ardindan işletim sistemi için güvenli kabul edilen uygulamalar (`SYSTEM_EXES`) ve uygulamanın kendisine ait süreçler (`SELF_EXES`) otomatik olarak izinli kabul edilir. Ayrica geliştirme ortamında uygulamanın `python.exe` üzerinden çalıştırıldığı durumlar için, pencere başlığında `focusync` ifadesi yer alıyorsa bu süreç de izinli sayılır. Bu istisnaların dışındaki bir exe adı, whitelist set’i içinde yer almıyorsa ihlal olarak değerlendirilir ve detay bilgisi `exe_name | window_title` biçiminde üretilir. İhlal başladığında sistem hem toplam ihlal süresini ölçmeye başlar hem de ilgili exe için ayrı bir ihlal bölümü oluşturur. Aktif ihlal eden uygulama değişirse önceki ihlal bölümü kapatılır ve yeni bir bölüm başlatılır. Bu yapı, tek bir oturum içinde birden fazla farklı uygulamanın neden olduğu ihlallerin ayrı ayrı raporlanmasını sağlar.

## 5.6.6 Sesli ve Görsel Uyarı Tasarımı

Modül, ihlal durumunda kullanıcıyı hem görsel hem de işitsel olarak uyarır. Görsel uyarı iki katmanda sunulmaktadır. İlk katmanda whitelist yönetim ekranındaki durum paneli güncellenir; burada “İhlal: EVET” etiketi ve tespit edilen uygulama adı gösterilir. İkinci katmanda ise ekranın üstünde kalacak şekilde tasarlanmış ayrı bir `ViolationAlertDialog` penceresi açılır. Bu pencere, ihlalin tespit edildiğini ve hangi uygulamanın çalıştığını kullanıcıya açık sekilde bildirir. Sesli uyarı tarafında sistem önce proje icindeki `whitelist_alert.wav` dosyasını asenkron olarak çalmayı dener; bu dosya bulunamazsa işletim sisteminin varsayılan uyarı sesi (`MessageBeep`) kullanılır. Kod tasarımında sesin yalnızca yeni ihlal başlangıcında çalışması, aynı ihlalin sürekli tekrarında kullanıcıyı gereksiz biçimde rahatsız etmemek için tercih edilmiştir. İhlal sona erdiğinde pop-up otomatik olarak kapatılır ve ekran “İhlal: Yok” durumuna döner.

## 5.6.7 İhlal Süresi Hesaplama

İhlal süresi hesaplaması iki seviyede yürütülür. Birinci seviyede, oturum içindeki toplam ihlal süresi `_violation_start_time` üzerinden ölçülür. Bir ihlal başladığında başlangıç zamanı kaydedilir; ihlal bittiğinde geçen süre hesaplanarak `_total_violation_seconds` değişkenine eklenir. İkinci seviyede, her ihlal eden uygulama için ayrı “episode” kayıtlar oluşturulur. `build_violation_entry` fonksiyonu, uygulamanın aktif olduğu başlangıç ve bitiş zamanları arasındaki farkı hesaplar; süre 1 saniyenin altındaysa kayıt oluşturmaz,aksi halde süreyi hem saniye cinsinden hem de `HH:MM:SS` formatında üretir. Böylece sistem, hem toplam ihlal süresini hem de uygulama bazında ne kadar süre boyunca ihlal yaşandığın ayrı ayrı sunabilir. Bu tasarım, raporlamada yalnızca “ihlal oldu” demek yerine ihlalin yoğunluğunu sayısal olarak ifade etmeyi mümkün kılar.

## 5.6.8 Oturum Sonu İhlal Özeti Oluşturma

Whitelist izleme süreci sona erdiğinde `stop_monitoring_and_save()` fonksiyonu çalıştırılır. Bu fonksiyon önce toplam izleme süresini hesaplar, ardından hâlen açık bir ihlal varsa onun süresini toplam ihlal süresine ekler ve aktif ihlal bölümünü kapatır. Sonrasında özet veriler hazırlanır: toplam izleme süresi, toplam ihlal süresi ve kaydedilen ihlal bölümü sayısı. Bu özet hem log çıktısı olarak yazdırılır hem de veritabanına gönderilecek veri yapısının temelini oluşturur. Focus Mode ile entegrasyon kapsamında tasarımda önce `FocusSessions` kaydının oluşturulması, ardından whitelist oturum özetinin bunun `focus_session_id` değeriyle ilişkilendirilmesi amaçlanmıştır. Böylece whitelist özeti, hangi odak seansına ait olduğunu referans seviyesinde gösterebilir.

## 5.6.9 Veritabanı Ekkileşimi

Whitelist modülünün veritabanı etkileşimi iki ayrı veri düzeyinde düşünülmüştür. Birinci düzey kullanıcı profilidir. `Users` koleksiyonunda `allowed_apps` alanı tanımlanmıştır ve `update_user_profile(...)` fonksiyonu bu alanı güncelleyebilecek biçimde tasarlanmıştır. Bu, whitelist’in kalıcı kullanıcı tercihi olarak saklanabilmesi için gerekli veri modelinin hazır olduğu güstermektedir. Ancak paylaşılan whitelist ekranı ve iş mantığı kodunda ekleme/silme işlemlerin bu güncelleme fonksiyonuna bağlandığı açık biçimde görülmemektedir; dolayısıyla mevcut kod parçasına göre whitelist içeriği çalışma anında bellek içinde tutulmakta, kalıcı senkronizasyon tarafı ise henüz eksik veya başka dosyada bırakılmış görünmektedir. İkinci düzey ise oturum raporlamasidır. `DatabaseManager.save_whitelist_session(...)` fonksiyonu, `WhitelistSessions` koleksiyonuna `user_id`, `focus_session_id`, toplam izleme süresi, toplam ihlal süresi, okunabilir süre alanları, ihlal sayısı, ihlal listesi, oturum başlangıc/bitiş zamanları ve `saved_at` damgasını tek dokümanda kaydeder. Bu yaklaşım, whitelist ihlallerini parça parça değil, bir oturum özeti halinde saklayarak raporlama ve istatistik üretimini kolaylaştırir. Ayrıca dashboard tarafında toplam ihlal sayısı bu koleksiyonan toplanmaktadir.

## 5.7 Adaptif Zorluk Güncelleme Modülü

## 5.7.1 Amaç

Bu modülün temel amacı, kullanıcının geçmiş çalışma performansını (odak skorları, ihlal süreleri ve ders hedefleri) analiz ederek her dersin zorluk seviyesini dinamik olarak yeniden hesaplamaktır. Sabit bir çalışma programı yerine, kullanıcının gerçek verilerine dayalı "adaptif" bir deneyim sunarak, verimin düştüğü derslere daha fazla ağırlık verilmesini ve çalışma planının bu verilere göre optimize edilmesini sağlar.

## 5.7.2 Kullanilan Girdiler

Algoritma, karar verme sürecinde veritabanındaki şu metrikleri girdi olarak kullanır:

- Focus Score (Odak Skoru): FocusSessions koleksiyonundan gelen, kafa takibi modülü ile hesaplanan 0-100 arası başarı yüzdesi.

- Violation Duration (İhlal Süresi): WhitelistSessions koleksiyonundan gelen, çalışma sırasında odak dağıtan uygulamalarda geçirilen süre.

- Target vs. Actual Grade (Hedef ve Mevcut Not): Kullanıcınin Courses koleksiyonunda belirlediği hedef not ile Exams koleksiyonuna girilen güncel notlar arasındaki sapma.

- Session Consistency (Oturum Sürekliliği): Planlanan çalışma süresi ile fiilen gerçekleştirilen süre arasındaki oran.

## 5.7.3 Zorluk Güncelleme Algoritması

Sistem, her pazar günü veya kullanıcı yeni bir plan talep ettiğinde arka planda şu mantıksal akışı işletir:

- Veri Toplama: DatabaseManager aracılığıyla ilgili kullanıcıya ait son 7 günlük tüm FocusSessions kayıtları çekilir.

- Ağırlıklı Ortalama Hesaplama: Her ders için o haftaki ortalama odak skoru hesaplanır. Eğer odak skoru eşik değerin (%60) altındaki ve ihlal süresi toplam sürenin %20'sini aşıyorsa, dersin zorluk seviyesi (difficulty_level) kademeli olarak artırılır.

- Başarı Analizi: Sınav notu hedef notun altında kalan dersler için "Kritik Öncelik" bayrağı atanır.

- Seviye Güncelleme: Elde edilen veriler sonucunda dersin zorluk seviyesi 1 ile 5 arasında normalize edilir. Örneğin, sürekli düşük odak skoru alınan bir dersin zorluğu 3'ten 4'e yükseltilerek bir sonraki haftalık planda o derse daha fazla seans atanması sağlanır.

## 5.7.4 Yeni Çalısma Planı Üretimi

Güncellenen zorluk seviyeleri, StudyPlans koleksiyonu oluşturulurken ana parametre olarak kullanılır:

- Zaman Tahsisi: Zorluk seviyesi yüksek (4 veya 5) olan derslere, haftalık boş zaman dilimlerinde öncelik verilir ve seans süreleri daha uzun tutulur.

- Dağılım Stratejisi: Algoritma, bilişsel yükü dengelemek adına çok zor bir dersin seansından sonra daha düşük zorluk seviyesine sahip bir dersi plana yerleştirir.

- Çiktı: Oluşturulan yeni JSON paketi StudyPlans koleksiyonuna asenkron olarak yazılır ve mobil uygulama ile еşzamanlı olarak paylaşılır.

## 5.7.5 Sinirlar ve Kisitlar

- Zorluk Sınırı: Bir dersin zorluk seviyesi algoritma tarafından 1'in altına düşürülemez ve 5'in üstüne çıkarılamaz.

- Minimum Veri Gereksinimi: Bir ders hakkında zorluk güncellemesi yapılabilmesi için o derse ait en az 3 tamamlanmış odak oturumu (Focus Session) bulunmalıdır;aksi takdirde kullanıcı tarafindan girilen manuel zorluk seviyesi korunur.

- Haftalık Sabit Program Engeli: Çalışma planı üretilirken Schedules koleksiyonundaki sabit ders saatleri "rezerve" alan olarak kabul edilir; bu saatlere hiçbir şekilde ek çalışma seansı atanamaz.

## 5.8 İstatistik ve Raporlama Modülü

## 5.8.1 Amaç

İstatistik ve Raporlama Modülü, kullanıcıın geçmiş çalışma oturumlarindan elde edilen verileri anlamlı grafiklere ve performans göstergelerine dönüştürmeyi amaçlar. Bu modül, kullanıcıın odaklanma alışkanlıklarını görselleştirerek hangi derslerde daha başarılı olduğunu veya hangi zaman dilimlerinde dikkatinin dağıldığını saptamasına yardımcı olur.

## 5.8.2 Toplanan Veriler

Modül, raporların oluşturmak için aşağıdaki veri setlerini bir araya getirir:

- Odak Verileri: FocusSessions koleksiyonundan alınan odak skoru, net odak süresi ve kafa eğim açılari.

- İhlal Verileri: WhitelistSessions koleksiyonundan alınan toplam ihlal süresi, ihlal sayısı ve en çok ihlale sebep olan uygulama listesi.

- Akademik Veriler: Exams koleksiyonundaki sınav notları ve Courses koleksiyonundaki hedef notlar ile güncel not ortalamaları.

## 5.8.3 İstatistik Hesaplama Yöntemi

Sistem, ham verileri kullanıcıya sunmadan önce şu analiz süreçlerinden geçirir:

- Trend Analizi: Odak skorları zamana bağlı bir dizide (time-series) sıralanarak performansın artış veya azalış eğilimi belirlenir.

- Başarı Normalizasyonu: Net odak süresi ile toplam oturum süresi oranlanarak genel verimlilik katsayısı üretilir.

- Kategorik Gruplandırma: Veriler ders bazlı gruplandırılarak, her dersin kullanıcı üzerindeki bilişsel yükü ve başarı oranı karşılastaırılır.

## 5.8.4 Kullanıcıya Sunulan Raporlar

Kullanıcı, arayüz üzerinden şu özet raporlara erişebilir:

- Genel Performans Özeti: Toplam tamamlanan seans sayısı, tüm seansların ortalama odak skoru ve kaydedilen en yüksek odak skoru.

- Ders Bazlı Analiz: Her ders kartında gösterilen güncel not ortalaması ve hedefe ulaşma yüzdesi.

- İhlal Raporu: Oturum bazında hangi uygulamaların çalışmayı kaç kez ve ne kadar süreyle böldüğünün dökümü.

## 5.8.5 Görselleştirme Tasarımı

Veriler, kullanıcı deneyimini artırmak için modern görsel bileşenlerle sunulur:

- Çizgi Grafikler (Line Chart): fl_chart kütüphanesi kullanılarak oluşturulan, seans sırasına göre performans değişimini gösteren dinamik grafikler.

- Renk Kodlu Veri Noktaları: Skorlara göre yeşil (≥%75), turuncu (≥%50) ve kırmızı (<%50) olarak renklendirilen veri noktaları ile hızlı durum tespiti.

- Özet Kartlar ve Tablolar: Geçmiş seansların tarih, saat ve başarı metrikleriyle listelendiği, ders kodlarına göre ayrıştırılmış detaylı liste görünümü.

## 5.9 Mobil Senkronizasyon Modülü

## 5.9.1 Amaç

Bu modül, kullanıcının masaüstü uygulamasında üretilen tüm verilere (dersler, çalışma planları, sınav takvimleri, odaklanma istatistikleri) mobil uygulama üzerinden erişilmesini sağlar. İlgili SRS gereksinimleri: MS-REQ-01/02, MS-PERF-01, MS-ERR-01.

## 5.9.2 Senkronizasyon Mantığı

FocuSync mobil uygulaması ile masaüstü uygulaması arasında doğrudan bir iletişim protokolü ya da ayrı bir senkronizasyon servisi bulunmamaktadır. Her iki platform da aynı Firebase Firestore projesine (focusync-d9f21) bağlı olduğundan senkronizasyon doğal olarak gerçekleşir: masaüstü uygulama bir koleksiyona veri yazdığında, mobil uygulama aynı koleksiyonu sorgulayarak güncel veriye ulaşir.

Mobil uygulama büyük ölçüde yalnızca okuma işlemleri yapar; veri yazımı ve güncelleme masaüstü uygulamasının sorumluluğundadır. Kullanıcı profil bilgileri bunun istisnasıdır: ad, soyad, okul ve şifre güncellemeleri mobil uygulama üzerinden de yapılabilmektedir.

## 5.9.3 Masaüstü-Mobil Veri Akışı

Mobil uygulama aşağıdaki Firestore koleksiyonlarından veri okur:

<table border="1"><tr><td>Koleksiyon</td><td>Metod</td><td>Filtreleme</td></tr><tr><td>Users</td><td>getUserProfile(userId)</td><td>Belge ID'si ile doğrudan erişim</td></tr><tr><td>Courses</td><td>getCourses(userId)</td><td>user_id alanına göre</td></tr><tr><td>Schedules</td><td>getSchedule(userId)</td><td>user_id alanına göre, ilk eşleşen</td></tr><tr><td>StudyPlans</td><td>getStudyPlan(userId)</td><td>user_id alanına göre, son eklenen (docs.last)</td></tr><tr><td>Exams</td><td>getExamSchedule(userId)</td><td>user_id alanına göre, ilk eşleşen</td></tr><tr><td>FocusSessions</td><td>getSessions(userId)</td><td>user_id+Dart tarafi:status=='Completed',timestamp artan</td></tr></table>

Tüm sorgular user_id referansıyla filtrelenir. Bu sayede her kullanıcı yalnızca kendi verilerine erişir.

Haftalık program verisinde özel bir yapı söz konusudur: Schedules koleksiyonundaki belgeler weekly_routine adlı iç içe bir harita içermektedir. getScheduleCourseIds() metodu bu haritayı iterasyonla gezerek programdaki benzersiz ders ID'lerini çıkarmaktadır.

StudyPlans koleksiyonunda masaüstü uygulama zamanla birden fazla plan belgesi oluşturabilmektedir. Mobil uygulama docs.last ile her zaman en güncel planı okur.

## 5.9.4 Tutarlılık ve Çakışma Yönetimi

Veri çakışmasi senaryosu bu tasarımda yapısal olarak mevcut değilir: mobil uygulama kullanıcı profili dışında hiçbir veri yazmadığından masaüstü-mobil çakışması oluşamaz. Profil güncellemeleri ise her iki platformda aynı Firestore belgesini güncellediği için Firestore'un son-yazım-kazanır (last-write-wins) modeli yeterlidir.

## Ag Kesintisi Durumu:

Uygulama katmanında çevrimdışı önbellek mekanizması bulunmamaktadır. Bağlantı kesildiğinde NetworkWrapper bileşeni uyarı bandını gösterir ve Firestore sorguları catch bloğuna düşerek kullanıcıyla bağlantı hatası mesajı iletilir. Bağlantı yeniden sağlandığında NetworkWrapper içindeki onConnectivityChanged stream'i durum değişikliğini algılar; _hasInternet degeri true olarak guncellenir ve bağlı ekranlar bu değişikliği reaktif olarak işleyerek Firestore sorguların otomatik olarak yeniden tetikler. Kullanıcının manuel müdahalesine gerek kalmadan arayüz en güncel verilerle yenilenir. Bu davranış MS-ERR-01 gereksinimini karşılamaktadır.

## Oturum Kimliği:

SharedPreferences'ta saklanan user_id, tüm Firestore sorgularında filtre anahtari olarak kullanılır. Bu değer oturum boyunca sabit kalır ve ancak çıkış işlemiyle silinir.

## 5.10 Veritabanı Tasarımı

FocuSync sistemi, geleneksel ilişkisel veritabanı yönetim sistemleri yerine, yüksek esneklik ve hızlı okuma/yazma performansı sunan bulut tabanlı bir NoSQL mimarisi olan Google Firebase Firestore üzerinde insa edilmiştir. Bu tercih, adaptif öğrenme algoritmalarının ürettiği dinamik verilerin ve sensörlerden (kamera) gelen anlık odaklanma istatistiklerinin gecikmesiz olarak işlenebilmesini sağlar.

## 5.10.1 Genel Veritabanı Mimarisi

Sistem mimarisi, izole edilmiş ancak referans anahtarlari ile mantıksal olarak birbirine bağlanmış "Koleksiyon (Collection)" ve "Doküman (Document)" mantığına dayanır. Veritabanı erişimi, güvenlik ve veri buttünlüğünü sağlamak amacıyla istemci (istemci arayüzü) tarafina kapalı tutulmuş olup, tüm işlemler merkezi bir "Database Manager" (Admin SDK) sınıfı üzerinden gerçekleştirilir.

Bu mimaride veriler; JSON formatında esnek şemalarla saklanır. Veri tekrarını (redundancy) tolere eden ancak okuma hızını maksimize eden bu yapı, hiyerarşik sorgular ve referans anahtarları (user_id, course_id vb.) aracılığıyla veri buttünlüğünü (relational integrity) korur.

Koleksiyonlar arası veri akışı ve dokümanların birbirlerine hangi referans anahtarlarıyla bağlandığın gösteren detaylı yapı için Ek-C: Veritabanı Şeması bölümüne bakılabilir.

## 5.10.2 Koleksiyonlar / Tablolar

Sistemdeki tüm veriler işlevsel buttünlüge göre 7 ana koleksiyona ayrılmıştır:

- Users: Kullanıcı profilleri, kimlik doğrulama bilgileri ve temel kullanıcı bilgileri.

- Courses: Sistemde tanımlı dersler, her derse ait bilgiler ve zorluk seviyeleri.

- Schedules: OCR modülü tarafından okunan veya manuel giriş ile kullanıcıın uygulamaya girişini sağladığı haftalık sabit ders programları.

- StudyPlans: FocuSync algoritması tarafından üretilen dinamik çalışma planları. Her derse ilişkili olarak belli çalışma seansları önerir.

- FocusSessions: Kamera modülü ile takip edilen ve tamamlanan, FocuSync algoritması tarafından önerilen seanslara ilişkin gerçekleştirilen çalışma oturumları.

- WhitelistSessions: Uygulama izleme modülü tarafindan yakalanan dikkat dağıtıcı uygulama ihlalleri. Her bir odak çalışma oturumunda eş zamanlı çalıştırılabilir.

- Exams: Kullanıcının kayıt olduğu derslere ilişkin akademik sınav tarihleri ve not bilgileri.

## 5.10.3 Kullanıcı (Users) Koleksiyonu

Users koleksiyonu, sisteme kayıtlı her kullanıcıya ait kimlik ve profil bilgilerini barındırrı. Koleksiyondaki her doküman, Firebase altyapısı tarafından atanan benzersiz doküman kimliği ile tanımlanır ve bu değer diğer tüm koleksiyonlar için birincil referans anahtarı işlevi görür.

Her kullanıcı dokümanı aşağıdaki alanlardan oluşmaktadir:

- email (string): Kullanıcının sisteme kayıt olduğu e-posta adresi.

- **password** (*string*): Kullanıcının PBKDF2 algoritmasıyla oluşturulmuş hash değeri.

- **role** (string): Kullanıcınin sistem içindeki rolünü tanımlar; varsayılan değer "User" olarak atanır. Bu alan, ileriki geliştirme aşamalarında çoklu kullanıcı türlerini desteklemek üzere genişletilebilir biçimde tasarlanmıştır.

- **name** (string): Kullanıcının adı.

- surname (string): Kullanıcıın soyadı.

- school (string): Kullanıcının kayıtlı olduğunu eğitim kurumu.

- salt (string): Şifre hashleme işleminde kullanılan kullanıcıya özel rastgele değer.

## 5.10.4 Ders (Courses) Koleksiyonu

Courses koleksiyonu, kullanıcıların sisteme tanımladığı derslere ait verileri saklar. Her dokümanın kimliği {user_id}_{course_id} formatında oluşturulan bileşik bir anahtar yapısına sahiptir; bu tasarım, farklı kullanıcıların aynı ders kodunu kullanması durumunda doküman çıkışmalarını önler.

Her ders dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id** (string): Dersin ait olduğunu kullanıcıya yönelik referans anahtarı.

- **course_id** (*string*): Derse özgü benzersiz tanımlayıcı.

- **course_name** (string): Ders adı. Schedules koleksiyonuna yeni bir program kaydedildiğinde CASCADE mantığıyla güncellenir.

- difficulty_level (number): Dersin zorluk seviyesi. Başlangıca kullanıcı tarafından belirlenir; adaptif algoritma tarafından çalışma performansına göre dinamik olarak güncellenir.

- weekly_hours (number): Haftalık toplam ders saati.

- exam_date (string): Dersin sınav tarihi. Exams koleksiyonu ile senkronize biçimde güncellenir.

- exam_weights (object): Vize, Final gibi sınav türlerine karşılık gelen not ağırlıklarını içeren sözlük yapısı.

- exam_grades (object): Sınav türlerine karşılık gelen not değerlerini içeren sözlük yapısı. Exams koleksiyonuyla senkronize edilir.

- **target_grade** (*number*): Kullanıcıının bu ders için belirlediği hedef not.

- **is_active (boolean)**: true değeri dersin aktif programda yer aldığın, false değeri ise dersin arşive alındığın belirtir. Bu alan üzerinden uygulanan yumuşak silme mekanizması, geçmiş çalışma verilerinin ve istatistiklerin veri buttünlüğü bozulmaksızın korunmasın sağlar.

## 5.10.5 Sabit Program (Schedules) Koleksiyonu

Schedules koleksiyonu, kullanıcıın OCR modülü aracılığıyla taratarak ya da manuel olarak sisteme girdigi haftalık sabit ders programlarını depolar. Her doküman, bir kullanıcıya ait tek bir dönemlik ders programını temsil eder.

Her program dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id** (*string*): Programın ait olduğu kullanıcıya yönelik referans anahtarı.

- schedule_name (string): Programa verilen dönem adı.

- **updated_at** (*timestamp*): SERVER_TIMESTAMP ile otomatik atanan, programın en son güncellenme zamanı.

- weekly_routine (object): Haftanın her gününe karşılık gelen ders dilimlerini listeleyen yapı. Her günün değeri bir dizi olup her dizi elemanı course_id, course_name, start_time, end_time ve type alanlarını içerir.

save_full_schedule fonksiyonu çağrıldığında mevcut program dokümanı silinerek yenisyle değiştirilir; eş zamanlı olarak Courses koleksiyonu upsert ve soft delete mantığıyla güncellenir. Bu sayede ders listesi her zaman aktif programla tutarlı kalır.

## 5.10.6 FocuSync Önerilen Program (StudyPlans) Koleksiyonu

StudyPlans koleksiyonu, adaptif öğrenme algoritması tarafından kullanıcıya özgü olarak üretilen haftalık çalışma planlarını depolar. Her doküman bir haftaya ait planlı çalışma seanslarını içerir ve algoritmanın yeni bir plan hesaplamasıyla birlikte yeniden üretilir.

Her plan dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id (string):** Planın ait olduğu kullanıcıya yönelik referans anahtarı.

- plan_start_date (timestamp): Planın geçerli olduğu haftanın başlangıç tarihi.

- weekly_sessions (object): Haftanın günlerine (Pazartesi, Salı vb.) göre düzenlenmiş çalışma oturumu dizilerini içeren ana yapı.

Her günün değeri bir dizi (array) olup, her dizi elemanı aşağıdaki alt alanları barındırr:

- session_id (string): StudyPlans ile FocusSessions koleksiyonu arasındaki ilişkiyi kuran, her çalışma oturumu için üretilen benzersiz referans anahtarı.

- course_id (string): Çalışlacak dersin benzersiz kimliği.

- course_name (string): Dersin kullanıcı tarafından görünen adı.

- planned_duration (number): Algoritma tarafindan o seans için belirlenen, dakika cinsinden planlanmış çalışma süresi.

- is_completed (boolean): Seansın fiilen gerçekleştirilip gerçekleştirilmediğini belirten bayrak. mark_session_completed fonksiyonu çağrıldığında true değerine güncellenir.

session_id alanı, planlanan bir seans ile fiilen gerçekleştirilen çalışma oturumunun (FocusSessions) birbiryle eşleştirilebilmesini sağlar. Bu sayede algoritma, planlanan süre (planned_duration) ile gerçek odak süresi arasındaki farkı analiz edebilir.

## 5.10.7 Çalısma Oturumu (Focus Sessions) Kolekisyonu

FocusSessions koleksiyonu, kullanıcınin kamera modülü eşliğinde yürüttüğü ve tamamladığı çalışma oturumlarına ait ölçüm verilerini barındırir. Her kayıt adaptif algoritmanın bir sonraki planı hesaplarken değerlendireceği gerçek zamanlı performans verisini temsil eder.

Her oturum dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id** (string): Oturumun ait olduğu kullanıcıya yönelik referans anahtarı.

- **study_plan_session_id** (*string*): StudyPlans koleksiyonundaki ilgili session_id değerine yönelik referans. Planlanan seans ile gerçekleştirilen oturum arasındaki bağ kurar.

- **course_id** (string): Çalısma yapılan derse ait referans anahtarı.

- actual_focus_time (number): Oturum süresince gerçekleşen toplam odak süresi (dakika, tam sayı).

- **head_tilt_degree** (number): Kamera modülünden elde edilen ortalama kafa eğim açısı (ondalıklı).

- **focus_score (number)**: Oturum genelinde hesaplanan odak skoru (ondalıklı). Görüntü işleme modülü tarafından iletilir ve algoritma tarafından girdi olarak tüketilir.

- status (string): Oturumun tamamlanma durumu (ör: "Completed").

- **timestamp** (*timestamp*): SERVER_TIMESTAMP ile otomatik atanan oturum bitiş zamanı.

## 5.10.8 Uygulama İzleme (WhiteList) Koleksiyonu

WhitelistSessions koleksiyonu, çalışma seansı süresince uygulama izleme modülü tarafından tespit edilen dikkat dağıtıcı uygulama ihlallerini kayıt altına alır. Her doküman tek bir çalışma oturumuna karşılık gelir ve o oturum boyunca gerçekleşen ihlalleri yapısal biçimde içerir.

Her izleme dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id** (*string*): İlgili kullanıcıya yönelik referans anahtarı.

- **focus_session_id** (string): FocusSessions koleksiyonundaki ilgili oturum dokümanına yönelik referans anahtari.

- **total_duration_seconds** (*number*): Oturumun toplam süresi, saniye cinsinden tam sayı olarak.

- violation_duration_seconds (number): İhlallerle geçen toplam süre, saniye cinsinden tam sayı olarak.

- **total_duration_hms** (string): Toplam sürenin SS:DD:SN formatında okunabilir biçimi.

- **violation_duration_hms** (*string*): İhlal süresinin SS:DD:SN formatında okunabilir biçimi.

- **violation_count** (*number*): violations dizisinin uzunluğundan otomatik hesaplanan toplam ihlal sayısı.

- violations (object[]): Her bir ihlale ait ayrını kayıtlarını içeren dizi. Her eleman; ihlal eden uygulamanın adını (app_name), ihlal süresini saniye ve okunabilir formatta (duration_seconds, duration_hms), ihlalin başlangıç ve bitiş zamanlarını (started_at, ended_at) barındırır.

- session_started_at (timestamp): Seans başlangıç zamanı.

- session_ended_at (timestamp): Seans bitiş zamanı.

- saved_at (timestamp): SERVER_TIMESTAMP ile otomatik atanan kayıt zamanı.

## 5.10.9 Sinavlar (Exams) Koleksiyonu

Exams koleksiyonu, kullanıcıın kayıtlı olduğunu dersler için tanımladığı sınav takvimi ve not verilerini depolar. Her doküman, bir kullanıcıya ait tüm sınav bilgilerini tek bir yapı altında toplar.

Her sınav dokümanı aşağıdaki alanlardan oluşmaktadir:

- **user_id** (string): İlgili kullanıcıya yönelik referans anahtar.

- exam_schedule_name (string): Sınav takvimine verilen ad.

- **updated_at** (timestamp): SERVER_TIMESTAMP ile otomatik atanan son güncelleme zamanı.

- **exams (object[]):** Derse özgü sınav bilgilerini içeren dizi. Her eleman; ilgili dersin referans anahtarını (course_id), sınav türünü (exam_type: "Vize", "Final" vb.), sınav tarihini (exam_date) ve sınav notunu (exam_grade) barındırr.

save_exam_schedule fonksiyonu çağrıldığında girilen not ve tarih bilgileri Courses koleksiyonundaki ilgili alanlara otomatik olarak yansıtılır. delete_exam_schedule işleminde ise silinen sınav takvimine bağlı derslerin not ve tarih alanları sıfirlanarak Courses koleksiyonunun tutarlılığı korunur.

## 5.10.10 İlişkiler ve Veri Bütünlüğü

FocuSync veritabanında koleksiyonlar arası ilişkiler, geleneksel ilişkisel veritabanlarındaki yabancı anahtar kısıtlaması mekanizması yerine referans anahtarlarının tutarlı biçimde kullanılmasıyla sağlanır. Ek-C'de sunulan veritabanı şemasında görüldüğü üzere tüm koleksiyonlar user_id, course_id, session_id ve focus_session_id gibi ortak referans değerleri aracılığıyla birbirine bağlanmaktadır. Şema yalnızca bu bağlantı noktalarını göstermek amacıyla oluşturulmuş olup her koleksiyonun tam alan yapısı ilgili alt bölümlerde ayrintilı biçimde açıklanmıştır.

Veri bütünlüğü, veritabanı motoru düzeyinde değil uygulama katmanında güvence altına alınır. Bu amaçla tüm veritabanı işlemleri; db_manager.py dosyasında tanımlı DatabaseManager sınifı altında merkezileştirilmiştir. Kod tabanının herhangi bir noktasından doğrudan veritabanına erişilmesi mimari olarak engellenmiş olup koleksiyonlar arası CASCADE güncellemeleri, referans tutarlılığı kontrolleri ve atomik yazma işlemleri bu sınif üzerinden yönetilir. Söz konusu merkezi yapı tutarsız veri durumlarının oluşmasını önlediği gibi sistemin bakımını ve hata tespitini de önemli ölçüde kolaylaştırir.

## 5.11 Mobil Kullanıcı Giriş Modülü

## 5.11.1 Amaç

Bu modül, FocuSync mobil uygulamasına kullanıcı erişimini yönetmektedir. Yeni kullanıcıların sisteme kayıt olmasını, mevcut kullanıcıların kimlik doğrulama yaparak oturum açmasını ve oturumun cihaz yerelinde kalıcı olarak saklanmasını sağlar. İlgili SRS gereksinimleri: AUTH-REQ-01/02, AUTH-ERR-01/02, DB-REQ-01/02/03.

## 5.11.2 Girdiler ve Çıktılar

Giriş (Sign In):

- Girdi: e-posta adresi (string), şifre (string)

- Çiktı: başarida null (hatasız), başarısızlkta kullanıcıya gösterilecek hata mesaj (string)

- Yan etki: başarılı girişte SharedPreferences'a user_id kaydedilir

## Kayit (Sign Up):

- Girdi: e-posta adresi (string), şifre (string), şifre tekrar (string)

- Çiktı: başarida null, başarısızlkta hata mesajı (string)

- Yan etki: Firestore Users koleksiyonuna yeni belge eklenir

## Çıkış (Sign Out):

- Girdi: yok

- Çiktı: yok

- Yan etki: SharedPreferences'tan user_id silinir

## 5.11.3 İşleyiş Mantığı

## Giriş Akışı:

Kullanıcı e-posta ve şifresini girdikten sonra "Giriş Yap" butonuna basar. DatabaseManager.signIn() metodu çağrılmadan önce aşağıldaki ön doğrulamalar gerçekleştirilir:

- Alanların boş olmadığı kontrol edilir.

- E-posta formatı regex ile doğrulanır (^[ \w- \. ]+@([ \w- ]+ \. )+[ \w- ]{2,4}$).

Ön doğrulamalar geçilirse Firestore Users koleksiyonunda email ve password alanlarina göre eşleşen belge sorgulanır. Eşleşen belge bulunursa belge ID'si (userId) SharedPreferences'a yazılır ve kullanıcı HomePage'e yönlendirilir.

## Kayıt Akışı:

DatabaseManager.signUp() metodunda sırasıyla şu kontroller yapılır: tüm alanlar doluluk kontrolü, e-posta format doğrulaması (regex), şifre uzunluğu kontrolü (minimum 6 karakter), şifre eşleşme kontrolü ve e-posta benzersizlik kontrolü (Firestore sorgusu). Tüm kontroller geçilirse Users koleksiyonuna yeni belge eklenir

## Oturum Kalıcılığ:

main.dart içinde uygulama başlatılırken SharedPreferences kontrol edilir. user_id mevcutsa LoginScreen atlanır ve kullanıcı doğrudan HomePage'e yönlendirilir. Bu sayede kullanıcı uygulamayı her açtığında yeniden giriş yapmak zorunda kalmaz.

## Internet Bağlantısı Kontrolü:

LoginScreen ve RegisterScreen, initState() içinde iki mekanizmayla bağlantı durumunu yönetir: _checkInitialConnection() açılış anindaki durumu tek seferlik okurken, onConnectivityChanged stream'i sayfa açık kaldığı sürece değişiklikleri anlık dinler. Bağlantı yokken ilgili buton onPressed: null konumuna alınır, rengi griye döner ve etiketi "İInternet

Bağlantısı Yok" olarak güncellenir. Ekran kapatıldığında _connectivitySubscription.cancel() ile bellek sızntısı önlenir.

## 5.11.4 Hata Durumlari

<table border="1"><tr><td>Hata Kodu</td><td>Durum</td><td>Gösterilen Mesaj</td></tr><tr><td>AUTH-ERR-01</td><td>E-posta veya şifre eşleşmedi</td><td>"E-posta veya Şifre hatalı."</td></tr><tr><td>AUTH-ERR-02</td><td>Geçersiz e-posta formatı</td><td>"Email formatına uymuyor."</td></tr><tr><td>—</td><td>Boş alan bırakıldı</td><td>"Lütfen tüm alanları doldurun."</td></tr><tr><td>—</td><td>Şifre 6 karakterden kısa</td><td>"Şifre en az 6 karakter olmalıdır."</td></tr><tr><td>—</td><td>Şifreler uyuşmuyor</td><td>"Şifreler uyuşmuyor."</td></tr><tr><td>—</td><td>E-posta zaten kayıtlı</td><td>"Bu e-posta zaten kullanımda."</td></tr><tr><td>DB-ERR-01</td><td>Firestore bağlantı hatası</td><td>"Bağlantı hatası oluştu." / "Kayıt sırasında hata oluştu."</td></tr></table>

Tüm hata mesajları ekranın alt kısmında SnackBar bileşeni aracılığıyla gösterilir.

## 5.11.5 Veritabanı Ekkileşimi

Modül yalnızca Users koleksiyonuyla etkileşime girer. Giriş işleminde iki alana göre where sorgusu (email, password) çalıştırılır. Kayıt işleminde once benzersizlik sorgusu ardından add() ile belge oluşturulur. Tüm Firestore işlemleri DatabaseManager sınılfi üzerinden yürütülür; ekranlar doğrudan Firestore API'sine erişmez.

## 5.12 Kullanıcı Arayüzü Tasarımı

## 5.12.1 Giriş / Kayıt Ekranı

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495551.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=zXwhQm1yS3VpjtHhzw0nnh3WabU%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.1. FocuSync Giriş ve Kayıt Ekranları

</div>

Giriş ve kayıt süreçleri, kullanıcı deneyimini tek bir pencere üzerinden yönetmek ve uygulama akışını kesintiye uğratmamak amacıyla katmanlı bir mimariyle tasarlanmıştır.

- Giriş Ekranı İşleyisi: Mevcut kullanıcıların sisteme erişimi için e-posta ve maskelenmiş parola verilerini toplar. Kullanıcı bilgileri girildiğinde sistem, veritabanı sorgusu öncesinde yerel bir format kontrolü yapar. Hatalı veya eksik veri girişleri, ana eylem butonunun hemen üzerinde yer alan dinamik uyarı etiketleri aracılığıyla kullanıcıya bildirilir.

- Kayıt Ekranı ve Veri Doğrulama: Yeni kullanıcıların hesap oluşturması için e-posta, minimum 6 karakter sınırına sahip şifre ve şifre onay verilerini toplar. Sistem, şifrelerin birbiriyle eşleştirini ve karakter sınırının sağlandığını doğrulamadan "Hesap Oluştur" işlemini başlatmaz. Bu yapı, veritabanına sadece geçerli ve tutarlı verilerin gönderilmesini garanti eder.

- Çevrimdışı (Offline) Durum Yönetimi: Uygulama, internet bağlantısının kesilmesi durumunda veri tutarsızlığın ve sunucu hatalarını önlemek amacıyla dinamik bir geri bildirim sistemi işletir. Bağlantı koptuğunda ekranın üst kısmında belirgin bir uyarı bandı aktifleşir. Bu durumda "Giriş Yap" veya "Hesap Oluştur" butonları otomatik

olarak devre dışı bırakılır ve buton metni "İInternet Bağlantısı Yok" olarak güncellenerek kullanıcının sistemle hatalı etkileşime girmesi engellenir.

- İşlevsel Yerleşim ve Navigasyon: Tüm form elemanları, kullanıcıının veri girişini yukaridan aşağıya doğru belirli bir hiyerarşide tamamlaması için dikey eksende sıralanmıştır. Ekranlar arası geçişler (Giriş/Kayıt arası değişim), bellek performansını optimize etmek ve geçiş gecikmelerini önlemek için aynı arayüz çerçevesi üzerinde katman değiştirme (Stacked UI) mantığıyla gerçekleştirilir.

## 5.12.2 Dashboard Ekrani

Dashboard ekranı, FocuSync sisteminin "komuta merkezi" olarak tasarlanmıştır. Kullanıcıin akademik durumunu, o günkü çalışma planını ve genel odaklanma başarısını tek bir bakışta görebilmesini sağlayan dinamik bir arayüzdür.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495557.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=oxIsk4DXHT%2BMKg0HhaOpIs%2FskMI%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.2. Dashboard Ekranı Genel Görünümü

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495563.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=C%2B6kNTX5UunKkMypJEO1YVMD%2FnI%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.3. Dashboard Ekranı - Akademik Risk ve Hedef Analizi

</div>

## İşlevsel Bileşenler ve Yerleşim:

- Karşılama ve Durum Paneli: Ekranın en üstünde kullanıcıyı ismiyle karşılayan bir selamlama metni ve sistemin o anki çalışma modunu (örn: "Firebase Modu Aktif") belirten durum göstergeleri bulunur.

- Özet İstatistik Kartları: Kullanıcıının motivasyonunu artırmak amacıyla en üst bölüme yerleştirilen üç ana veri kartından oluşur:

○ Toplam Seans: Kullanıcınin o güne kadar tamamladığı toplam odak oturumu sayısı.

○ Ortalama Odaklanma: Tüm oturumların yüzde bazlı başarı ortalaması.

○ En İyi Skor: Tek bir oturumda ulaşılan en yüksek odaklanma yüzdesi.

- Günlük Önerilen Program Akışı: StudyPlans koleksiyonundan çekilen verilerle oluşturulan bu bölümde, o güne ait çalışma seansları kronolojik bir liste (ScrollArea) şeklinde sunulur. Her seans kartı; ders kodunu, dersin adını, planlanan süreyi ve algoritmanın atadığı öncelik rozetini (Öncelikli, Orta, Düşük) içerir.

- Hızlı Erişim Navigasyonu: Sol tarafta yer alan dikey menü (Sidebar), kullanıcınin Dashboard'dan diğer modüllere (Ders Programı, Odak Modu, Whitelist vb.) anlık geçiş yapmasını sağlar.

## Tasarım Kararları ve UX Yaklaşımı:

- Veri Görselleştirme: Dashboard'daki grafikler ve ilerleme çubukları, kullanıcıın sayısal verileri bilişsel olarak daha hızlı işlemesi için fl_chart benzeri görsel kütüphanelerle desteklenir.

- Renk Kodlu Geri Bildirimler: Başarı skorları ve öncelik durumları; yeşil (yüksek), turuncu (orta) ve kırmızı (düşük/kritik) renk paletiyle işaretlenerek kullanıcınin dikkatini gereken noktalara yönlendirir.

- Asenkron Veri Yükleme: Dashboard açıldığında, arayüzün donmaması için veritabanı sorguları (db_manager) arka plan iş parçacıklarında (Threads) yürütülür ve veriler geldikçe arayüz dinamik olarak güncellenir.

- Reaktif Güncelleme: Kullanıcı bir odak seansını tamamladığında veya yeni bir ders eklediğinde, Dashboard üzerindeki istatistikler ve program akışı otomatik olarak yenilenerek "Tek Doğru Kaynağı" prensibini korur.

## 5.12.3 Ders Programi Ekrani

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495568.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=0RebiBqM11Zy0qQyLCotkTtf81I%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.4. Güncel Ders Programı Ekranı

</div>

Bu arayüz, sisteme başarıyla işlenmiş olan ders programının haftalık bazda takibini sağlar.

- Haftalık Ders Matrisi: Ekranın merkezini kaplayan ana bileşen, günleri (sütun) ve saat dilimlerini (satır) içeren bir izgara yapısidir. Dersler, bu matris üzerinde başlangıç ve bitiş saatlerine göre ilgili hücrelere yerleştirilir. Bu görsel hiyerarşı, kullanıcıın gün icindeki yoğunluğunu ve dersler arasındaki boş zamanlarını (çalışma seanslar için potansiyel vakitleri) anlık olarak saptamasına olanak tanır.

- İşlevsel Güncelleme ve Düzenleme: Sağ üst bölümde konumlandırılan (mavi) "Düzenle / Güncelle" butonu, kullanıcınin mevcut programı revize etme ihtiyacını karşılar. Bu buton, tek tiklama ile göruntüleme modundan düzenleme moduna geçişi

sağlayarak kullanıcıın veri akışını kesmeden hatalı kayıtlar düzeltmesine veya yeni bir program yüklemesine imkan tanır.

- Ders Bilgisi Görselleştirmesi: Her ders hücresi; dersin adı, kodu ve etkinlik türü (Teorik/Pratik) gibi temel bilgileri içerir. Bu sayede kullanıcı, detaylı bir menüye girmeden sadece ekranı tarayarak günlük akademik sorumluluklarını görebilir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495581.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=4MzmT8QtTEeyd6m3CezeDJTMfkI%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.5. Ders Programı Yükleme ve Düzeltme Ekranı

</div>

Bu arayüz, program verilerinin sisteme ilk girişini ve yapay zeka (OCR) tarafindan çözümlenen verilerin kullanıcı tarafindan denetlenmesini sağlar.

- Yükleme Alanı: Ekranın merkezinde yer alan geniş, kesik çizgili (Dashed Border) alan, dosya yükleme işlemini görsel olarak ön plana çıkarır. Bu tasarım, kullanıcıının karmaşık menüler arasında dolaşmadan doğrudan ana eyleme (dosya seçimi) odaklanmasını sağlar. Büyük ikon ve yönlendirici metin kullanımı, işlemin basitliğini vurgulayan bir UX tercihidir.

- Interaktif Düzenleme Tablosu (Editor Mode): PDF veya görsel dosya analiz edildikten sonra arayüz, verileri düzenlenebilir bir tablo formatına dönüştürür. Her ders kaydı; kod, ders adı ve zaman dilimi bazında hücrelere ayrılır. Bu yapı, kullanıcınin yapay zeka tarafından yanlış okunan veya eksik kalan kısımlari hücre bazında anlık olarak manuel düzeltmesine imkan tanır.

- Doğrudan Veri Denetimi: Kullanıcı, ekstra onay kutuları yerine doğrudan düzenlenebilir tablo hücreleri üzerinden verilere müdahale eder. Hatalı okunan ders kodları anında düzeltilir, gereksiz satırlar silinerek veya eklenerek sisteme kaydedilecek nihai veri paketi oluşturulur.

- Kayıt ve Navigasyon Akışı: Düzenlemeler tamamlandığında ana kayıt butonu ile veriler Firestore'a asenkron olarak iletilir. İşlemden vazgeçilmesi durumunda ise üst navigasyonda yer alan "Geri Dön" butonu kullanilarak hatalı veri aktarımı engellenir ve ana görünüme geçilir.

- Dinamik Geri Bildirim ve Durum Mesajları: Analiz süreci boyunca kullanıcıya işlemin devam ettiğine dair görsel geri bildirimler sunulur. Hatalı dosya formatı veya okuma başarısızlığı durumunda, ekran üzerinde beliren uyarilar kullanıcıyı doğru işlem adımına yönlendirir.

## 5.12.4 Notlar Ekranı

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495587.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=iiYQDyWY5Zhz%2FT%2BYg5Dxr%2Bm%2B6AA%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.6. Kayıtlı Notlar Görünüm

</div>

Notlar modülünün ana ekranı (Görüntüleme Modu), kullanıcıının yaklaşan sınavlarını ve mevcut akademik başarısını güvenli bir şekilde analiz etmesi için salt okunur (read-only) bir mimaride tasarlanmıştır.

- Dinamik Önceliklendirme Paneli: Ekranın üst bölümünde yer alan akıllı analiz etiketi, takvimdeki tarihleri mevcut günle karşılaştırarak "En Yakın Sınavı" ve kalan süreyi (Örn: "BUGÜN!") hesaplar. Bu özellik, kullanıcınin acil akademik yükümlülüklerine anında odaklanmasını sağlayan yönlendirici bir UX kararidır.

- Salt Okunur Veri Matrisi: Sınav ve not kayıtları; Tarih, Saat, Ders Bilgisi, Tür, Salon ve Not sütunlarından oluşan yapısal bir tabloda sunulur. Yanlışlıkla veri değiştirilmesini önlemek amacıyla tablo hücreleri dışarından müdahaleye tamamen kapatılmıştır (NoEditTriggers).

- Erişim ve Yıkıcı İşlem Kontrolü: Sayfanın alt kısmında yer alan aksiyon butonları, görüntüleme ve veri düzenleme (State) akışlarını birbirinden ayırır. Mavi "Düzenle / Yükle" butonu veri akışını kesintisiz olarak editör katmanına geçirken; kırmızı "Tüm Notları Sil" butonu, sistem genelindeki notların (Course kartlarındaki dahil) silinmesi gibi yıkıcı bir işlem barındırdigindan ek bir onay diyalogu (Confirmation) ile koruma altına alınmıştır.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495593.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=Y4G0elWBMIjcBtAm4KxV6WsQsYk%3D&Expires=1779181295' alt='OCR图片'/></div>

## Şekil 5.7. Notlar Düzenleme ve Sınav Programı Ekleme Ekranı

Bu arayüz, kullanıcıların manuel olarak not/sınav girişi yapmasını veya PDF/Görsel üzerinden yapay zeka (OCR) destekli belge aktarımını tek bir ekranda yönetmesini sağlar.

- Bütünleşik OCR ve Düzenleme Katmanı: Ekranın üst kısmında yer alan sürüklebirak destekli dosya yükleme alanı, OCR modülünü tetikler. Okunan veriler, doğrudan alt kısımdaki düzenlenebilir hücrelerden oluşan tabloya aktarilarak kullanıcıyla anında denetim ve düzeltme imkanı sunar.

- Akıllı Seçim Mekanizması (Smart Selection): Tablonun en solunda yer alan onay kutuları (Checkbox), sisteme aktarılacak verilerin filtrelenmesi için kullanılır. Yapay zeka taraması sonrası sistem, okunan dersleri kullanıcının mevcut aktif ders havuzuyla çapraz kontrole sokar ve yalnızca eşleşen dersleri otomatik olarak işaretler. Sadece işaretli satırlar veritabanına işlenir.

- Dinamik Veri Denetimleri: Form hatalarını minimuma indirmek için hücrelere özel akıllı bileşenler kodlanmıştır. "Sınav Türü" hücresi, seçilen türe göre (Örn: Vize) otomatik sıra numarası açarken, tekil sınavlarda (Final, Bütünleme) bu

numaralandırmayı gizler. "Not" sütunu ise veri tutarlılığın sağlamak amacıyla donanımsal olarak maksimum 100 değerine sabitlenmiştir (QIntValidator).

- Kayıt Akışı ve Güvenli Çıkış: Onay sürecini tamamlayan kullanıcı, ekranın altında merkezi olarak konumlandırılan geniş "Seçilenleri Kaydet" butonu ile asenkron yazma işlemini başlatır. Hatalı dosya yüklemelerinde veya işlemden vazgeçilmesi durumunda, ekranın en üstündeki "İptal / Geri Dön" navigasyonu kullanilarak veritabanına hiçbir kirli veri gönderilmeden ana okuma moduna dönülür.

## 5.12.5 Odak Modu Ekrani:

Odak Modu arayüzü, kullanıcınin seçtiği bir ders için çalışma seansını yürüttüğü ve arka planda çalışan Kafa Takibi (Göruntü İşleme) modülünün görsel geri bildirimlerini barındiran ana çalışma panelidir. Arayüz tasarımı, kullanıcınin dikkatini dağıtmayacak şekilde sade, karanlık tema ağırlıklı ve modüler kartlardan (QFrame) oluşmaktadir.

Arayüz dört ana görsel bileşenden oluşur:

- Kamera ve Canlı Önizleme Alanı (Live Feed): Ekranın sol üst bölümünü kaplayan bu geniş alan, oturum başladığında kullanıcının kendi görüntüsünü anlık olarak takip edebilmesini sağlar. Kullanicının arka plan gizliliğinden emin olması ve kameranın doğru konumlandırıldığın teyit edebilmesi için tasarlanmıştır.

- Seans Süresi ve Başlatma Kontrolleri: Sol alt kartta, seans süresini gösteren büyük puntolu (48px) bir dijital kronometre bulunur. Kronometrenin sağında, kullanıcıin veritabanindan çekilen aktif dersleri ("Ders Kodu - Ders Adı" formatında) seçebilecegi bir açılır menü (QComboBox) ve seansı yöneten "Başlat/Bitir" butonu konumlandırılmıştır.

- Dinamik Odak Skoru Halkası: Sağ panelde yer alan bu bileşen (FocusCircle), arka plan iş parçacığindan gelen gerçek zamanlı hesaplamalara göre anlık başarı yüzdesini yansıtır. İlerleme çubuğunun rengi, odak skoruna bağlı olarak dinamik bir şekilde yeşil, turuncu veya kırmızı tonlarına geçiş yaparak kullanıcıya durumunu hissettirir.

- Uyarı ve Bildirim Katmanı (Notification System): Kullanıcının dikkati dağıldığında arayüzün üst kısmında renkli bir bildirim bandı (NotificationBanner) belirir. Ayrıca uygulamanın arka planda (küçültülmüş) çalışması ihtimaline karşı, işletim sistemi seviyesinde diğer pencerelerin üstüne çıkan (WindowStaysOnTopHint) ve sistem uyarı sesi çalışan bağımsız bir Pop-up penceresi (DistractionAlertDialog) devreye girerek kullanıcıyı derse dönmeye davet eder.

## 5.12.6 Whitelist Yönetim Ekranı

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495599.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=nisOEorurs%2FeG%2BaPEISioehG1h0%3D&Expires=1779181295' alt='OCR图片'/></div>

## Şekil 5.8. Whitelist Yönetim Ekranı ve Uygulama Seçim Diyalogları

Bu ekran, kullanıcınin odak oturumları sırasında izin verilecek masaüstü uygulamalarını yönetmesi için tasarlanmıştır. Arayüzün temel amacı, whitelist mantığını kullanıcı açısından görünür ve kolay yönetilebilir hale getirmektir. Ekranın üst bölümünde “Beyaz Liste & Denetim” başlığı ve kısa açıklama metni yer alır; bu açıklama, whitelist'e eklenen `.exe` dosyaları dışındaki aktif kullanıcı uygulamalarının ihlal sayılacağını ve sistem uygulamalarının otomatik olarak izinli kabul edildiğini kullanıcıya açık biçimde bildirir. Arayüz, karanlık tema, yüksek kontrastlı başlıklar ve durum renkleri ile FocuSync’in genel görsel diliyle uyumlu şekilde tasarlanmıştır.

- Çoklu Uygulama Ekleme Mekanizması: Ekran, whitelist'e uygulama eklemek için üç farklı giriş yolu sunar. Birinci yöntem “Kurulu Uygulamalardan Ekle” butonudur; bu işlem Windows Registry üzerinden algılanan kurulu yazılımları ayrı bir seçim penceresinde listeler. İkinci yöntem “Dosyadan .exe Seç” butonudur; bu seçenek işletim sisteminin standart dosya seçme penceresini açarak kullanıcınin doğrudan bir çalıştırılabilir dosya belirlemesine izin verir. Üçüncü yöntem ise manuel giriş alanıdır; kullanıcı örneğin `chrome.exe` gibi doğrudan exe adını yazarak “Elle Ekle” işlemini başlatabilir. Bu çoklu yapı, hem teknik bilgisi yüksek kullanıcılar hem de daha görsel seçim yapmak isteyen kullanıcılar desteklemek amacıyla tercih edilmiştir.

- Kurulu Uygulama Seçim Diyaloğu: “Kurulu Uygulamalardan Ekle” akışı, ayrı bir `InstalledAppsDialog` penceresi üzerinden yürütülür. Bu pencere icinde bir arama kutusu, eşleşen uygulamaların listesi ve “Seçili Uygulamayı Ekle” butonu bulunur. Arama işlemi yalnızca uygulama adına değil, exe adına, yayıncı bilgisine ve exe yoluna

göre de filtreleme yapar. Ayrıca ekranda “Gösterilen uygulama sayısı” etiketi yer alarak kullanıcıın filtreleme sonucunu anlık görmesi sağlanır. Liste öğeleri çift tıklama ile de seçilebilir. Bu tasarım, çok sayída kurulu uygulama bulunan sistemlerde hedef uygulamaya hızlı erişim sağlamak için geliştirilmiştir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495606.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=5Q1bAHS3RPM3WON%2Fi4Nu8DeUCUc%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.9. Kurulu uygulamalardan whitelist e uygulama ekleme penceresi

</div>

- Manuel Giriş ve Liste Yönetimi: Ana whitelist ekranında yer alan manuel giriş alanı, doğrudan exe adı kabul edecek şekilde yapılandırılmıştır ve Enter tuşu ile de çalıştırılabilir. Kullanıcı tarafından eklenen uygulamalar, “İzin Verilen Uygulamalar” başlığı altında bir `QListWidget` içinde gösterilir. Liste alanı, seçili öğeyi görsel olarak belirgin hale getiren renkli seçim durumu ile tasarlanmıştır. Kullanıcı, “Seçili Girişi Kaldır” butonu ile listedeki bir exe kaydını silebilir. Bu yapı, whitelist’in yalnızca oluşturulmasını değil, aynı zamanda düzenli olarak guncellenmesini de destekler.

- Hızlı İzin Verme Akışı: Arayüzde ayrica “Son İhlale İzin Ver” işlevi için ayrı bir buton ve `Ctrl+Shift+A` klavye kısayolu tanımlanmıştır. Bu özellik, kullanıcı ihlal durumunda olan son uygulamayı tek adımda whitelist'e eklemek istediğinde hızlı bir düzeltme sağlar. Buton varsayılan olarak yalnızca sistemde “son ihlal” bilgisi mevcut olduğunda aktif hale gelir; aktif olduğunda buton metni ilgili exe adıyla güncellenir. Bu yaklaşım, kullanıcıyi ihlal ekranından whitelist yönetimine geri dönüp aynı uygulamayı tekrar aramak zorunda bırakmadan akışı hızlandırir.

- Durum Paneli ve Geribildirim Tasarımı: Ekranın alt bölümünde yer alan durum paneli, whitelist sisteminin o anki çalışmasını özetleyen üç temel bilgi sunar: ihlal durumu, tespit edilen uygulama ve izleme durumu. İhlal yokken panel nötr veya yeşil

tonlarda "İhlal: Yok" geri bildirimi verir; ihlal algılandığında ise turuncu vurgu ile "İhlal: EVET" ifadesi gösterilir ve ilgili uygulama adı detay satırında belirtilir. İzleme süreci aktif değilse "İzleme: Kapalı", aktifse "İzleme: Açık" etiketi gösterilir. Böylece kullanıcı, whitelist denetiminin yalnızca ayar ekranını değil aynı zamanda canlı sistem durumunu da aynı yerden takip edebilir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495612.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=hqDWiSWn3ydtMUhKdzDaJC5YWfk%3D&Expires=1779181295' alt='OCR图片'/></div>

<div align="center">

Şekil 5.10. Pop-up Uyari Penceresi

</div>

- Pop-up Uyarı Penceresi: İhlal oluştuğunda ana ekran üzerindeki durum paneline ek olarak ayrı bir `ViolationAlertDialog` penceresi açılır. Bu pencere her zaman üstte kalacak sekilde yapılandırılmıştır ve “Whitelist ihlali algılandı” mesajı ile birlikte tespit edilen uygulamayı gösterir. Pencerede ayrıca, ihlal yapan uygulama kapandığında bu uyarının otomatik olarak kapanacağını belirten açıklayıcı metin yer alır. Böylece kullanıcı ana arayüzü takip etmese bile ihlal durumundan doğrudan haberdar edilir. Kod tasarımında bu pop-up, sesli uyarı mekanizmasıyla birlikte çalışacak sekilde kurgulanmıştır.

- Hata ve Platform Uyum Geri Bildirimi:Arayüz, kullanıcı hataları ve platform kısıtları için doğrudan geri bildirim üretir. Örneğin listeden bir öge seçmeden silme işlemi yapılırsa uyarı mesajı gösterilir. Kurulu uygulamalardan eklemeözelliği yalnızca Windows için etkinleştirilmiştir; desteklenmeyen platformlarda kullanıcıya bu durum açıkça bildirilir. Benzer şekilde, kurulu uygulama listesi alınamazsa kullanıcıya dosyadan `\.exe` seçme seçeneğini kullanabileceği bilgisi verilir. Bu tasarım, ekranın yalnızca işlevsel değil aynı zamanda yönlendirici ve hata toleranslı olmasını sağlar.

## 5.12.7 İstatistikler Ekranı

FocuSync sisteminde istatistikler ayrı bir sayfa yerine Dashboard ekranına entegre edilmiş bir panel olarak sunulur. Bu tasarım kararı, kullanıcıının uygulamayı açtığı anda mevcut durumunu ve gelişim trendini ek bir navigasyon işlemi yapmadan görmesini sağlar.

Görselleştirme ve Analiz Bileşenleri:

- Performans Özet Kartları: Dashboard'un üst kısmında, kullanıcıin genel başarısını simgeleyen üç ana veri kartı bulunur:

○ Toplam Seans: FocusSessions koleksiyonundan çekilen, tamamlanmış toplam oturum sayısı.

○ Ortalama Odaklanma: Tüm geçmiş oturumların focus_score değerlerinin ortalaması.

○ En Yüksek Skor: Tek bir oturumda ulaşılan maksimum başarı yüzdesi.

- Odaklanma Skoru Trendi (Grafik Paneli): Dashboard'un merkezinde yer alan bu grafik, kullanıcının zaman içindeki performans değişimini izler.

○ Dinamik Çizgi Grafik: Seans sırasına göre odaklanma skorlarını birbirine bağlayan bir Line Chart yapısı kullanılır.

○ Renk Kodlu Veri Noktaları: Skorlara göre noktalar yeşil (≥%75), turuncu (≥%50) ve kırmızı (<%50) olarak renklendirilerek görsel bir performans eşiği sunulur.

- Geçmiş Seanslar Listesi: Grafişin altında, oturumların detaylı dökümü yer alır. Her kayıt; ders kodu, tarih-saat, net odak süresi ve kafa eğim açısı gibi FocusSessions koleksiyonundan gelen teknik verileri içerir.

Teknik İşleyiş:

- Veri Senkronizasyonu: Dashboard her yüklendiğinde (showEvent), DatabaseManager üzerinden en güncel oturum verileri asenkron olarak çekilir ve grafikler çalışma anında (runtime) yeniden çizilir.

- Görsel Geri Bildirim: İstatistiksel veriler, sadece bilgilendirme amaçlı değil, aynı zamanda kullanıcının çalışma alışkanlıklarını iyileştirmesi için bir aynalama (mirroring) aracı olarak kullanılır.

## 5.12.8 Mobil Arayüz Ekranlari

## Giriş Ekranı

E-posta ve şifre alanlarından oluşan giriş sayfasıdır. Şifre alanının yanındaki göz simgesiyle şifre görünürlüğü değiştirilebilir. Internet bağlantısı mevcut olduğunda "Giriş Yap" butonu aktif ve yeşil renktedir. Hesabı olmayan kullanıcılar "Kayıt Ol" butonuyla kayıt ekranına yönlendirilir.

## Giriş Ekranı - Çevrimdışı Durum

İnternet bağlantısı kesildiğinde ekranın üst kısmında kırmızı bir uyarı bandı belirir ve "Giriş Yap" butonu griye dönerek "İInternet Bağlantısı Yok" etiketini gösterir, buton devre dışı kalır.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495620.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=7bhorWbn4IQ562Xvig0gBNsKQHU%3D&Expires=1779181295' alt='OCR图片'/></div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_2_1778576495626.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=7mWv9cJ3eetxv94VMJCePEC726M%3D&Expires=1779181295' alt='OCR图片'/></div>

## Kayıt Ekranı

Yeni kullanıcıların hesap oluşturduğu ekrandır. E-posta, şifre (en az 6 karakter) ve şifre tekrar alanlarını içerir. Tüm doğrulamalar tamamlandığında "Hesap Oluştur" butonu ile kayıt işlemi tamamlanır. Mevcut hesabı olanlar "Giriş Yap" bağlantısıyla giriş ekranına dönebilir.

## Kayıt Ekranı - Çevrimdışı Durum

İnternet bağlantısı kesildiğinde ekranın üst kısmında kırmızı bir uyarı bandı belirir ve "Hesap Oluştur" butonu devre dışı kalarak "İnternet Bağlantısı Yok" olarak değişir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495636.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=Dqoe%2Fob0YRvLvTdImU08856RMLk%3D&Expires=1779181295' alt='OCR图片'/></div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_2_1778576495642.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=h2PAHeWJoAHdPqFpkBs8huKD55Q%3D&Expires=1779181295' alt='OCR图片'/></div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495648.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=RQ%2BQO1fG4W4dXC5Fvd8KCAjf56g%3D&Expires=1779181295' alt='OCR图片'/></div>

## Ana Sayfa

Kimliği doğrulanmış kullanıcıının karşılandığı ana ekrandir. Masaüstü uygulamasının ürettiği akıllı çalışma planı, gün başlıklar altında ders kartları şeklinde listelenir. Her kart ders kodu, ders adı, önerilen süre ve öncelik rozetini (Öncelikli / Orta / Düşük) renk kodlu biçimde gösterir. Üst çubukta performans, profil ve çıkış simgeleri yer alır.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_2_1778576495654.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=%2F8%2Fgk77U7Jtxn2bkyaW6fw%2FvMcU%3D&Expires=1779181295' alt='OCR图片'/></div>

## Haftalik Program

Kullanıcının ders programını gösteren sekmedir. Dersler güne göre gruplandırılmış kartlar halinde listelenir. Her kartta ders kodu, ders adı ve saat aralığı görüntülenir. Sol kenardaki renkli serit her dersin türüne özgü rengi gösterir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495678.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=GnF8gqZDcU9DJulOKa8l%2BggRhyU%3D&Expires=1779181295' alt='OCR图片'/></div>

## Sinavlar

Kullanıcıının sınav takvimini ve sınav notlarını bir arada sunan sekmedir. Her ders için vize ve final sınavları ayrı kartlar halinde gösterilir. Kart üzerinde sınav türü, tarih, saat, sınif bilgisi ve varsa alınan not yer alır.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_2_1778576495690.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=6vxc2c4YqTr3au8qMpUOGB1vkuk%3D&Expires=1779181295' alt='OCR图片'/></div>

## Dersler

Kullanıcının aktif derslerini detaylı biçimde listeleyen sekmedir. Her ders kartında zorluk puanı, haftalık ders saati, hedef not, güncel not ortalaması ve dönem içi sınav notları gösterilir. Hedef not belirlenmemiş dersler "Belirlenmedi", ağırlık tanımlanmamış dersler ise "Hesaplanamıyor" etiketiyle işaretlenir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495695.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=ICnZT%2BjEAVACE%2BAWRgG9h5XwY48%3D&Expires=1779181295' alt='OCR图片'/></div>

## Profil Ayarlari

Kullanıcının ad, soyad ve okul bilgilerini düzenleyebildiği ekrandır. E-posta adresi salt okunur olarak gösterilir ve değiştirilemez. Ekranın alt bölümündeki "Güvenlik ve Şifre" alanı aracılığıyla mevcut şifre doğrulandiktan sonra yeni şifre belirlenebilir. "Değişiklikleri Kaydet" butonu tüm güncellemeleri tek işlemde Firestore'a yazar.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_2_1778576495710.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=7eqzNwLKVjKH9KWJPod%2FUFzkDEU%3D&Expires=1779181295' alt='OCR图片'/></div>

## Performans

Kullanicının tamamlanmış odak oturumlarını görselleştiren ekrandir. Üst kısımda toplam seans sayısı, ortalama odaklanma skoru ve en yüksek skor özet kartlarda sunulur. Ortada seans sırasına göre odaklanma skoru trendini gösteren çizgi grafik yer alır. Veri noktaları skora göre yeşil (≥75%), turuncu (≥50%) ve kırmızı (<50%) olarak renklenir. Alt kısımda her geçmiş seans ders kodu, tarih saat, odak süresi ve kafa eğim açısı bilgileriyle kartlar halinde listelenir.

## 6. Gereksinimlerin İzlenebilirliği

Bu bölümün amacı, Software Requirements Specification (SRS) dokümanında tanımlanan gereksinimlerin, Software Design Description (SDD) dokümanında tanımlanan tasarım bileşenleri ile olan ilişkisini sistematik biçimde ortaya koymaktadır. Gereksinimlerin izlenebilirliğini sağlanması; her bir gereksinimin tasarım düzeyinde hangi bileşen tarafından karşılandığının gösterilmesi, tasarım kararlarının gerekçelendirilmesi ve ilerleyen doğrulama/doğrulama faaliyetlerinde referans buttünlüğünün korunması açısından kritik öneme sahiptir. Bu kapsamda izlenebilirlik hem ileri yönlü hem de geri yönlü olarak ele alınmıştır. İleri yönlü izlenebilirlikte, SRS gereksinimlerinin hangi tasarım modülleri tarafından karşılandığı gösterilmekte; geri yönlü izlenebilirlikte ise her tasarım modülünün hangi gereksinimlere hizmet ettiği ortaya konulmaktadır.

## 6.1 SRS Gereksinimlerinden Tasarım Bileşenlerine İzlenebilirlik

Bu alt bölümde, SRS dokümanında tanımlanmış olan fonksiyonel ve fonksiyonel olmayan gereksinimlerin, SDD içerisinde tanımlanan ilgili tasarım bileşenlerine eşlenmesi sunulmaktadır. FocuSync sisteminde gereksinimler; kullanıcı arayüzü, donanım arayüzü, yazılım arayüzü, iletişim, kullanıcı giriş sistemi, ders yönetimi, program ve sınav yönetimi, odak oturumu yönetimi, kafa takibi, beyaz liste kontrolü, adaptif zorluk güncelleme, istatistik ve raporlama ile mobil senkronizasyon gibi başlıklar altında tanımlanmıştır. SDD tarafında ise bu gereksinimlere karşılık gelen modüller 5.1 ile 5.12 arasındaki ayrintilı tasarım bileşenleri altında ele alınmıştır.

Bu bağlamda kullanıcı girişine ilişkin AUTH-REQ ve AUTH-ERR kodlu gereksinimler, esas olarak 5.1 Kullanıcı Giriş ve Profil Modülü, 5.10 Veritabanı Tasarımı ve 5.11 Mobil Kullanıcı Giriş Modülü tarafından karşılanmaktadır. Benzer şekilde derslerin oluşturulması, saklanması ve guncellenmesine ilişkin COURSE-REQ ve ilişkili DB gereksinimleri, 5.2 Ders Yönetimi Modülü ile 5.7 Adaptif Zorluk Guncelleme Modülü tarafından desteklenmektedir. Program ve sınav yönetimi ile OCR tabanlı veri alma süreçlerine ilişkin OCR-REQ ve OCR-ERR gereksinimleri ise 5.3 Program ve Sınav Yönetimi Modülü ile 5.12 Kullanıcı Arayüzü Tasarımı bileşenleri altında gerçekleştirilmiştir.

Odak oturumu başlatma, sürdürme, sonlandırma ve oturum verisinin kaydedilmesine ilişkin FSS gereksinimleri, 5.4 Odak Oturumu Yönetimi Modülü ile karşılanmaktadır. Kamera üzerinden yüz ve kafa yönü takibi, odak skorunun hesaplanması ve bu süreçte arayüzün donmadan çalışmasının sağlanmasına ilişkin gereksinimler ise 5.5 Kafa Takibi ve Odak Skoru Modülü ile ilişkilidir. Beyaz liste yönetimi, aktif uygulama izleme, ihlal tespiti, uyarı üretimi ve ihlal süresi hesaplaması gibi gereksinimler 5.6 Whitelist Kontrol Modülü içerisinde karşılanmaktadır.

Adaptif zorluk güncelleme, odak verileri ve beyaz liste ihlallerinden beslenen dinamik karar mekanizmasına dayanmaktadır. Bu nedenle ADG-REQ ve ilişkili veritabanı gereksinimleri, başta 5.7 Adaptif Zorluk Güncelleme Modülü olmak üzere 5.2 Ders Yönetimi, 5.5 Kafa Takibi

ve Odak Skoru, 5.6 Whitelist Kontrol ve 5.10 Veritabanı Tasarımı bileşenleri ile karşılanmaktadır. İstatistik ve raporlama işlevlerine ilişkin IVR gereksinimleri ise 5.8 İstatistik ve Raporlama Modülü üzerinden sağlanmaktadır. Mobil platform ile veri paylaşımı, senkronizasyon ve giriş işlemleri bakımından tanımlanan MS-REQ ailesi ise 5.9 Mobil Senkronizasyon, 5.10 Veritabanı Tasarımı ve 5.11 Mobil Kullanıcı Giriş Modülü tarafından karşılanmaktadır.

Sonuç olarak, SRS dokümanında tanımlanan gereksinimlerin tamamı SDD içerisinde karşılık gelen modüller ile eşlenebilmekte; özellikle veritabanı, odak yönetimi, kafa takibi, beyaz liste ve mobil senkronizasyon bileşenlerinin sistem çapında yatay sorumluluk üstlendigi görülmektedir. Bu durum, tasarımın gereksinim temelli olarak oluşturulduğunu ve modüller arası ilişkilerin sistematik biçimde tanımlandığı nı göstermektedir.

<table border="1"><tr><td>SRS Gereksinim Kümesi</td><td>Karşılayan Tasarım Bileşen(ler)i</td><td>Açıklama</td></tr><tr><td>REQ-UI-01</td><td>5.3 Program ve Sınav Yönetimi,5.12 Kullanıcı Arayüzü Tasarımı</td><td>Ders programı ve sınav tarihleri için manuel/PDF tabanlı arayüz tasarımı bu bileşenlerde karşılanır.</td></tr><tr><td>REQ-UI-02</td><td>5.4 Odak Oturumu Yönetimi,5.5 Kafa Takibi ve Odak Skoru,5.6 Whitelist Kontrol,5.12 Kullanıcı Arayüzü Tasarımı</td><td>Dikkat dağılması,yüz algılanamaması ve whitelist ihlali durumlarındaki görsel/sesli uyarılar bu bileşenler tarafından üretilir.</td></tr><tr><td>REQ-UI-03</td><td>5.9 Mobil Senkronizasyon,5.11 Mobil Kullanıcı Giriş,5.12 Kullanıcı Arayüzü Tasarımı</td><td>Mobil giriş/kayıt ekranlar ile senkronize veri görüntüleme işlevi bu tasarım bileşenleriyle sağlanır.</td></tr><tr><td>REQ-HW-01</td><td>5.5 Kafa Takibi ve Odak Skoru,5.4 Odak Oturumu Yönetimi</td><td>Kamera erişimi ve görüntü akışının odak oturumu içinde kullanılması bu modüllerde tanımlanır.</td></tr><tr><td>REQ-HW-02</td><td>5.4 Odak Oturumu Yönetimi,5.5 Kafa Takibi ve Odak Skoru,5.6 Whitelist Kontrol</td><td>Sesli uyarılar hem odak hem de whitelist ihlali bağlamında bu modüllerce üretilir.</td></tr></table>

<table border="1"><tr><td>REQ-SW-01</td><td>5.6 Whitelist Kontrol</td><td>İşletim sistemi süreç/pencere yönetimi ve izinli uygulama denetimi whitelist modülünde tasarlanmıştır.</td></tr><tr><td>REQ-SW-02, REQ-COMM-01</td><td>5.9 Mobil Senkronizasyon, 5.10 Veritabanı Tasarımı, 5.11 Mobil Kullanıcı Giriş</td><td>Firebase tabanlı veri saklama, senkronizasyon ve asenkron iletişim bu bileşenlerde karşılanır.</td></tr><tr><td>AUTH-REQ, AUTH-ERR, DB-REQ-01/02/03, DB-ERR-01</td><td>5.1 Kullanıcı Giriş ve Profil, 5.10 Veritabanı Tasarımı, 5.11 Mobil Kullanıcı Giriş</td><td>Kimlik doğrulama, kullanıcı kaydı,hata yönetimi ve merkezi veritabanı erişimi burada ele alınır.</td></tr><tr><td>COURSE-REQ, DB-REQ-04/05</td><td>5.2 Ders Yönetimi, 5.7 Adaptif Zorluk Güncelleme, 5.10 Veritabanı Tasarımı</td><td>Derslerin tutulması,zorluk katsayısının güncellenmesi ve stratejinin kaydedilmesi bu modüllerde gerçekleştirilir.</td></tr><tr><td>OCR-REQ, OCR-ERR, DB-REQ-06, DB-ERR-02</td><td>5.3 Program ve Sınav Yönetimi, 5.10 Veritabanı Tasarımı, 5.12 Kullanıcı Arayüzü Tasarımı</td><td>PDF yükleme, OCR ile veri çıkarımı, doğrulama ve veritabanına yazma süreci burada tasarlanmıştır.</td></tr><tr><td>FSS-REQ, FSS-ERR, FSS-PERF</td><td>5.4 Odak Oturumu Yönetimi, 5.5 Kafa Takibi ve Odak Skoru, 5.10 Veritabanı Tasarımı</td><td>Oturum başlatma/durdurma,sayaç,veri kaydı ve kafa takibi entegrasyon bu modüllerde bulunur.</td></tr><tr><td>HTS-REQ, HTS-ERR, HTS-PERF</td><td>5.5 Kafa Takibi ve Odak Skoru, 5.4 Odak Oturumu Yönetimi, 5.10 Veritabanı Tasarımı</td><td>Kamera akışı,yüz/landmark analizi,açı hesabı,odak skoru ve performans hedefleri burada karşılanır.</td></tr><tr><td>WL-REQ, WL-ERR, WL-PERF, DB-REQ-07/08/09</td><td>5.6 Whitelist Kontrol, 5.4 Odak Oturumu Yönetimi, 5.8 İstatistik ve Raporlama, 5.10 Veritabanı Tasarımı</td><td>İzinli uygulama yönetimi,ihlal tespiti,ihlal özeti,focus session ilişkilendirmesi ve raporlamaya veri sağlama bu modüllerde yer alır.</td></tr></table>

<table border="1"><tr><td>ADG-REQ, ADG-ERR, DB-REQ-10</td><td>5.7 Adaptif Zorluk Güncelleme,5.2 Ders Yönetimi,5.5 Kafa Takibi ve Odak Skoru,5.6 Whitelist Kontrol,5.10 Veritabanı Tasarımı</td><td>Odak skoru ve whitelist verileri kullanılarak ders zorluğu güncellenir ve yeni strateji oluşturulur.</td></tr><tr><td>IVR-REQ, IVR-ERR</td><td>5.8 İstatistik ve Raporlama,5.6 Whitelist Kontrol,5.10 Veritabanı Tasarımı</td><td>Günlük/haftalık performans özeti,dikkat dağıtıcı analizi ve veri çekme hataları bu bileşenlerle karşılanır.</td></tr><tr><td>MS-REQ, MS-PERF, MS-ERR</td><td>5.9 Mobil Senkronizasyon,5.10 Veritabanı Tasarımı,5.11 Mobil Kullanıcı Giriş</td><td>Mobil veri erişimi, senkronizasyon hızı ve bağlantı kesintisi yönetimi bu modüllerde tanımlanmıştır.</td></tr><tr><td>SYS-REQ-01,SYS-REQ-10/11/12/14</td><td>3.6 Gerçek Zamanlı İşleme ve Multithreading Kararları,3.8 Gizlilik ve Kamera Verisi İşleme,5.4,5.5,5.6</td><td>Yüz kaybında güvenli davranış,çoklu iş parçacığı,FPS/CPU sınırları ve ham görüntünün saklanmaması bu bölümlerde güvence altına alınmıştır.</td></tr><tr><td>SYS-REQ-02/03/04/05/06,DB-REQ-11/12/13/14/15</td><td>3.5 Veritabanı Tasarım Kararları,5.9 Mobil Senkronizasyon,5.10 Veritabanı Tasarımı,5.11 Mobil Kullanıcı Giriş</td><td>Çevrimdışı tolerans, merkezi erişim,JSON tabanlı NoSQL yapı,veri bütünlüğü ve gerçek zamanlı senkronizasyon bu tasarım bileşenleriyle karşılanır.</td></tr><tr><td>SYS-REQ-13</td><td>5.3 Program ve Sınav Yönetimi,5.12 Kullanıcı Arayüzü Tasarımı</td><td>OCR sonrası manuel onay/düzenleme arayüzü bu gereksinimi karşılanır.</td></tr></table>

## 6.2 Modüllerden Gereksinimlere Geri İzlenebilirlik

Bu alt bölümde geri izlenebilirlik yaklaşımı benimsenmiş olup, her bir tasarım modülünün hangi gereksinim gruplarını karşıladığı açıklanmaktadır. Bu yaklaşım, belirli bir modül incelendiğinde onun sistem içindeki işlevsel kapsamının ve gereksinim katkısının açık biçimde anlaşılmasını sağlar. Özellikle bakım, güncelleme ve test süreçlerinde modül bazlı gereksinim eşleştirmesi önemli bir referans noktası oluşturmaktadır.

Bu çerçevede 5.1 Kullanıcı Giriş ve Profil Modülü, kullanıcı doğrulama, hatalı giriş yönetimi ve kullanıcı bilgilerinin güncellenmesiyle ilişkili gereksinimleri karşılamaktadır. 5.2 Ders Yönetimi Modülü, ders tanımlama, ders verilerinin güncellenmesi ve ders bazlı çalışma parametrelerinin tutulması ile ilgili gereksinimlerden sorumludur. 5.3 Program ve Sınav Yönetimi Modülü, hem manuel veri girişi hem de OCR ile veri alma süreçlerini kapsayarak akademik takvimin sisteme aktarılmasıyla ilgili gereksinimleri karşılamaktadır. 5.4 Odak Oturumu Yönetimi Modülü, odak oturumunun yaşam döngüsünü yönetirken; 5.5 Kafa Takibi ve Odak Skoru Modülü, bu oturum sırasında göruntü işleme ve odak analitiğini gerçekleştirmektedir.

Buna ek olarak 5.6 Whitelist Kontrol Modülü, işletim sistemi düzeyinde uygulama denetimi yaparak izin verilmeyen uygulamaları tespit etmekte, ihlal sürelerini hesaplamakta ve kullanıcıyı görsel/işitsel olarak uyarmaktadır. 5.7 Adaptif Zorluk Guncelleme Modülü, odak ve ihlal verilerini kullanarak ders zorluk katsayılarını güncellemektedir. 5.8 İstatistik ve Raporlama Modülü, sistemin diğer modüllerinden gelen çıktıları özetleyerek anlamı kullanıcı geri bildirimine dönüştürmektedir. 5.9 Mobil Senkronizasyon Modülü ile 5.11 Mobil Kullanıcı Giriş Modülü, masaüstü ve mobil istemciler arasında veri sürekliliği ve kimlik doğrulama işlevlerini yerine getirmektedir. Son olarak 5.10 Veritabanı Tasarımı modülü, sistemdeki tüm veri erişim işlemleri için merkezi altyapıyı sunmakta; 5.12 Kullanıcı Arayüzü Tasarımı ise gereksinimlerin kullanıcı ile etkileşime dönüştüruldüğü sunum katmanını oluşturmaktadır.

Dolayısıyla geri izlenebilirlik perspektifinden bakıldığında, FocuSync mimarisinde her modülün belirli bir gereksinim kümesine hizmet ettiği; bazı yatay modüllerin ise birden fazla gereksinim grubunu desteklediği anlaşılmaktadır. Bu yapı, hem modülerliği hem de gereksinim odaklı tasarım buttünlüğünü güçlendirmektedir.

<table border="1"><tr><td>Tasarım Bileşeni</td><td>Karşıladığı Gereksinimler</td></tr><tr><td>5.1 Kullanıcı Giriş ve Profil Modülü</td><td>AUTH-REQ-01/02, AUTH-ERR-01/02, DB-REQ-01/02/03, DB-ERR-01</td></tr></table>

<table border="1"><tr><td>5.2 Ders Yönetimi Modülü</td><td>COURSE-REQ-01/02/03/04, DB-REQ-04/05, ADG-REQ-01/02/03</td></tr><tr><td>5.3 Program ve Sınav Yönetimi Modülü</td><td>REQ-UI-01, OCR-REQ-01/02/03, OCR-ERR-01/02/03, DB-REQ-06, DB-ERR-02, SYS-REQ-13</td></tr><tr><td>5.4 Odak Oturumu Yönetimi Modülü</td><td>REQ-UI-02, REQ-HW-02, FSS-REQ-01...10, FSS-ERR-01/02/03, FSS-PERF-01/02, HTS ile entegrasyon gereksinimleri</td></tr><tr><td>5.5 Kafa Takibi ve Odak Skoru Modülü</td><td>REQ-HW-01/02, HTS-REQ-01...10, HTS-ERR-01/02/03, HTS-PERF-01/02/03, SYS-REQ-01, SYS-REQ-11, SYS-REQ-14</td></tr><tr><td>5.6 Whitelist Kontrol Modülü</td><td>REQ-SW-01, WL-REQ-01...14, WL-ERR-01...06, WL-PERF-01...04, DB-REQ-07/08/09</td></tr><tr><td>5.7 Adaptif Zorluk Güncelleme Modülü</td><td>COURSE-REQ-03/04, ADG-REQ-01/02/03, ADG-ERR-01, DB-REQ-10</td></tr><tr><td>5.8 İstatistik ve Raporlama Modülü</td><td>IVR-REQ-01/02/03/04, IVR-ERR-05, DB-REQ-09</td></tr><tr><td>5.9 Mobil Senkronizasyon Modülü</td><td>REQ-UI-03, REQ-SW-02, REQ-COMM-01, MS-REQ-01/02, MS-PERF-01, MS-ERR-01, SYS-REQ-04</td></tr><tr><td>5.10 Veritabanı Tasarımı</td><td>DB-REQ-02, DB-REQ-05/06/07/08/09/10/11/12/13/14/15, SYS-REQ-05, SYS-REQ-06</td></tr><tr><td>5.11 Mobil Kullanıcı Giriş Modülü</td><td>REQ-UI-03, AUTH-REQ-01/02, AUTH-ERR-01/02, DB-REQ-01/02/03, DB-ERR-01, MS-REQ-01</td></tr></table>

<table border="1"><tr><td>5.12 Kullanıcı Arayüzü Tasarımı</td><td>REQ-UI-01/02/03, SYS-REQ-13</td></tr></table>

## 6.3 Gereksinim-Modül Eşleştirme Tablosu

Aşağida, SRS gereksinim gruplar ile SDD tasarım modülleri arasındaki ilişkiyi özetleyen gereksinim-modül eşleştirme tablosu sunulmaktadır. Tabloda “X” işareti, ilgili modülün söz konusu gereksinim grubunu doğrudan karşıladığını göstermektedir. Tablo, hem ileri izlenebilirlik hem de geri izlenebilirlik analizlerinin özet görünümünü sunmak amacıyla hazirlanmıştir.

<table border="1"><tr><td>Gereksinim Grubu</td><td>5.1</td><td>5.2</td><td>5.3</td><td>5.4</td><td>5.5</td><td>5.6</td><td>5.7</td><td>5.8</td><td>5.9</td><td>5.10</td><td>5.11</td><td>5.12</td></tr><tr><td>REQ-UI</td><td></td><td></td><td>X</td><td>X</td><td>X</td><td>X</td><td></td><td></td><td>X</td><td></td><td>X</td><td>X</td></tr><tr><td>REQ-HW</td><td></td><td></td><td></td><td>X</td><td>X</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>REQ-SW</td><td></td><td></td><td></td><td></td><td></td><td>X</td><td></td><td></td><td>X</td><td>X</td><td></td><td></td></tr><tr><td>REQ-COMM</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>X</td><td>X</td><td>X</td><td></td></tr><tr><td>AUTH-REQ/AUTH-ERR</td><td>X</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>X</td><td>X</td><td></td></tr><tr><td>COURSE-REQ</td><td></td><td>X</td><td></td><td></td><td></td><td></td><td>X</td><td></td><td></td><td>X</td><td></td><td></td></tr><tr><td>OCR-REQ/OCR-ERR</td><td></td><td></td><td>X</td><td></td><td></td><td></td><td></td><td></td><td></td><td>X</td><td></td><td>X</td></tr><tr><td>FSS-REQ</td><td></td><td></td><td></td><td>X</td><td>X</td><td></td><td></td><td></td><td></td><td>X</td><td></td><td></td></tr></table>

<table border="1"><tr><td>HTS-REQ</td><td></td><td></td><td></td><td>X</td><td>X</td><td></td><td></td><td></td><td></td><td>X</td><td></td><td></td></tr><tr><td>WL-REQ/WL-ERR</td><td></td><td></td><td></td><td></td><td></td><td>X</td><td></td><td>X</td><td></td><td>X</td><td></td><td></td></tr><tr><td>ADG-REQ/ADG-ERR</td><td></td><td>X</td><td></td><td></td><td>X</td><td>X</td><td>X</td><td></td><td></td><td>X</td><td></td><td></td></tr><tr><td>IVR-REQ</td><td></td><td></td><td></td><td></td><td></td><td>X</td><td></td><td>X</td><td></td><td>X</td><td></td><td></td></tr><tr><td>MS-REQ/MS-ERR</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>X</td><td>X</td><td>X</td><td></td></tr><tr><td>DB-REQ</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td></td></tr></table>

<div align="center">

Tablo 6.1'de görüldüğü üzere, özellikle 5.10 Veritabanı Tasarımı modülü sistemin hemen her gereksinim grubu ile ilişkili yatay bir bileşen niteliğindedir. Buna karşılık 5.4, 5.5 ve 5.6 numaralı modüller sistemin gerçek zamanlı çalışma eksenini; 5.7 ve 5.8 numaralı modüller ise analiz ve uyarlama eksenini oluşturmaktadır. 5.9 ve 5.11 numaralı modüller mobil istemci sürekliliğini desteklerken, 5.12 kullanıcı etkileşiminin sunum katmanındaki karşılığın oluşturmaktadır. Böylece gereksinimlerden tasarima uzanan buttünsel bağ açık biçimde kurulmuş olmaktadır.

</div>

## 7. Notlar

## 7.1 Kisaltmalar

- AI (Artificial Intelligence): Yapay Zeka.

- API (Application Programming Interface): Uygulama Programlama Arayüzü.

- CPU (Central Processing Unit): Merkezi İşlem Birimi.

- DAL (Data Access Layer): Veri Erişim Katmanı.

- FPS (Frames Per Second): Saniyedeki Kare Sayısı.

- GUI (Graphical User Interface): Grafiksel Kullanıcı Arayüzü.

- HMAC (Hash-based Message Authentication Code): Anahtarlamalı Özet Mesaj Doğrulama Kodu.

- JSON (JavaScript Object Notation): Hafif veri değişim formatı.

- OCR (Optical Character Recognition): Optik Karakter Tanima.

- PBKDF2 (Password-Based Key Derivation Function 2): Parola Tabanlı Anahtar Türetme Fonksiyonu 2.

- RAM (Random Access Memory): Rastgele Erişimli Bellek.

- SDD (Software Design Document): Yazılım Tasarım Dokümanı.

- SDK (Software Development Kit): Yazılım Geliştirme Kiti.

- SHA (Secure Hash Algorithm): Güvenli Özet Algoritması.

- SPA (Single Page Application): Tek Sayfa Uygulaması.

- SPMP (Software Project Management Plan): Yazılım Proje Yönetim Planı.

- SRS (Software Requirements Specification): Yazılım Gereksinim Belirtimi.

- UI (User Interface): Kullanıcı Arayüzü.

- UUID (Universally Unique Identifier): Evrensel Benzersiz Tanımlayıcı.

- UX (User Experience): Kullanıcı Deneyimi.

## 7.2 Terimler Sözlüğü

- Debounce (Yumuşatma): Anlık kafa sarsıntılarını ve yanlış pozitifleri önlemek için uygulanan, odak durumunun değişmesi için gereken asgari tampon süresi (kare sayısı) mekanizması.

- Gateway Pattern (Geçit Tasarım Deseni): Modüllerin doğrudan veritabanı ile iletişim kurmasını engelleyen ve tüm CRUD operasyonların izole edilmiş tek bir sınıf üzerinden yürütuldüğü merkezi mimari yapı.

- Kalın İstemci (Thick Client): Ağır işlem yükü gerektiren bilgisayarlı görü (OCR, kafa takibi) ve işletim sistemi düzeyindeki görevleri sunucu yerine yerel makinede (kullanıcı bilgisayarında) çözen mimari yaklaşım.

- Landmark: Görüntü işleme sırasında kafa pozisyonu tahmini yapabilmek için yüz üzerinden (burun, çene, göz vb.) çıkarılan referans koordinat noktaları.

- Multithreading (Çoklu İş Parçacığı): Ana arayüzün kilitlenmesini ve donmasını önlemek için ağır görevlerin (kamera akışı, OCR taraması, aktif pencere izleme) asenkron arka plan işçilerine bölünmesi.

- Pitch / Yaw / Roll: Kafa hareketlerinin üç boyutlu düzlemdeki Euler açılaridır; sırasıyla yukarı/aşağı, sağ/sol ve omuzlara eğilme yönelimlerini ifade eder.

- Hash: Herhangi bir boyuttaki veriyi (örneğin bir parolayı) matematiksel algoritmalar kullanarak sabit uzunlukta, karmaşık ve geri döndürulemez bir karakter dizisine dönüştürme işlemi.

- Salted Hash: Şifre güvenliğini sağlamak için her kullanıcıya özel rastgele üretilen bir tuz (salt) değerinin kullanıcının şifresi ile birleştirilerek şifrenmesi işlemi.

- Soft Delete (Yumuşak Silme): Verilerin fiziksel olarak tamamen silinmesi (Hard Delete) yerine, referans buttünlüğünün ve geçmişe dönük analizlerin korunması amacıyla durum bayrakları (is_active = false) ile arayüzden gizlenmesi stratejisi.

- Upsert: Veritabanında belirtilen koşullara uygun bir kayıt yoksa yeni kayıt oluşurma, eşleşen bir kayıt varsa mevcut kaydı veri kaybı yaşanmadan güncelleme (Update + Insert) mimarisi.

- Whitelist (Beyaz Liste): Kullanıcının odak oturumu sırasında çalışmasına izin verdiği ve ceza (ihlal süresi) almadığı istisna masaüstü uygulamaları listesi.

## 7.3 Tasarım Varsayımlari

- Donanım Gereksinimi: Kullanıcınin kafa takibi (Head Tracker) modülünü kullanabilmesi için cihazında çalışır durumda ve gerekli izinlere sahip bir web kamerası donanımı bulunduğu varsayılmıştır.

- İşletim Sistemi Bağımlılığı: Beyaz Liste (Whitelist) modülundeki aktif pencere tespitinin ve süreç izleme mekanizmasının (win32gui, win32process, Windows Registry) Windows işletim sistemi kurulu cihazlar üzerinde çalışacağı varsayılmıştır.

- Ağ Durumu ve Çevrimdışı (Offline) Yaklaşım: Internet bağlantısı kesildiğinde veritabanı işlemlerin hata fırlatacağı varsayilmış ve işlemlerin durdurulmasını sağlayan savunmacı bir tasarım yapilmıştır. Mimari düzeyde verileri yerelde depolayacak bir önbellek (offline cache) altyapısı varsayilmamıştır.

- Yapay Zeka Servis Kararlılığı: OCR belge ayrıştırmasi ve JSON şeması oluşturma adımlarında Google Gemini AI modelinin (gemini-1.5-flash-8b) genel erişilebilir durumda olacağı ve bekleme sürelerinin (latency) "Uygulama Yanıt Vermiyor" sorununa yol açmadan arka planda çözüleceği varsayılmıştır.

## 7.4 Gelecek Sürümler İçin Genişletme Notları

- Gelişmiş Çevrimdışı Destek (Offline-First Mimarisi): Mevcut sistemde ağ kesintileri uygulamanın sadece veri okuma ve yazma eylemlerini durdurmasına yol açmaktadır. Gelecek sürümlerde istemcilere SQLite veya Room/Hive gibi bir yerel veritabanı eklenerek, tam çevrimdışı çalışma desteği ve bağlantı geldiğinde asenkron veri senkronizasyonu mekanizması entegre edilebilir.

- Çapraz Platform (Cross-Platform) Masaüstü İzleme Desteği: Şu anki mimarideki aktif uygulama denetimi (Whitelist), Windows API kütüphanelerine bağlidır. İlerleyen aşamalarda macOS ve Linux için pencere durumu algılama bağımlılıklar dahil edilerek sistemin platform bağımsızlığı artırılabilir.

- Çoklu Rol Yönetimi: Veritabanındaki Users koleksiyonunda yer alan role alanı varsayılan olarak "User" atanmıştır. Bu yapı, uygulamanın öğretmen, akademik danışman veya ebeveyn gibi çoklu aktörleri barındirabilecek bir düzeye (Multi-role Access) çıkarılması için önceden tasarlanmıştır ve genişletilmeye açıktır.

- Bulut Tabanlı Whitelist Senkronizasyonu: Beyaz Liste (Whitelist) yönetim ekranında oluşturulan listelerin şu anki iş mantığı, çalışma anında bellek içerisinde tutulmaktadır. İlerleyen geliştirmelerde, bu verinin Users koleksiyonunda halihazırda ayrılmış olan allowed_apps alanı kullanılarak cihazlar arası kalıcı olarak senkronize edilmesi hedeflenmelidir.

## 8. Ekler

<div align="center">

Ek-A: Sistem Mimarisi Diyagramları

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495718.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=kX3Rijycfkwhkbf56UTfSULOzoE%3D&Expires=1779181295' alt='OCR图片'/></div>

## Ek-C: Veritabanı Şeması

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F2026051217002402246458e11b4179%2Fcrop_1_1778576495727.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=Wkl%2BHGRGvR1FaCimyGUOXOmHFVE%3D&Expires=1779181295' alt='OCR图片'/></div>