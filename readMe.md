# FocuSync - Geliştirici Kurulum Rehberi 🚀

Herkese selam! Projede kullandığımız kütüphanelerin (PyQt6, Firebase vb.) birbirine girmemesi ve hepimizin bilgisayarında aynı sürümlerle sorunsuz çalışabilmesi için projeyi **Sanal Ortam (Virtual Environment - venv)** kullanarak geliştireceğiz.

Böylece kimsenin bilgisayarına gereksiz paket inmeyecek, her şey sadece bu proje klasörüne özel kalacak. Lütfen projeyi çektikten sonra kod yazmaya başlamadan önce aşağıdaki adımları sırasıyla uygulayın.

## 1. Sanal Ortamı (venv) Oluşturma

Terminalinizi (veya Komut İstemini) proje klasörünün içinde açın ve işletim sisteminize göre şu komutu çalıştırarak yalıtılmış çalışma odamızı inşa edin:

- **Windows için:** `python -m venv venv`
- **Mac/Linux için:** `python3 -m venv venv`

_(Bu komut klasörde `venv` adında bir dosya oluşturacak. Bu dosyanın içine manuel olarak ASLA dokunmuyoruz.)_

## 2. Sanal Ortamı Aktifleştirme (İçeri Girme)

Oluşturduğumuz bu ortama girmeden paket indiremeyiz veya kod çalıştıramayız. Yine işletim sisteminize göre şu komutu çalıştırın:

- **Windows için:** `venv\Scripts\activate`
- **Mac/Linux için:** `source venv/bin/activate`

_(Başarılı olduğunuzda terminal satırınızın en başında `(venv)` yazısını göreceksiniz. Kod yazarken ve çalıştırırken hep bu ortamın içinde olmalısınız.)_

## 3. Gerekli Kütüphaneleri Tek Tıkla Kurma

Artık ortamın içindeyiz. Şimdi projede kullandığımız kütüphanelerin birebir aynı sürümlerini kendi bilgisayarınıza kurmak için şu komutu çalıştırın:

`pip install -r requirements.txt`

Hepsi bu kadar! Artık projeyi çalıştırmaya hazırsınız.

---

## 💡 ÖNEMLİ BİLGİ: Dosyalarımızı Nereye Açacağız?

Sanal ortam oluşturduk diye yeni açacağımız kod dosyalarını (`.py`, `.md` vb.) `venv` klasörünün içine **KOYMUYORUZ**.

- Yazdığımız tüm kodlar her zaman ana proje klasöründe (`FocuSync`), `venv` klasörüyle yan yana durmalıdır.
- `venv` klasörü sadece indirdiğimiz kütüphanelerin (PyQt6, Firebase vb) tutulduğu **kilitli bir depodur**.
- Terminalde `(venv)` yazması, dosyaların nereye kaydedileceğini değil; yazdığınız kodun bilgisayardaki Python ile değil, bu deponun içindeki kütüphanelerle çalıştırılacağını belirtir.

## 🛡️ GÜVENLİK VE GİT: Neden .gitignore Kullanıyoruz?

Projemizde bir `.gitignore` dosyası var ve içine `venv/` ile `serviceAccountKey.json` ekledik. Bunun iki devasa sebebi var:

1. **Neden venv'i GitHub'a atmıyoruz?** `venv` klasörü çok büyük boyutludur ve işletim sistemine özel (Mac/Windows) dosyalar barındırır. Eğer GitHub'a atarsak hem saatlerce yükleme bekleriz hem de Mac'te oluşturulan bir `venv`, Windows kullanan birinde asla çalışmaz. Bu yüzden herkes `venv`'i kendi bilgisayarında yerel olarak kurar.
2. **Neden serviceAccountKey.json'ı atmıyoruz?** Bu dosya, veritabanımızın VIP giriş kartıdır (şifresidir). GitHub'a yüklemek, veritabanı anahtarımızı herkese açık hale getirmek demektir. Veritabanı testleri yapacağınız zaman bu JSON dosyasını benden (Yunus'tan) şahsen isteyin ve klasörünüze kendiniz yapıştırın.


# 🗄️ Veritabanı Mimarisi ve Güvenlik Stratejisi

FocuSync projesinde veritabanı olarak **Google Firebase Firestore** kullanılmaktadır.  
Geliştirme sürecini hızlandırmak ve güvenliği en üst seviyede tutmak için **Private Key (Admin SDK)** yöntemi tercih edilmiştir.

---

## 🔑 Neden Private Key Kullanıyoruz?

### ✅ Tam Yetki
Her geliştirici, **Database Admin** yetkisine sahiptir ve tüm koleksiyonlara doğrudan erişebilir.

### 🔒 Güçlü Güvenlik
- Veritabanı dış dünyaya tamamen kapalıdır  
- Sadece `serviceAccountKey.json` dosyasına sahip yetkili geliştiriciler erişebilir  

### ⚡ Hız
Authentication süreçleriyle uğraşmadan:
- Doğrudan veri işlemleri yapılabilir  
- Geliştirme süreci hızlanır  
- İş mantığına odaklanılır  

---

## 📊 NoSQL (Document-Based) Yapı

Firestore bir **NoSQL veritabanıdır** ve şu yapı ile çalışır:

- 📁 **Collections (Koleksiyonlar)**
- 📄 **Documents (Dokümanlar)**

### Özellikler:
- Veriler JSON formatında tutulur  
- Esnek şema yapısı vardır  
- İlişkiler `user_id` gibi alanlar üzerinden kurulur  

---

## 📑 Veritabanı Koleksiyon Yapısı

Tüm veri akışı `DatabaseManager` sınıfı üzerinden yönetilir.

### 👤 Users
Kullanıcı hesap bilgileri

{
  "email": "string",
  "password": "string",
  "role": "string"
}

---

### 📚 Courses

Ders bilgileri ve zorluk seviyeleri

{
  "course_name": "string",
  "difficulty_level": "string",
  "exam_date": "timestamp",
  "user_id": "string"
}

---

### 📅 Schedules

PDF'ten alınan ders programı

{
  "day": "string",
  "course_name": "string",
  "start_time": "string",
  "end_time": "string",
  "type": "string",
  "user_id": "string"
}

---

### 🧠 StudyPlans

Algoritma tarafından oluşturulan çalışma planı

{
  "course_name": "string",
  "planned_date": "timestamp",
  "planned_duration": "number",
  "is_completed": "boolean",
  "user_id": "string"
}

---

### 🎯 FocusSessions

Gerçekleşen odaklanma verileri (kamera tabanlı)

{
  "study_plan_id": "string",
  "course_name": "string",
  "actual_focus_time": "number",
  "focus_score": "number",
  "status": "string",
  "timestamp": "timestamp",
  "user_id": "string"
}

---

### 🚫 Violations

Whitelist dışı uygulama ihlalleri

{
  "session_id": "string",
  "app_name": "string",
  "duration": "number",
  "timestamp": "timestamp",
  "user_id": "string"
}

---

## 🛠️ Geliştirici Kullanım Rehberi

Tüm veritabanı işlemleri `db_manager.py` üzerinden yapılmalıdır.

### 👥 Rol Bazlı Fonksiyon Kullanımı

| Geliştirici      | Sorumluluk     | Kullanacağı Fonksiyonlar           |
|------------------|---------------|-----------------------------------|
| Zeynep Yamaç     | Algoritma      | `add_study_plan()`, `add_course()` |
| Mehmet Akif Türk | Görüntü İşleme | `add_focus_session()`              |
| Kerem Kapısız    | Arayüz         | `add_violation()`                  |
| Yunus Recepoğlu  | DB & Otomasyon | `add_base_schedule()`              |

---

## ⚠️ Önemli Notlar

- ❗ Veritabanına **doğrudan erişim yapılmamalıdır**
- ❗ Tüm işlemler `DatabaseManager` üzerinden gerçekleştirilmelidir
- 🔐 `serviceAccountKey.json` dosyası **asla public repoya yüklenmemelidir**
```

