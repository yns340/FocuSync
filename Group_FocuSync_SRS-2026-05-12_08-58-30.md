<div align="center">

# GAZİ ÜNİVERSİTESİ

Mühendislik Fakültesi – Bilgisayar Mühendisliği Bölümü

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F20260512165752ba865aa1a5364a94%2Fcrop_1_1778576306325.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=s%2B%2Bi%2FC%2FWq1CDK%2FyRRVHzD6fbv3U%3D&Expires=1779181106' alt='OCR图片'/></div>

<div align="center">

# BM314 Yazılım Mühendisliği

</div>

<div align="center">

# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

</div>

FocuSync

Hazirlayanlar:

- Mehmet Koksal - 23118080060

- Yunus Recepoğlu - 23118080019

- Zeynep Yamaç - 23118080080

- Kerem Kapısız - 22118080009

- Mehmet Akif Türk - 23118080702

## Revizyon Sayfası

<table border="1"><tr><td>Sürüm</td><td>Tarih</td><td>Yazar(lar)</td><td>Açıklama</td></tr><tr><td>1.0</td><td>22 Mart 2026</td><td>Mehmet Köksal, Yunus Recepoğlu, Zeynep Yamaç, Kerem Kapısız, Mehmet Akif Türk</td><td>SRS (Yazılım Gereksinim Belirtimi) ilk taslağı oluşturuldu</td></tr></table>

İçindekiler

1. Giriş ... 5

1.1 Amaç ... 5

1.2 Kapsam ... 5

1.3 Ürün Genel Bakışı ... 5

1.4 Tanımlar ve Kısaltmalar ... 5

1.5 Referanslar ... 5

2. Genel Tanım ... 6

2.1 Ürün Perspektifi ... 6

2.2 Ürün Fonksiyonları ... 6

2.3 Kullanıcı Sınifları ... 6

2.4 Çalışma Ortamı ... 6

2.4.1 Masaüstü Uygulaması ... 6

2.5 Kısıtlar ... 7

2.5.1 Teknik Kısıtlar ... 7

2.5.2 Tasarım ve Uygulama Kısıtları ... 7

2.5.3 Yasal ve Gizlilik Kısıtları ... 7

2.6 Varsayımlar ve Bağımlılıklar ... 7

2.6.1 Varsayımlar ... 7

2.6.2 Bağımlılıklar ... 8

3. Özel Gereksinimler ... 9

3.1 Harici Arayüz Gereksinimleri ... 9

3.1.1 Kullanıcı Arayüzleri ... 9

3.1.2 Donanım Arayüzleri ... 9

3.1.3 Yazılım Arayüzleri ... 9

3.1.4 İletişim Arayüzleri ... 10

3.2 Yazılım Ürün Özellikleri ... 10

3.2.1 Kullanıcı Giriş Sistemi ... 10

3.2.2 Ders Yönetimi ... 11

3.2.3 Program ve Sınav Yönetimi ... 12

3.2.4 Odak Oturumu Yönetimi ... 13

3.2.5 Kafa Takibi ve Odak Skoru ... 15

3.2.6 Beyaz Liste Kontrolü ... 17

3.2.7 Adaptif Zorluk Güncelleme ... 20

3.2.8 İstatistik ve Raporlama ... 21

3.2.9 Mobil Senkronizasyon ... 21

3.3 Yazılım Sistem Nitelikleri ...22

3.3.1 Güvenilirlik ...22

3.3.2 Kullanılabilirlik ...22

3.3.3 Güvenlik ...23

3.3.4 Bakım Yapılabilirlik ...23

3.3.5 Taşınabilirlik ...23

3.3.6 Performans ...23

3.3.7 Kullanım Kolaylıği ...24

3.3.8 Gizlilik ...24

3.4 Veritabanı Gereksinimleri ...24

4. Ek Materyaller ...25

## 1. Giriş

## 1.1 Amaç

Bu dokümanın amacı, FocuSync projesinin tüm fonksiyonel ve fonksiyonel olmayan gereksinimlerini detaylandırmaktadır. FocuSync, kullanıcıların bilgisayar başında ders çalışrken verimliliklerini ölçmeyi ve artırmayı hedefleyen kapsamlı bir odaklanma ve planlama sistemidir.

## 1.2 Kapsam

FocuSync sistemi, kamera aracılığıyla kafa yönünü izleyerek dikkati ölçen bir masaüstü uygulaması ve bu verilerin senkronize edildiği bir mobil uygulamayı kapsar. Sistem, arka planda çalışan uygulamalara erişimi denetleyen "Whitelist" modülü ve elde edilen odaklanma verilerine göre ders çalışma stratejilerini dinamik olarak optimize eden bir altyapı sunar.

## 1.3 Ürün Genel Bakışı

Ürün, kullanıcının ders programını manuel olarak veya PDF formatında sisteme girmesine olanak tanıyan bir altyapı ile çalışmaya başlar. Masaüstü uygulaması, bir web kamerası üzerinden yüz ve kafa hareketlerini takip ederek "Odaklanma Skoru" hesaplar ve kullanıcının belirlediği uygulamalar haricindeki yazılmlara erişimi "Whitelist" sistemiyle engelleyerek odaklanmayı maksimize eder. Sistem, kullanıcının dikkat dağınklığı düzeyine göre ders zorluklarını ve mola sürelerini içeren odaklanma stratejilerini arka planda dinamik olarak günceller. Ayrıca, sunulan mobil uygulama arayüzü sayesinde kullanıcılar ders programlarına, sınav tarihlerine ve verimlilik istatistiklerine diledikleri zaman uzaktan erişebilirler.

## 1.4 Tanımlar ve Kısaltmalar

- Whitelist: Odaklanma oturumu aktifken çalışmasına izin verilen, işletim sistemi seviyesindeki güvenilir prosesleri içeren yapı.

- Multithreading: Kamera takibi ve uygulama denetimi gibi ağır işlemlerin kullanıcı arayüzünü dondurmadan arka planda eş zamanlı çalışmasını sağlayan çoklu iş parçacıgı mimarisi.

- FPS: Saniyedeki kare sayıs1 (Frames Per Second).

- Kafa Takip Modülü: Kamera göruntüsünden kafa yönünün (Pitch/Yaw/Roll) hesaplanması

- Pitch / Yaw / Roll: öne-arkaya eğim / sağa-sola döndürme / yana yatma

- OpenCV: Açık kaynaklı bilgisayar görüşü kütüphanesi

- OBS: Ögrenci Bilgi Sistemi

## 1.5 Referanslar

- IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications

- Firebase Firestore Dokümantasyonu - https://firebase.google.com/docs/firestore

## 2. Genel Tanim

## 2.1 Ürün Perspektifi

FocuSync, bağımsız bir masaüstü uygulaması ve bu uygulamayı veri bazında destekleyen tamamlayıcı bir mobil uygulamadan oluşan bulut veri tabanı mimarisine sahip bir sistemdir. Masaüstü uygulaması doğrudan işletim sistemi proses yönetim araçları ve standart donanımlar (web kamerası) ile birlikte çalışır. Masaüstü ve mobil platformlar arasındaki iletişim ve istatistik senkronizasyonu Firebase altyapısı kullanılarak gerçek zamanlı olarak sağlanır.

## 2.2 Ürün Fonksiyonları

- Kullanıcınin sisteme ders programı ve sınav tarihlerini manuel olarak veya PDF işleme (OCR) mekanizması aracılığıyla yüklemesinin sağlanması.

- Kamera ve görüntü işleme algoritmaları (OpenCV) aracılığıyla kullanıcınin kafa yönü takibinin ve dikkat analizinin yapılması.

- Kullanıcınin dikkatinin dağıldığı durumların tespiti için Euler açılarındaki sapmaların ölçülmesi ve süre aşıldığında sesli veya görsel uyariların tetiklenmesi.

- İzin verilmeyen uygulamalara erişimi kısıtlayan Whitelist denetiminin yapılması ve olası ihlallerde raporlanması.

- Kamera ve denetim modüllerinden alınan istatistiklerle "Odaklanma Skoru" oluşturulması ve matematiksel modeller ile ders çalışma zorluklarının/planlarının otomatik olarak güncellenmesi (Adaptif Zorluk).

- Elde edilen verimlilik raporların bulut ortamında güvenle saklanması ve masaüstü ile mobil uygulamalar arasında kesintisiz eşzamanlı senkronizasyonu.

## 2.3 Kullanıcı Sınıfları

Öğrenci / Son Kullanıcı: Bilgisayar başında ders çalışan, odaklanma sorunuyla mücadele eden lise veya üniversite öğrencisi. Kamera takibini aktifleştirir, Whitelist'i yapılandırir, ders programını girer ve istatistiklerini takip eder. Temel teknik yeterlilik beklenir (uygulama kurulumu, kamera erişim izni verme gibi). Mobil uygulamayı da aktif olarak kullanır. Sistemde şu an için farklı bir "Yönetici (Admin)" rolü öngörülmemektedir

## 2.4 Çalısma Ortami

## 2.4.1 Masaüstü Uygulaması

- İşletim Sistemi: Windows 10 / Windows 11 (64-bit). macOS / Linux desteği bu sürümün kapsamı dışındanadır.

- Donanim: Standart dahili veya harici USB web kamerası (minimum 720p çözünürlük önerilir), minimum 4 GB RAM, çift çekirdekli işlemci (multithreading mimarisi nedeniyle).

- Aydınlatma: Kafa takibi algoritmasının doğruluğu yeterli ortam ışıklandırmasına bağlidır (açık ışık kaynağı önünde konumlanmaktan kaçınılmalıdır).

- Geliştirme Ortamı: Python (OpenCV, MediaPipe/Dlib, psutil), Git/GitHub versiyon kontrolü.

## 2.5 Kısitlar

## 2.5.1 Teknik Kısıtlar

- Kafa takibi algoritmasının doğruluğu, ortam ışıklandırması ve kullanıcıının kameraya olan açısının stabil olmasıyla doğrudan bağmlıdır. Yetersiz ışık koşullarında performans düşüşü beklenmektedir.

- Whitelist denetimi yalnızca Windows işletim sistemi API'leriyle uyumlu biçimde geliştirilmektedir, diğer platformlar mevcut sürümde desteklenmemektedir.

- Kamera takibi, Whitelist denetimi ve UI eşzamanlı çalıştırılacağı için multithreading mimarisinin uygulanması zorunludur,aksi durumda kullanıcı arayüzunde donmalar yaşanabilir.

- OCR tabanlı PDF okuma işlevinin doğruluğu, yüklenen PDF dosyasının yapısal düzenine ve metin kalitesine bağlidır.

## 2.5.2 Tasarım ve Uygulama Kısıtları

- Kullanıcı göz hareketleri veya diğer biyometrik veriler izlenmeyecektir, yalnızca kafa yönü kullanılacaktır.

- Adaptif algoritma çıktılar, modelin uç değerlere kaymasını önlemek amacıyla alt ve üst çalışma süresi sınırlarıyla kısıtlanacaktır.

## 2.5.3 Yasal ve Gizlilik Kısıtları

- Kamera görüntüleri yerel olarak işlenmekte ve ham görüntü verisi buluta aktarılmamaktadır. Yalnızca türetilmiş metrikler (açı değerleri, odaklanma skoru) saklanmaktadır.

- Kullanıcı kişisel verileri (ders programı, istatistikler) Firebase üzerinde kullanıcıya özgü kimlik doğrulama kapsamında korunacaktır.

## 2.6 Varsayımlar ve Bağımlıliklar

## 2.6.1 Varsayimlar

- Kullanıcınin bilgisayarında en az bir adet işlevsel web kamerası bulunmaktadır ve uygulama kamera erişim iznine sahiptir.

- Kullanıcı, ders programını sisteme ya manuel olarak girecek ya da uyumlu PDF formatında sağlayacaktır.

- Masaüstü uygulaması sürekli internet bağlantısı gerektirmeden temel işlevlerini yerine getirecek, senkronizasyon için bağlantı sağlandığında Firebase ile eşleşme yapılacaktır.

- Kullanıcı, Whitelist'te yer almayan uygulamaların odaklanma oturumu sırasında engelleneceğini önceden bilmekte ve bunu kabul etmektedir.

- Kamera, kullanıcı masada otururken yüzü açıkça görülebilecek konumda ve sabit açida tutulacaktır.

## 2.6.2 Bağımlıliklar

- Firebase bağmlılığı: Bulut senkronizasyon ve kimlik doğrulama özellikleri tamamen Firebase hizmetinin sürekliliğine bağlidır. Servis kesintisi durumunda yalnızca yerel veri erişimi mümkün olacaktır.

- OpenCV bağımlılığı: Kafa takibi modülü bu açık kaynaklı kütüphanelere dayanmaktadır, kütüphane güncellemeleri uyumluluk testini zorunlu kılar.

- Görev bağımlılıklar: Dinamik Ağirlık Guncelleme Modülü, kamera ve Whitelist modüllerinden gelen verilerin kalitesine doğrudan bağmlıdır. Bu iki modülün tamamlanması Dinamik Ağirlık Guncelleme için ön koşuldur.

- Mobil uygulama bağmlılığı: Mobil uygulama işlevselliği, masaüstü uygulamasının Firebase'e yazdığı veri şemasına bağlidır. Şema değişiklikleri her iki platformu da etkileyecektir.

- Donanım bağlmlılığı: Sistem performansı, kullanıcı bilgisayarının işlemci kapasitesine ve kamera kalitesine bağlidır. Düşük donanımlı sistemlerde FPS düşüşü yaşanabilir.

## 3. Özel Gereksinimler

## 3.1 Harici Arayüz Gereksinimleri

## 3.1.1 Kullanıcı Arayüzleri

## REQ-UI-01:

Masaüstü uygulaması, kullanıcının ders programını ve sınav tarihlerini manuel olarak gireceği veya PDF formatında sisteme yükleyebileceği bir arayüz sağlayacaktır.

## REQ-UI-02:

Sistem, "Beyaz Liste" (Whitelist) ihlali yapıldığında veya kafa takibi sonucunda yüz tespit edilemediğinde/dikkat dağıldığında ekranda görsel pop-up uyarları gösterecektir.

## REQ-UI-03:

Mobil uygulama, masaüstü uygulamasıyla senkronize çalışarak giriş/kayıt (Login/Register) ekranlar sunacak. Güncel ders programlarını, sınav tarihlerini ve odaklanma istatistiklerini görüntüleme imkanı sağlayacaktır.

## 3.1.2 Donanım Arayüzleri

## REQ-HW-01:

Sistem, kullanıcıın dikkat dağılımını ölçmek ve kafa yönünü izlemek için standart web kamerası donanımına erişim sağlayacaktır.

## REQ-HW-02:

Sistem, odaklanma süresi boyunca belirlenen eşik değerlerden sapma olduğunda kullanıcıyı uyarmak üzere cihazın ses donanımını kullanarak sesli bildirim verecektir.

## 3.1.3 Yazılım Arayüzleri

## REQ-SW-01:

Sistem, işletim sistemi seviyesinde çalışan prosesleri dinlemek ve yalnızca "Beyaz Liste" içindeki uygulamalara izin vermek için işletim sistemineözgü proses/pencere yönetimi API'lerini kullanacaktır.

## REQ-SW-02:

Kullanıcı verilerinin (akademik planlar, istatistikler ve ihlal logları) NoSQL yapısında saklanması ve masaüstü-mobil arası eşzamanlı senkronizasyonu için Firebase (Firestore/Realtime Database) arayüzleri kullanılacaktır.

## 3.1.4 İletişim Arayüzleri

## REQ-COMM-01:

Masaüstü ve mobil istemcilerin veritabanı (Firebase) ile haberlesmesi uygulanın ana iş parçacığını dondurmadan (asenkron olarak) ağ bağlantısı üzerinden kesintisiz bir şekilde gerçekleştircektir.

## 3.2 Yazılım Ürün Özellikleri

## 3.2.1 Kullanıcı Giriş Sistemi

## 3.2.1.1 Modül Tanımı

FocuSync sistemi, kullanıcıların masaüstü ve mobil platformlar üzerinden kişisel çalışma verilerine erişebilmesi için merkezi bir kimlik doğrulama mekanizması sunar. Kullanıcılar, eposta ve şifre kombinasyonu ile sisteme kayıt olduktan sonra bu veriler, NoSQL mimarisine sahip Firebase Firestore bulut veritabanında güvenli bir şekilde depolanır. Sistem, her iki platformdan gelen giriş taleplerini aynı merkezi veritabanı üzerinden doğrular ve başarılı oturum açma işlemi sonrasında kullanıcı profili ile çalışma istatistiklerini cihazlar arasında eşzamanlı olarak senkronize eder.

## 3.2.1.2 Fonksiyonel Gereksinimler

## AUTH-REQ-01:

Sistem, yeni kayıt oluşturmak isteyen kullanıcıdan yalnızca e-posta adresi ve şifre bilgilerini alarak kayıt işlemini tamamlamalıdır.

## DB-REQ-01:

Başarıyla oluşturulan kullanıcı kimlik bilgileri, NoSQL bulut veritabanında ilgili kullanıcı koleksiyonuna yeni bir kayıt olarak eklenmelidir.

## AUTH-REQ-02:

Sistem, giriş yapmak isteyen kullanıcının sunduğu e-posta ve şifre kombinasyonunun doğruluğunu, doğrudan veritabanındaki kayıtları sorgulayarak teyit etmelidir.

## DB-REQ-02:

Veritabanına yönelik tüm okuma (giriş yapma) ve yazma (kayıt olma) talepleri, doğrudan bağlantı kurmak yerine, yetkilendirilmiş merkezi bir veritabanı yöneticisi modülü üzerinden yürütülmelidir.

## DB-REQ-03:

Başarılı giriş sonrasında kullanıcı oturumu ve verileri, masaüstü ve mobil platformlar arasında eşzamanlı olarak senkronize edilmelidir.

## 3.2.1.3 Hata Yönetimi Gereksinimleri

## AUTH-ERR-01:

Sistem, girilen e-posta adresi veritabanında bulunamadığında veya e-postaya ait şifre eşleşmediinde kullanıcıyla "Hatalı Giriş Bilgileri" uyarısı döndürmelidir.

## AUTH-ERR-02:

E-posta formatına uygun olmayan (örn: @ işareti eksik) giriş denemelerinde sistem, veritabanına sorgu göndermeden işlemi arayüz seviyesinde engellemeli ve kullanıcıyı uyarmalıdır.

## DB-ERR-01:

Veritabanı yapılandırmasının eksik olması veya sunucu bağlantısının kurulamaması durumunda sistem, giriş/kayıt işlemini durdurmalı ve kullanıcıya "Bağlantı Hatası" mesajı göstermelidir.

## 3.2.2 Ders Yönetimi

## 3.2.2.1 Modül Tanımı

Sistem; kullanıcıya ait ders adlarını, bu derslere başlangıca atanan zorluk derecelerini ve günlük çalışma planlarını NoSQL tabanlı bulut veritabanı mimarisinde kayıt altında tutar. Ders yönetimi modülü, kafa takip modülünden gelen gerçek zamanlı odaklanma verilerini analiz ederek başlangıca statik olan ders zorluklarını "dinamik ağırlık güncelleme" algoritması aracılığıyla otomatik olarak revize eder. Odaklanma skorunun düşük kaldığı dersler için sistem, veritabanındaki ilgili dersin zorluk katsayısını artırarak kullanıcıya daha kısa çalışma periyotları ve sık mola süreleri içeren optimize edilmiş yeni bir odaklanma stratejisi sunar. Uygulama kapatılsa dahi tüm bu güncel ders verileri ve verimlilik istatistikleri, veri kaybını önlemek amacıyla bulut veritabanında güvenle saklanır ve mobil platformla ezzamanlı olarak paylaşılır.

## 3.2.2.2 Fonksiyonel Gereksinimler

## COURSE-REQ-01:

Sistem, kullanıcının ders adlarını, bu derslere atadığı başlangıç zorluk derecelerini ve günlük çalışma planlarını girmesine olanak tanimalidır.

## DB-REQ-04:

Sistem, kullanıcı tarafından girilen ders ve çalışma planı verilerini NoSQL bulut veritabanında kalıcı olarak saklamaldır.

## COURSE-REQ-02:

Sistem, kafa takip modülünden oturum sonlarında elde edilen "odaklanma skorunu" alarak ilgili dersin veritabanı kaydına işlemelidir.

## COURSE-REQ-03:

Sistem, bir derse ait odaklanma skorunun düşük olması durumunda arka planda dinamik ağırlık güncelleme algoritmasını tetikleyerek, o dersin zorluk katsayısını veritabanında otomatik olarak artırmalıdır.

## COURSE-REQ-04:

Sistem, zorluk derecesi güncellenen dersler için çalışma sürelerini değiştirerek yeni ve optimize edilmiş bir çalışma planı oluşturmalıdır.

## DB-REQ-05:

Sistem, algoritma tarafından güncellenen tüm ders zorluklarını ve yeni çalışma stratejilerini bulut veritabanına kaydetmeli ve veri bütünlüğünü sağlamak için mobil platformla anlık olarak senkronize etmelidir.

## 3.2.3 Program ve Sınav Yönetimi

## 3.2.3.1 Modül Tanımı

Sistem, kullanıcının akademik takvimini manuel giriş zahmetinden kurtarmak amacıyla otomatik bir veri çekme (OCR) mekanizması barındırir. Kullanıcı tarafından PDF formatında sisteme yüklenen haftalık ders programları ve sınav takvimleri, görüntü işleme ve metin ayıklama teknikleri kullanılarak analiz edilir; ayıklanan ders isimleri, saatleri ve tarihleri otomatik olarak veritabanına işlenir. Bu sayede elde edilen veriler, sistemin çalışma planı oluşturma ve hatırlatıcı servisleri için temel veri kaynağını oluşturur

## 3.2.3.2 Fonksiyonel Gereksinimler

## OCR-REQ-01:

Sistem, kullanıcınin OBS’den temin ettiği haftalık ders programı ve sınav takvimini içeren dosyaları PDF formatlarında sisteme yüklemesine olanak tanimalidır.

## OCR-REQ-02:

Sistem, yüklenen dosya (PDF) üzerindeki metinleri ve tabloları görüntü işleme algoritmaları aracılığıyla tarayarak ders isimlerini, başlangıc/bitiş saatlerini ve sınav tarihlerini ayıklamalıdır.

## DB-REQ-06:

Sistem, OCR mekanizması tarafından başarıyla ayıklanan tüm ders ve sınav programı verilerini,

NoSQL bulut veritabanındaki ilgili koleksiyonlara kaydetmelidir.

## OCR-REQ-03:

Sistem, OCR modülünün hatalı çalışmasından kaynaklanabilecek eksik veya hatalı veri aktarımını önlemek adına, ayiklanan verileri veritabanına işlemeden önce manuel bir düzenleme/onay arayüzü seçeneği sunmalıdır.

## 3.2.3.3 Hata Yönetimi Gereksinimleri

## OCR-ERR-01:

Sistem, desteklenmeyen bir dosya formatı (örn. .docx, .xlsx, .txt) yüklendiğinde işlemi anında reddetmeli ve kullanıcıya "Geçersiz Dosya Formatı" uyarısı göstermelidir.

## OCR-ERR-02:

Sistem, yüklenen görselin veya dokümanın çözünürlük düşüklüğü, aşırı karmaşık tablo yapısı veya okunmayan fontlar nedeniyle veri ayıklama işlemini gerçekleştirmezse, kullanıcıya "Okunamayan Doküman" hatası döndürmeli ve manuel giriş ekranına yönlendirmelidir.

## OCR-ERR-03:

Sistem, yüklenen dosya içindeki tarih ve saat formatlarının sistemin beklediği standartların dışında (örn. "14:00" yerine "öğleden sonra iki") olması durumunda, veritabanı tutarsızlığın önlemek için o kaydı atlamalı veya kullanıcıdan düzeltme talep etmelidir.

## DB-ERR-02:

Sistem, ayıklanan verileri veritabanına kaydederken sunucu tarafında bir bağlantı kopması yaşanırsa, eksik veri girişini engellemek için tüm kaydetme işlemini iptal etmeli (rollback) ve kullanıcı bilgilendirmelidir.

## 3.2.4 Odak Oturumu Yönetimi

## 3.2.4.1 Modül Tanımı

Odak Oturumu Yönetimi modülü, kullanıcınin belirli bir süre boyunca dikkatini bir göreve vermesini sağlamak amacıyla oluşturulan odaklanma oturumlarını yönetecektir. Bu modül, kullanıcınin odak oturumunu başlatmasına, durdurmasına ve tamamlamasına olanak sağlayacaktır.

Sistem, odak oturumu süresince kullanıcının çalışma süresini takip edecek ve oturum sonunda analiz yapılabilmesi için gerekli verileri kaydedecektir. Bu modül, kafa takibi ve odak skoru modülü ile entegre şekilde çalışacaktır.

Odak oturumu yönetimi, kullanıcıın dikkat sürecini düzenli hale getirmeyi ve verimli çalışma alıskanlığı geliştirmesini destekleyecektir.

## 3.2.4.2 Fonksiyonel Gereksinimler

## FSS-REQ-01 (Oturum Başlatma):

Sistem, kullanıcının odak oturumu başlatma komutu vermesi ile birlikte yeni bir odak oturumu oluşturacaktır.

## FSS-REQ-02 (Oturum Süresi Belirleme):

Sistem, kullanıcınin odak oturumu için belirli bir süre seçmesine veya varsayılan süreyi kullanmasına izin verecektir.

## FSS-REQ-03 (Zamanlayıcı Başlatma):

Sistem, odak oturumu başladığında geri sayım zamanlayıcısinı başlatacaktır.

## FSS-REQ-04 (Oturum Duraklatma):

## FSS-REQ-05 (Oturum Devam Ettirme):

Sistem, kullanıcı talep ettiğinde aktif odak oturumunu geçici olarak duraklatacaktır.

Sistem, duraklatılmış bir odak oturumunun kullanıcı tarafından tekrar başlatılmasını sağlayacaktır.

## FSS-REQ-06 (Oturum Sonlandırma):

Sistem, kullanıcı tarafından sonlandırılan veya süresi dolan odak oturumunu tamamlanmış olarak işaretleyecektir.

## FSS-REQ-07 (Oturum Verisi Kaydetme):

Sistem, tamamlanan odak oturumuna ait süre bilgisi ve odak verilerini veritabanına kaydedecektir.

## FSS-REQ-08 (Oturum Durumu Gösterimi):

Sistem, kullanıcı arayüzunde aktif odak oturumunun kalan süresini ve durumunu gösterecektir.

## FSS-REQ-09 (Oturum Geçmişi Oluşturma):

Sistem, kullanıcının geçmiş odak oturumlarını listeleyebilecektir.

## FSS-REQ-10 (Modül Entegrasyonu):

Sistem, odak oturumu sırasında kafa takibi ve odak skoru modülü ile veri alışverisi gerçekleştircektir.

## 3.2.4.3 Hata Yönetimi Gereksinimleri

## FSS-ERR-01 (Oturum Başlatma Hatası):

Sistem, odak oturumu başlatılamadığında kullanıcıya hata mesajı gösterecektir.

## FSS-ERR-02 (Zamanlayıcı Hatası):

Sistem, zamanlayıcıda oluşabilecek bir hata durumunda oturum verilerini koruyacak ve sistemi güvenli şekilde durduracaktır.

## FSS-ERR-03 (Veri Kaydı Hatası):

Sistem, oturum verileri veritabanına kaydedilemediğinde kullanıcıyı bilgilendirecektir.

## 3.2.4.4 Performans Gereksinimleri

## FSS-PERF-01 (Gerçek Zamanlı Güncelleme):

Sistem, odak oturumu zamanlayıcısını kullanıcı arayüzunde gerçek zamanlı olarak (1 saniye aralıklarla) güncelleyecektir.

## FSS-PERF-02 (Sistem Tepki Süresi):

Sistem, oturum başlatma ve durdurma işlemlerine 1 saniyeden kısa sürede yanıt verecektir.

## 3.2.5 Kafa Takibi ve Odak Skoru

## 3.2.5.1 Modül Tanımı

Kafa Takibi ve Odak Skoru modülü, kullanıcıın bilgisayar başında çalışırken dikkat seviyesini ölcmek amacıyla geliştirilecektir. Bu modül, bilgisayar kamerasını kullanarak kullanıcıın kafa yönünü analiz edecek ve kullanıcıın ekrana odaklanıp odaklanmadığın belirleyecektir.

Sistem, gerçek zamanlı görüntü işleme teknikleri kullanarak kafa pozisyonunu hesaplayacak ve belirlenen eşik değerlerine göre kullanıcının dikkatinin dağılıp dağılmadığını tespit edecektir. Elde edilen veriler doğrultusunda oturum sonunda bir odaklanma skoru oluşturulacaktır.

Bu modül, sistemin temel analiz bileşenlerinden biri olacaktır ve diğer modüllerle veri paylaşımı gerçekleştircektir.

## 3.2.5.2 Fonksiyonel Gereksinimler

## HTS-REQ-01 (Kamera Başlatma):

Sistem, odaklanma oturumu başlatıldığında kullanıcınin bilgisayar kamerasını otomatik olarak aktif hale getirecek ve görüntü akışını başlatacaktır.

## HTS-REQ-02 (Yüz Tespiti):

Sistem, kamera görüntüsü üzerinde kullanıcınin yüzünü tespit edecek ve yüzün konumunu gerçek zamanlı olarak belirleyecektir.

## HTS-REQ-03 (Kafa Pozisyonu Hesaplama):

Sistem, yüz landmark noktalarını kullanarak kullanıcıın kafa pozisyonunu hesaplayacak ve pitch, yaw ve roll açılarını belirleyecektir.

## HTS-REQ-04 (Referans Odak Açısı Belirleme):

Sistem, odaklanma oturumu başladığında kullanıcıın ekrana baktığı referans kafa açısını belirleyecek ve bu açıyı temel karşılastırma noktası olarak kullanacaktır.

## HTS-REQ-05 (Dikkat Dağılması Tespiti):

Sistem, kullanıcının kafa açısı belirlenen eşik değerlerin dışına çıktığında dikkat dağıldığını tespit edecektir.

## HTS-REQ-06 (Odak Süresi Hesaplama):

Sistem, kullanıcıın referans açı içerisinde kaldığı süreyi hesaplayacak ve bu süreyi odaklanma süresi olarak kaydedecektir.

## HTS-REQ-07 (Odaklanma Skoru Oluşturma):

Sistem, odaklanma süresi ile toplam oturum süresini karşılastırarak yüzde (%) cinsinden bir odaklanma skoru oluşturacaktır.

## HTS-REQ-08 (Yüz Algilanamama Durumu Yönetimi):

Sistem, kamerada yüz algılanamadığında odaklanma sayacını geçici olarak durduracak ve kullanıcıya hem sesli hem de pop-up şeklinde geri bildirim verecektir.

## HTS-REQ-09 (Gerçek Zamanlı Performans):

Sistem, kafa takibi işlemini gerçek zamanlı olarak gerçekleştircek ve kullanıcı deneyimini etkilemeyecek sekilde çalışacaktır.

## HTS-REQ-10 (Veri Aktarimı):

Sistem, oluşturulan odaklanma skorunu ve oturum verilerini sistem veritabanına kaydedecektir.

## 3.2.5.3 Hata Yönetimi Gereksinimleri

## HTS-ERR-01 (Kamera Hatası Yönetimi):

Sistem, kamera erişimi sağlanamadığında kullanıcıyı bilgilendirecek ve odaklanma oturumunun başlatılmasını engelleyecektir.

## HTS-ERR-02 (Düşük Işık Durumu):

Sistem, düşük ışık koşullarında yüz tespit doğruluğun düşmesi durumunda kullanıcıya bilgilendirici bir uyarı gösterecektir.

## HTS-ERR-03 (Takip Kaybı Durumu):

Sistem, kafa takibi kaybolduğunda sistemi otomatik olarak bekleme durumuna alacak ve takip yeniden sağlandığinda devam edecektir.

## 3.2.5.4 Performans Gereksinimleri

## HTS-PERF-01 (FPS Performansi):

Sistem, kamera görüntüsünü gerçek zamanlı olarak işleyerek kafa takibi algoritmasını 15-30 FPS aralığında çalıştıracaktır.

## HTS-PERF-02 (CPU Kullanımı):

Sistem, görüntü işleme işlemlerini optimize ederek toplam cpu kullanımını %25’in altında tutacaktır

## HTS-PERF-03 (Çoklu İş Parçacığı Kullanımı):

Sistem, kamera takibi işlemlerini arayüz performansını etkilemeyecek şekilde multithreading mimarisi ile çalıştıracaktır.

## 3.2.6 Beyaz Liste Kontrolü

## 3.2.6.1 Modül Tanımı

Beyaz Liste Kontrolü modülü, kullanıcının odaklanma oturumu sırasında yalnızca önceden izin verdiği uygulamalar üzerinde çalışmasını desteklemek amacıyla geliştirilecektir. Sistem, odaklanma modu aktifken işletim sistemi üzerinde aktif olan pencereyi ve bu pencereye ait süreç bilgisini belirli aralıklarla denetleyecektir. Kullanıcının beyaz listeye eklediği uygulamalar dışındaki uygulamalar aktif hale geldiğinde sistem bu durumu whitelist ihlali olarak değerlendirecektir.

Modül, kullanıcının izin verdigi uygulama adlarını arayüz üzerinden eklemesine,

göruntülemesine ve kaldırmasına olanak sağlayacaktır. İşletim sisteminin temel çalışması için

gerekli sistem süreçleri ile uygulamanın kendi çalışması için gerekli tanımlı süreçler ihlal

değerlendirmesi dışında tutulacaktır. İzin verilmeyen bir uygulama tespit edildiğinde sistem

kullanıcıya sesli ve görsel uyarı verecek, ihlal bilgilerini oturum süresince takip edecek ve

oturum sonunda bu verileri veritabanına kaydedilmek üzere hazırlayacaktır.

Bu modül, odak oturumu yönetimi, istatistik ve raporlama modülü ile veritabanı altyapısı ile entegre çalışacaktır. Böylece whitelist ihlalleri kullanıcıın odak performansının değerlendirilmesinde ve oturum sonu verimlilik analizlerinde kullanılabilecektir.

## 3.2.6.2 Fonksiyonel Gereksinimler

## WL-REQ-01 (Beyaz Listeye Uygulama Ekleme):

Sistem, kullanıcının izin vermek istediği uygulamaları .exe adı ile beyaz listeye eklemesine olanak tanıyacaktır.

## WL-REQ-02 (Beyaz Listeyi Göruntüleme):

Sistem, kullanıcı tarafından tanımlanan izinli uygulamalar kullanıcı arayüzünde liste halinde gösterecektir.

## WL-REQ-03 (Beyaz Listeden Uygulama Kaldirma):

Sistem, kullanıcının seçtiği izinli uygulamayı beyaz listeden kaldirmasına olanak tanıyacaktır.

## WL-REQ-04 (İzlemeyi Başlatma ve Durdurma):

Sistem, kullanıcıın aktif uygulama izlemesini başlatmasına ve durdurmasına olanak sağlayacaktır.

## WL-REQ-05 (Aktif Uygulama Tespiti):

Sistem, izleme açıkken işletim sisteminde o anda aktif olan pencereyi ve buna ait süreç adını belirli aralıklarla tespit edecektir.

## WL-REQ-06 (İzinli Uygulama Doğrulama):

Sistem, tespit edilen aktif uygulamanın beyaz listede bulunup bulunmadığını kontrol edecektir.

## WL-REQ-07 (Sistem Süreçlerini Hariç Tutma):

Sistem, işletim sisteminin temel çalışması için gerekli tanımlı sistem süreçlerini ihlal değerlendirmesine dahil etmeyecektir.

## WL-REQ-08 (Uygulamanın Kendi Süreçlerini Hariç Tutma):

Sistem, FocuSync uygulamasının kendi çalışması için gerekli tanımlı süreçleri ihlal değerlendirmesine dahil etmeyecektir.

## WL-REQ-09 (Whitelist Ihlali Tespiti):

Sistem, beyaz listede bulunmayan bir uygulama aktif hale geldiğinde bu durumu whitelist ihlali olarak işaretleyecektir.

## WL-REQ-10 (Sesli ve Görsel Uyari):

Sistem, whitelist ihlali tespit edildiğinde kullanıcıya sesli ve görsel bildirim verecektir.

## WL-REQ-11 (İhlal Bilgisinin Gösterimi):

Sistem, kullanıcı arayüzünde ihlal durumunu ve tespit edilen uygulama bilgisini gösterecektir.

## WL-REQ-12 (İhlal Süresi Hesaplama):

Sistem, ihlalin başladığı ve sona erdiği zamanları dikkate alarak toplam ihlal süresini hesaplayacaktır.

## WL-REQ-13 (Toplam İzleme Süresi Hesaplama):

Sistem, izleme başlatıldığı andan izleme sonlandırıldığı ana kadar geçen toplam süreyi hesaplayacaktır.

## WL-REQ-14 (Oturum Sonu İhlal Özeti Oluşturma):

Sistem, odak oturumu veya izleme sona erdiğinde toplam izleme süresi, toplam ihlal süresi ve ihlal detaylarından oluşan oturum özetini oluşturacaktır.

## DB-REQ-07 (Whitelist İhlal Verisinin Kaydedilmesi):

Sistem, whitelist ihlaline ilişkin süre ve log verilerini oturum sonunda veritabanına kaydedecektir.

## DB-REQ-08 (Odak Oturumu ile İlişkilendirme):

Sistem, oluşturulan whitelist ihlal kayıtlarını ilgili kullanıcı ve ilgili odak oturumu ile ilişkilendirecektir.

## DB-REQ-09 (İstatistiklere Veri Sağlama):

Sistem, kaydedilen whitelist ihlal verilerini istatistik ve raporlama modülünün kullanabileceği

şekilde erişilebilir halde tutacaktır.

## 3.2.6.3 Hata Yönetimi Gereksinimleri

## WL-ERR-01 (Geçersiz Uygulama Adı Girişi):

Sistem, kullanıcı uygulama isim girişi .exe uzantısıyla bitmediğinde ekleme işlemini engelleyecek ve kullanıcıya uyarı gösterecektir.

## WL-ERR-02 (Yinelenen Kayıt Engelleme):

Sistem, beyaz listede zaten bulunan bir uygulama yeniden eklenmek istendiğinde kullanıcıyı bilgilendirecek ve aynı kaydın tekrar eklenmesini engelleyecektir.

## WL-ERR-03 (Seçim Yapılmadan Silme Denemesi):

Sistem, kullanıcı listeden bir uygulama seçmeden silme işlemi yapmak istediğinde işlemi durduracak ve kullanıcıya uyarı gösterecektir.

## WL-ERR-04 (İzleme Bağımlılıkların Eksik Olması):

Sistem, aktif pencere ve süreç takibi için gerekli yazılım bağımlılıklar eksik olduğunda izlemeyi başlatmayacak ve kullanıcıyla bilgilendirici hata mesajı gösterecektir.

## WL-ERR-05 (Aktif Pencere Bilgisinin Alınamaması):

Sistem, aktif pencere veya süreç bilgisi alınamadığında uygulamayı sonlandırmayacak, izleme sürecini güvenli biçimde sürdürecek ve ilgili durumu hata toleranslı şekilde yönetecektir.

## WL-ERR-06 (Veri Kaydı Hatası):

Sistem, whitelist ihlal verileri oturum sonunda veritabanına kaydedilemediğinde kullanıcıyı bilgilendirecektir.

## 3.2.6.4 Performans Gereksinimleri

## WL-PERF-01 (Arka Plan İzleme):

Sistem, whitelist denetimini kullanıcı arayüzü performansını etkilemeyecek sekilde arka planda çalışan ayrı bir iş parçacığı veya eşdeğer bir yürütme mekanizması ile gerçekleştircektir.

## WL-PERF-02 (Denetim Aralığı):

Sistem, aktif uygulama denetimini sabit zaman aralıklarıyla gerçekleştircektir.

## WL-PERF-03 (Kaynak Kullanımı):

Sistem, whitelist denetimini sürekli yüksek işlemci kullanımına neden olmayacak şekilde optimize edilmiş aralıklarla yürütecektir.

## WL-PERF-04 (Durum Güncelleme Tepkisi):

Sistem, ihlal durumu değiştiğinde kullanıcı arayüzundeki ihlal bilgisini maksimum 30 saniye gecikme ile güncelleyecektir.

## 3.2.7 Adaptif Zorluk Güncelleme

## 3.2.7.1 Modül Tanımı

Adaptif Zorluk Güncelleme modülü, kullanıcınin başlangıca dersleri için manuel olarak belirlediği zorluk derecelerini, çalışma seanslarından elde edilen gerçek verilerle dinamik olarak revize eden "akıllı karar motoru" olarak görev yapacaktır. Kafa takibi ve odak oturumu modüllerinden gelen odaklanma skorlarını analiz eden sistem, kullanıcınin zorlandığı veya dikkatinin sık dağıldığı dersleri tespit edecektir. Bu analiz sonucunda, ilgili dersin ağirlık katsayısı arka planda sistem tarafindan artırılacak ve kullanıcı için daha kısa çalışma periyotları ile daha sık molalar içeren kişiselleştirilmiş yeni bir odaklanma stratejisi oluşturulacaktır.

## 3.2.7.2 Fonksiyonel Gereksinimler

## ADG-REQ-01 (Odak Skoru Analizi):

Sistem, tamamlanan her odak oturumu sonrasında kafa takip modülüden gelen odaklanma skorunu alacak ve ilgili dersin mevcut zorluk derecesi ile karşılaştırmalı olarak analiz edecektir.

## ADG-REQ-02 (Dinamik Ağırlık Artırımı):

Sistem, kullanıcıın belirli bir dersteki odaklanma skoru arka arkaya eşik değerin altında kaldığında veya sık whitelist ihlali yaşandığında, o dersin zorluk ağirlik katsayısını veritabanında otomatik olarak artıracaktır.

## ADG-REQ-03 (Yeni Strateji Optimizasyonu):

Sistem, zorluk ağırlığı güncellenen (artırılan) dersler için kullanıcının çalışma ve mola sürelerini yeniden hesaplayarak (örneğin; çalışma süresini kısaltıp, mola sıklığını artırarak) optimize edilmiş yeni bir odaklanma stratejisi oluşturacaktır.

## DB-REQ-10 (Strateji Eşitlemesi):

Sistem, oluşturulan yeni adaptif çalışma planlarını ve güncel ders ağırlıklarını, veri kaybını önlemek adına mobil uygulama ile senkronize edilmek üzere anında bulut veritabanına kaydedecektir.

## 3.2.7.3 Hata Yönetimi Gereksinimleri

## ADG-ERR-01 (Yetersiz Veri Durumu):

Sistem, odak oturumunun kullanıcı tarafından çok kısa bir süre içinde iptal edilmesi veya kafa takibi algoritmasının yeterli veri toplayamaması durumunda, yanıltıcı sonuçları önlemek için o oturuma ait verileri zorluk güncelleme hesaplamasına dahil etmeyecektir.

## 3.2.7.4 Performans Gereksinimleri

## ADG-PERF-01 (Uç Değer Koruması - Overfitting):

Sistem, algoritmanın çalışma programını mantıksiz uç değerlere taşımasını (örneğin mola süresini tamamen sıfırlaması veya çalışma süresini 5 dakikaya düşürmesi) engellemek amacıyla, matematiksel model çıktılarını sabit (hard-coded) alt ve üst limitler çerçevesinde tutacaktır.

## 3.2.8 İstatistik ve Raporlama

## 3.2.8.1 Modül Tanımı

İstatistik ve Raporlama modülü, sistemdeki diğer tüm modüllerin (Kafa Takibi, Odak Oturumu, Beyaz Liste) ürettiği verileri anlamlı analizlere dönüştürerek kullanıcıyla sunan raporlama bileşenidir. Sistem, kullanıcının verimlilik trendlerini, ders bazlı performansını ve dikkat dağıtıcı unsurları (ihlalleri) derleyerek hem masaüstü hem de mobil arayüzde gösterilebilecek istatistiksel özetler üretecektir. Bu modül sayesinde kullanıcı, kendi çalışma alşkanlıklarını ve gelişime açık yönlerini grafiksel veriler üzerinden takip edebilecektir.

## 3.2.8.2 Fonksiyonel Gereksinimler

## IVR-REQ-01 (Günlük Verimlilik Özeti):

Sistem; kullanıcınin o gün içindeki toplam çalışma süresini, ortalama odaklanma skorunu ve toplam whitelist ihlal sayısını hesaplayarak gün sonu raporu oluşturacaktır.

## IVR-REQ-02 (Ders Bazlı Performans Raporlaması):

Sistem, her bir ders için özel olarak harcanan toplam süreyi ve bu derslerde elde edilen ortalama odaklanma skorlarını filtreleyerek ders bazlı verimlilik sıralaması yapacaktır.

## IVR-REQ-03 (Dikkat Dağıtıcı Analizi):

Sistem, beyaz liste (whitelist) kontrol modülünden gelen ihlal kayıtlarını analiz ederek, odaklanmayı en çok bölen ilk 3 uygulamayı tespit edecek ve kullanıcıya raporlayacaktır.

## IVR-REQ-04 (Haftalık/Aylik Trend Oluşturma):

Sistem, günlük verileri birleştirerek kullanıcının haftalık ve aylık bazdaki odaklanma eğilimlerini (skor artışı veya azalışı) sunmak üzere tarihsel veritabanı sorguları oluşturacaktır.

## 3.2.8.3 Hata Yönetimi Gereksinimleri

## IVR-ERR-05 (Veri Çekme Hatası):

Sistem, istatistikleri oluşturmak için bulut veritabanına bağlanamadığında uygulamanın çökmesini engelleyecek, kullanıcıya "Veriler Güncellenmedi" uyarısı göstererek varsa cihazdaki önbellege alınmış son istatistikleri sunacaktır.

## 3.2.9 Mobil Senkronizasyon

## 3.2.9.1 Modül Tanımı

FocuSync mobil uygulaması, kullanıcıın masaüstü platformunda oluşturduğu verilere dilediği zaman erişebilmesini sağlayan tamamlayıcı bir arayüz olarak tasarlanmıştır. Sistem, kullanıcı deneyimini kesintiye uğratmadan cihazlar arası eş zamanlı veri aktarımını sağlayacaktır.

## 3.2.9.2 Fonksiyonel Gereksinimler

## MS-REQ-01 (Kimlik Doğrulama ve Veri Bağlantısı):

Sistem, güvenli bir giriş ve kayıt (Login/Register) yapısı sunacak ve kullanıcının kişisel verilerini mobil uygulama ile masaüstü uygulaması arasında kesintisiz olarak senkronize edecektir.

## MS-REQ-02 (Eş Zamanlı Veri Erişimi):

Mobil uygulama doğrudan ana veritabanı ile eşzamanlı olarak çalışarak güncel ders programlarını, manuel veya PDF üzerinden aktarılan sınav tarihlerini, günlük çalışma planlarını ve detaylı odaklanma istatistiklerini kullanıcıya sunacaktır.

## 3.2.9.3 Performans Gereksinimleri

## MS-PERF-01 (Senkronizasyon Hızı):

Cihazın ağ bağlantısı stabilken sunucu ile mobil uygulama arasındaki verilerin (maksimum 5 MB) çekilme işlemi en fazla 10 saniye içerisinde tamamlanacaktır.

## 3.2.9.4 Hata Yönetimi Gereksinimleri

## MS-ERR-01 (Bağlantı ve Kesinti Yönetimi):

Mobil uygulama ile sunucu bağlantısı sağlanamadığı durumlarda sistem kullanıcıya bağlantı hatası uyarısı verecek, ağ bağlantısı tekrar sağlandığında ise arayüz otomatik olarak en güncel verilerle yenilenecektir.

## 3.3 Yazılım Sistem Nitelikleri

## 3.3.1 Güvenilirlik

## SYS-REQ-01:

Kafa takibi sırasında yüz tespit edilememesi veya kaybolması durumunda sistem çökmek yerine odaklanma sayacını duraklatacak ve kullanıcıya sesli veya görsel bir uyarı verecektir.

## SYS-REQ-02:

İnternet bağlantısının kopması veya veritabanı iletişiminin sağlanamaması durumunda sistem veritabanı işlemlerini durduracak ve işlemlerin devam edebilmesi için kullanıcıya internet bağlantısını kontrol etmesi yönünde bir uyarı mesajı gösterecektir.

## 3.3.2 Kullanılabilirlik

## SYS-REQ-03:

Masaüstü uygulaması, çevrimdışı (offline) durumlarda da asgari düzeyde çalışacak ve temel işlevlerini sürekli bir internet bağlantısı gerektireden yerine getirecektir.

## SYS-REQ-04:

Sistem, Firebase bulut altyapısı üzerinden masaüstü ve mobil platformlar arasında еşzamanlı veri erişimini kesintisiz olarak sağlayacaktır.

## 3.3.3 Güvenlik

## SYS-REQ-05:

Veritabanına yönelik tüm okuma, yazma ve güncelleme işlemleri yalnızca yetkilendirilmiş bir merkezi veritabanı yöneticisi modülü (Admin SDK/Private Key) üzerinden gerçekleştirilecektir.

## 3.3.4 Bakım Yapılabilirlik

## SYS-REQ-06:

Veritabanındaki tüm dokümanlar, adaptif algoritmanın zamanla yapacağı güncellemelere uyum sağlayabilmesi için esnek şemalı JSON formatında tutulacaktır.

## SYS-REQ-07:

Sistem geliştirme ortamı, kodların yönetimi ve ekip içi iş birliğinin sağlanabilmesi için Git/GitHub versiyon kontrolü ile izlenecektir.

## 3.3.5 Taşınabilirlik

## SYS-REQ-08:

Masaüstü uygulamasının çalışması ve "Beyaz Liste" denetim mekanizması, işletim sistemi API'leriyle uyumlu olarak Windows 10 ve Windows 11 (64-bit) üzerinde sorunsuz çalıştırılacaktır.

## SYS-REQ-09:

Sistem, cihazlar arası veri transferini sağlamak adına ileride farklı platformlar tarafından okunup yazılabilecek NoSQL tabanlı evrensel bir veritabanı yapısı kullanacaktır.

## 3.3.6 Performans

## SYS-REQ-10:

Kamera takibi, Beyaz Liste denetimi ve arayüz süreçleri, kullanıcı arayüzunde donmalara yol açmamak için multithreading (çoklu iş parçacığı) mimarisi ile eszamanlı olarak çalıştırılacaktır.

## SYS-REQ-11:

Sistem, kafa takibi algoritmasını 15-30 FPS aralığında çalıştıracak ve görüntü işleme işlemlerini optimize ederek toplam işlemci (CPU) kullanımını %25'in altında tutacaktır.

SYS-REQ-12:

Sistem, oturum başlatma ve durdurma komutlarına 1 saniyeden daha kısa bir sürede yanıt verecektir.

## 3.3.7 Kullanım Kolaylığı

## SYS-REQ-13:

Sistem, OCR mekanizmasının hatalı çalışması durumunda oluşabilecek yanlış veri aktarımlarını önlemek adına, kullanıcıının ders programını manuel olarak düzenleyebileceği bir onay arayüzü sunacaktır.

## 3.3.8 Gizlilik

## SYS-REQ-14:

Kamera takibi modülü ham görüntü verilerini kesinlikle buluta aktarmayacak veya yerel olarak kaydetmeyecek; yalnızca türetilmiş verileri (açı değerleri ve odaklanma skoru) hesaplayarak saklayacaktır.

## 3.4 Veritabanı Gereksinimleri

FocuSync sistemi, veri depolama ve senkronizasyon altyapısı olarak bulut tabanlı, NoSQL mimarisine sahip Google Firebase Firestore kullanacaktır. Sistemin esnek yapısı, kullanıcı istatistiklerinin ve adaptif algoritmaların anlık olarak işlenmesine olanak tanır.

DB-REQ-11 (Veri Modelleri): Sistem; kullanıcı profillerini, ders içeriklerini, haftalık akademik programları, çalışma planlarını, odaklanma oturumu istatistiklerini ve beyaz liste (whitelist) ihlallerini birbirinden izole edilmiş koleksiyonlar (Collections) halinde saklamaldır.

DB-REQ-12 (Veri Formatı): Veritabanındaki tüm dokümanlar (Documents), adaptif algoritmanın güncellemelerine uyum sağlayabilmesi için esnek şemalı JSON formatında tutulmalıdır.

DB-REQ-13 (İlişkisel Bütünlük): NoSQL mimarisi kullanılmasına rağmen veri tutarlılığın sağlamak için sistem; dersler, planlar ve oturumlar gibi alt verileri benzersiz kullanıcı kimlikleri (User ID) ve ders referansları (Course ID) ile birbirine bağlamaldır.

DB-REQ-14 (Merkezi Erişim ve Güvenlik): Veritabanı, istemci (kullanıcı) tarafındaki doğrudan erişimlere tamamen kapalı olmalı; tüm okuma, yazma ve güncelleme işlemleri yalnızca yetkilendirilmiş bir merkezi veritabanı yöneticisi modülü (Admin SDK/Private Key) üzerinden gerçekleştirilmelidir.

DB-REQ-15 (Eşzamanlılık): Sistem, masaüstü uygulamasında veya arka plan süreçlerinde (kamera takibi, ihlal denetimi) üretilen verileri, anlık olarak (real-time) bulut veritabanına yansıtmalı ve mobil arayüzle senkronize etmelidir.

4. Ek Materyaller