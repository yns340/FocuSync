<div align="center">

# 🎯 FocuSync

### Geliştirici Kurulum Rehberi

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

</div>

<br>

---

<div align="center">

# 🌐 SANAL ORTAM KULLANIMI 🌐

</div>

---

<br>

Herkese selam! Projede kullandığımız kütüphanelerin (PyQt6, Firebase vb.) birbirine girmemesi ve hepimizin bilgisayarında aynı sürümlerle sorunsuz çalışabilmesi için projeyi **Sanal Ortam (Virtual Environment - venv)** kullanarak geliştireceğiz.

Böylece kimsenin bilgisayarına gereksiz paket inmeyecek, her şey sadece bu proje klasörüne özel kalacak. Lütfen projeyi çektikten sonra kod yazmaya başlamadan önce aşağıdaki adımları sırasıyla uygulayın.

---

## 1. Sanal Ortamı (venv) Oluşturma

Terminalinizi (veya Komut İstemini) proje klasörünün içinde açın ve işletim sisteminize göre şu komutu çalıştırarak yalıtılmış çalışma odamızı inşa edin:

| İşletim Sistemi   | Komut                  |
| ----------------- | ---------------------- |
| 🪟 Windows        | `python -m venv venv`  |
| 🍎 Mac / 🐧 Linux | `python3 -m venv venv` |

> _Bu komut klasörde `venv` adında bir dosya oluşturacak. Bu dosyanın içine manuel olarak **ASLA** dokunmuyoruz._

---

## 2. Sanal Ortamı Aktifleştirme (İçeri Girme)

Oluşturduğumuz bu ortama girmeden paket indiremeyiz veya kod çalıştıramayız. Yine işletim sisteminize göre şu komutu çalıştırın:

| İşletim Sistemi   | Komut                      |
| ----------------- | -------------------------- |
| 🪟 Windows        | `venv\Scripts\activate`    |
| 🍎 Mac / 🐧 Linux | `source venv/bin/activate` |

> _Başarılı olduğunuzda terminal satırınızın en başında `(venv)` yazısını göreceksiniz. Kod yazarken ve çalıştırırken hep bu ortamın içinde olmalısınız._

---

## 3. Gerekli Kütüphaneleri Tek Tıkla Kurma

Artık ortamın içindeyiz. Şimdi projede kullandığımız kütüphanelerin birebir aynı sürümlerini kendi bilgisayarınıza kurmak için şu komutu çalıştırın:

```bash
pip install -r requirements.txt
```

✅ Hepsi bu kadar! Artık projeyi çalıştırmaya hazırsınız.

---

## 💡 ÖNEMLİ BİLGİ: Dosyalarımızı Nereye Açacağız?

Sanal ortam oluşturduk diye yeni açacağımız kod dosyalarını (`.py`, `.md` vb.) `venv` klasörünün içine **KOYMUYORUZ**.

- Yazdığımız tüm kodlar her zaman ana proje klasöründe (`FocuSync`), `venv` klasörüyle yan yana durmalıdır.
- `venv` klasörü sadece indirdiğimiz kütüphanelerin (PyQt6, Firebase vb) tutulduğu **kilitli bir depodur**.
- Terminalde `(venv)` yazması, dosyaların nereye kaydedileceğini değil; yazdığınız kodun bilgisayardaki Python ile değil, bu deponun içindeki kütüphanelerle çalıştırılacağını belirtir.

```
📁 FocuSync/                      ← Tüm .py dosyaları buranın altına
├── 📁 venv/                      ← Sanal kütüphaneler (!!!! BURAYA DOKUNULMAYACAK, EKLEMELER BURAYA YAPILMAYACAK !!!!)
├── 📁 ui/
├── 📄 db_manager.py              ← Tüm database işlemleri (Firebase Firestore) buradan yapılacak, ek bir db işlemi yapılmayacak
├── 📄 main.py
├── 📄 requirements.txt           ← Sanal ortama yüklenecek kütüphaneler (ihtiyacımız olan yeni kütüphaneler olursa buraya eklenmeli - diğerlerinin de güncel kütüphaneleri sanal ortamına yüklemesi için)
├── 📄 readMe.md
├── 📄 serviceAccountKey.json     ← Firestore private key (Yunustan istenmeli)
└── 📄 .gitignore                 ← venv klasörü gibi büyük sanal dosyaların veya json keyin github a gitmemesi için
```

---

## 🛡️ GÜVENLİK VE GİT: Neden .gitignore Kullanıyoruz?

Projemizde bir `.gitignore` dosyası var ve içine `venv/` ile `serviceAccountKey.json` ekledik. Bunun iki devasa sebebi var:

> **1. Neden venv'i GitHub'a atmıyoruz?**
> `venv` klasörü çok büyük boyutludur ve işletim sistemine özel (Mac/Windows) dosyalar barındırır. Eğer GitHub'a atarsak hem saatlerce yükleme bekleriz hem de Mac'te oluşturulan bir `venv`, Windows kullanan birinde asla çalışmaz. Bu yüzden herkes `venv`'i kendi bilgisayarında yerel olarak kurar.

> **2. Neden serviceAccountKey.json'ı atmıyoruz?**
> Bu dosya, veritabanımızın VIP giriş kartıdır (şifresidir). GitHub'a yüklemek, veritabanı anahtarımızı herkese açık hale getirmek demektir. Veritabanı testleri yapacağınız zaman bu JSON dosyasını benden (Yunus'tan) şahsen isteyin ve klasörünüze kendiniz yapıştırın.

<br><br>

---

<div align="center">

# 🗄️ VERİTABANI MİMARİSİ 🗄️

</div>

---

<br>

# 🧱 VERİTABANI MİMARİSİ & GÜVENLİK STRATEJİSİ

> ⚠️ Bu bölüm, proje içerisindeki diğer tüm geliştirmelerden **KESKİN şekilde ayrılır**.  
> Veritabanı erişimi, güvenlik ve veri akışı ile ilgili **tüm kurallar burada tanımlanmıştır**.  
> Bu standartların dışına çıkılması sistem bütünlüğünü ve güvenliği riske atar.

---

## 🗄️ Veritabanı Mimarisi

FocuSync projesinde veritabanı olarak **Google Firebase Firestore** kullanılmaktadır.  
Geliştirme sürecini hızlandırmak ve maksimum güvenlik sağlamak amacıyla **Private Key (Admin SDK)** yöntemi tercih edilmiştir.

---

## 🔑 Neden Private Key Kullanıyoruz?

<table>
<tr>
<td width="33%" align="center">

### ✅ Tam Yetki

Tüm geliştiriciler **Database Admin** yetkisine sahiptir.  
Koleksiyonlara doğrudan erişim sağlanır.

</td>
<td width="33%" align="center">

### 🔒 Güçlü Güvenlik

Veritabanı dış dünyaya **tamamen kapalıdır**.  
Sadece `serviceAccountKey.json` dosyasına sahip kişiler erişebilir.

</td>
<td width="33%" align="center">

### ⚡ Hız ve Verimlilik

Authentication süreçleri yok.  
Doğrudan veri işlemleri yapılabilir.  
Geliştirme süreci hızlanır.

</td>
</tr>
</table>

---

## 📊 Firestore Veri Yapısı (NoSQL)

```
Firestore
├── 📁 Collections
│   └── 📄 Documents
│       ├── JSON formatında veri
│       ├── Esnek şema
│       └── user_id ile ilişki kurma
```

---

## 📑 Koleksiyon Yapısı

> ⚠️ Tüm işlemler sadece `DatabaseManager` sınıfı üzerinden `(db_manager.py dosyası)` yapılmalıdır.

---

# 📘 Veritabanı Şeması & Geliştirici Rehberi

---

## 📦 Koleksiyonlar

### 👤 Users

| Alan               | Tip      | Açıklama                        |
| ------------------ | -------- | ------------------------------- |
| `allowed_apps`     | string[] | Kullanıcının whitelist izinleri |
| `daily_study_goal` | number   | Kullanıcı çalışma süresi hedefi |
| `email`            | string   | Kullanıcı email                 |
| `name`             | string   | Kullanıcı isim                  |
| `password`         | string   | Şifre                           |
| `role`             | string   | Kullanıcı rolü                  |
| `school`           | string   | Kullanıcı okul                  |
| `surname`          | string   | Kullanıcı soyad                 |

```json
{
  "allowed_apps": ["string"],
  "daily_study_goal": "number",
  "email": "string",
  "name": "string",
  "password": "string",
  "role": "string",
  "school": "string",
  "surname": "string"
}
```

---

### 📚 Courses

> **Doküman ID:** `{user_id}_{course_id}` (Composite Key — çakışmaları önler)

| Alan               | Tip     | Açıklama                                           |
| ------------------ | ------- | -------------------------------------------------- |
| **`user_id`**      | string  | Kullanıcı referansı                                |
| **`course_id`**    | string  | Ders referansı                                     |
| `course_name`      | string  | Ders adı                                           |
| `difficulty_level` | number  | Zorluk seviyesi (algoritma tarafından güncellenir) |
| `weekly_hours`     | number  | Haftalık ders saati (okuldaki kredi/sıklık)        |
| `exam_date`        | string  | Sınav tarihi (Exams ile senkronize)                |
| `exam_weights`     | object  | Sınav ağırlıkları sözlüğü                          |
| `exam_grades`      | object  | Sınav notları sözlüğü (Exams ile senkronize)       |
| `target_grade`     | number  | Hedef not                                          |
| `is_active`        | boolean | Güncel programda mı, yoksa arşivde mi?             |

```json
{
  "user_id": "string",
  "course_id": "string",
  "course_name": "string",
  "difficulty_level": "number",
  "weekly_hours": "number",
  "exam_date": "string",
  "exam_weights": {
    "Vize": "number",
    "Final": "number"
  },
  "exam_grades": {
    "Vize": "string",
    "Final": "string"
  },
  "target_grade": "number",
  "is_active": "boolean"
}
```

---

### 📅 Schedules

| Alan             | Tip       | Açıklama                   |
| ---------------- | --------- | -------------------------- |
| **`user_id`**    | string    | Kullanıcı referansı        |
| `schedule_name`  | string    | Program dönem adı          |
| `updated_at`     | timestamp | Programın yüklenme tarihi  |
| `weekly_routine` | object    | Günlere göre ders programı |

#### `weekly_routine[gun][]` — Dizi Elemanı

| Alan            | Tip    | Açıklama        |
| --------------- | ------ | --------------- |
| **`course_id`** | string | Ders referansı  |
| `course_name`   | string | Ders adı        |
| `start_time`    | string | Başlangıç saati |
| `end_time`      | string | Bitiş saati     |
| `type`          | string | Etkinlik türü   |

```json
{
  "user_id": "string",
  "schedule_name": "string",
  "updated_at": "timestamp",
  "weekly_routine": {
    "Pazartesi": [
      {
        "course_id": "string",
        "course_name": "string",
        "start_time": "string",
        "end_time": "string",
        "type": "string"
      }
    ],
    "Salı": [],
    "Çarşamba": [],
    "Perşembe": [],
    "Cuma": [],
    "Cumartesi": [],
    "Pazar": []
  }
}
```

---

### 🧠 StudyPlans

| Alan              | Tip       | Açıklama                        |
| ----------------- | --------- | ------------------------------- |
| **`user_id`**     | string    | Kullanıcı referansı             |
| `plan_start_date` | timestamp | Planın başlangıç tarihi         |
| `weekly_sessions` | object    | Günlere göre çalışma oturumları |

#### `weekly_sessions[gun][]` — Dizi Elemanı

| Alan               | Tip     | Açıklama                                |
| ------------------ | ------- | --------------------------------------- |
| **`session_id`**   | string  | Oturum ID (örn: `session1`, `session2`) |
| **`course_id`**    | string  | Ders referansı                          |
| `course_name`      | string  | Ders adı                                |
| `planned_duration` | number  | Planlanan süre (dakika)                 |
| `is_completed`     | boolean | Tamamlandı mı?                          |

```json
{
  "user_id": "string",
  "plan_start_date": "timestamp",
  "weekly_sessions": {
    "Pazartesi": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Salı": [],
    "Çarşamba": [],
    "Perşembe": [],
    "Cuma": [],
    "Cumartesi": [],
    "Pazar": []
  }
}
```

---

### 🎯 FocusSessions

| Alan                        | Tip       | Açıklama                         |
| --------------------------- | --------- | -------------------------------- |
| **`user_id`**               | string    | Kullanıcı referansı              |
| **`study_plan_session_id`** | string    | StudyPlan `session_id` referansı |
| **`course_id`**             | string    | Ders referansı                   |
| `actual_focus_time`         | number    | Gerçek odak süresi (dakika)      |
| `head_tilt_degree`          | number    | Kafa eğimi açı değeri            |
| `focus_score`               | number    | Odak skoru                       |
| `status`                    | string    | Oturum durumu                    |
| `timestamp`                 | timestamp | Oturum zamanı                    |

```json
{
  "user_id": "string",
  "study_plan_session_id": "string",
  "course_id": "string",
  "actual_focus_time": "number",
  "head_tilt_degree": "number",
  "focus_score": "number",
  "status": "string",
  "timestamp": "timestamp"
}
```

---

### 🚫 Violations

| Alan                   | Tip       | Açıklama                |
| ---------------------- | --------- | ----------------------- |
| **`user_id`**          | string    | Kullanıcı referansı     |
| **`focus_session_id`** | string    | FocusSession referansı  |
| `app_name`             | string    | İhlal eden uygulama adı |
| `duration`             | number    | İhlal süresi (saniye)   |
| `timestamp`            | timestamp | İhlal zamanı            |

```json
{
  "user_id": "string",
  "focus_session_id": "string",
  "app_name": "string",
  "duration": "number",
  "timestamp": "timestamp"
}
```

---

### 🛡️ WhitelistSessions

| Alan                         | Tip       | Açıklama                            |
| ---------------------------- | --------- | ----------------------------------- |
| **`user_id`**                | string    | Kullanıcı referansı                 |
| `total_duration_seconds`     | number    | Toplam seans süresi (saniye)        |
| `violation_duration_seconds` | number    | Toplam ihlal süresi (saniye)        |
| `total_duration_hms`         | string    | Toplam süre (okunabilir, SS:DD:SN)  |
| `violation_duration_hms`     | string    | İhlal süresi (okunabilir, SS:DD:SN) |
| `violation_count`            | number    | Toplam ihlal sayısı                 |
| `violations`                 | object[]  | İhlal detayları listesi             |
| `session_started_at`         | timestamp | Seans başlangıç zamanı              |
| `session_ended_at`           | timestamp | Seans bitiş zamanı                  |
| `saved_at`                   | timestamp | Kaydedilme zamanı                   |

```json
{
  "user_id": "string",
  "total_duration_seconds": "number",
  "violation_duration_seconds": "number",
  "total_duration_hms": "string",
  "violation_duration_hms": "string",
  "violation_count": "number",
  "violations": [
    {
      "app_name": "string",
      "duration": "number"
    }
  ],
  "session_started_at": "timestamp",
  "session_ended_at": "timestamp",
  "saved_at": "timestamp"
}
```

---

### 📝 Exams

| Alan                 | Tip       | Açıklama              |
| -------------------- | --------- | --------------------- |
| **`user_id`**        | string    | Kullanıcı referansı   |
| `exam_schedule_name` | string    | Sınav takvimi adı     |
| `updated_at`         | timestamp | Son güncelleme zamanı |
| `exams`              | object[]  | Sınav listesi         |

#### `exams[]` — Dizi Elemanı

| Alan            | Tip    | Açıklama                                         |
| --------------- | ------ | ------------------------------------------------ |
| **`course_id`** | string | Ders referansı                                   |
| `exam_type`     | string | Sınav türü (örn: `Vize`, `Final`)                |
| `exam_date`     | string | Sınav tarihi                                     |
| `exam_grade`    | string | Sınav notu (Courses tablosuna senkronize edilir) |

```json
{
  "user_id": "string",
  "exam_schedule_name": "string",
  "updated_at": "timestamp",
  "exams": [
    {
      "course_id": "string",
      "exam_type": "string",
      "exam_date": "string",
      "exam_grade": "string"
    }
  ]
}
```

---

## 🛠️ Geliştirici Kullanım Rehberi

### 👥 Rol Bazlı Dağılım

| Geliştirici          | Sorumluluk                 | Fonksiyonlar (db_manager.py)                                                                                                                                        |
| :------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Zeynep Yamaç**     | Akıllı Algoritma           | `add_course()`, `save_study_plan()`, `get_study_plan()`, `get_courses()`, `update_course_difficulty()`                                                              |
| **Mehmet Akif Türk** | Görüntü İşleme (Kamera)    | `add_focus_session()`, `mark_session_completed()`                                                                                                                   |
| **Kerem Kapısız**    | Beyaz Liste & İhlal Takibi | `add_violation()`                                                                                                                                                   |
| **Yunus Recepoğlu**  | DB, OCR & Core Arayüz      | `login_user()`, `register_user()`, `get_user_profile()`, `update_user_profile()`, `get_dashboard_stats()`, `save_schedule()`, `get_schedule()`, `delete_schedule()` |

---

### ⚠️ Kritik Kurallar

> ❗ Direkt DB erişimi **YASAK** (SQLite, SQL gibi yerel yeni metodlar oluşturulmayacak, her şey yazılan db_manager.py dosyasından)
>
> ❗ Sadece `DatabaseManager (db_manager.py dosyası)` kullanılmalı

#### 🔐 `serviceAccountKey.json`

- Public repo'ya **yüklenemez**
- Sadece **yetkili kişilerde** bulunur

---

## 🔚 Sistem Hedefi

| Hedef         | Açıklama                        |
| ------------- | ------------------------------- |
| 🔒 Güvenlik   | Yetkisiz erişimin önlenmesi     |
| ⚡ Performans | Hızlı ve verimli veri işleme    |
| 🧩 Modülerlik | Bağımsız, genişletilebilir yapı |
| 🛠️ Yönetim    | Kolay bakım ve güncelleme       |

---

<br>

---

## 🔐 Firebase Veritabanı ve Güvenlik Mimarisi (ÖNEMLİ NOTLAR!)

Projemizdeki Firebase veritabanı erişimi, Masaüstü (Python) ve Mobil (İstemci/Client) taraflarında tamamen farklı mimarilerle çalışmaktadır. Geliştirme sürecinde veritabanı bağlantı hatası almamak ve güvenlik açığı yaratmamak için aşağıdaki kurallara mutlaka dikkat edilmelidir:

### 1. Masaüstü Uygulaması (Python) 🖥️

- **Bağlantı Yöntemi:** `firebase_admin` kütüphanesi ve `serviceAccountKey.json` (Private Key / Admin SDK) kullanılarak bağlanılmaktadır.
- **Yetki Durumu:** Admin SDK, Firebase'deki en üst düzey (VIP) yetkiye sahiptir. Bu nedenle Firebase Güvenlik Kurallarını (Security Rules) ve tarih kısıtlamalarını **tamamen es geçer**. Test modu bitse dahi masaüstü uygulaması veritabanına sorunsuzca yazıp okumaya devam eder.
- **Kırmızı Çizgi:** `serviceAccountKey.json` dosyası bizim en gizli anahtarımızdır. Bu dosya **ASLA** GitHub'a açık olarak yüklenmemeli ve **KESİNLİKLE** mobil uygulamanın içine gömülmemelidir!

### 2. Mobil Uygulama (Client / İstemci) 📱

- **Bağlantı Yöntemi:** Mobil uygulama (Android/iOS) Private Key kullanmaz! Sadece standart Firebase Client SDK kütüphaneleri ile veritabanına bağlanır.
- **Mevcut Durum (Test Modu):** Mobil geliştirmenin hızlıca yapılabilmesi için Firebase Güvenlik Kurallarındaki tarih sınırı **01 Temmuz 2026**'ya kadar uzatılmıştır. Bu tarihe kadar mobil geliştirici, herhangi bir "Giriş Yap (Login)" modülü kodlamadan veritabanından veri okuyup yazabilir.

### ⚠️ 01 Temmuz 2026'dan Sonra Ne Olacak?

Belirtilen tarih dolduğunda Firebase, veritabanının kapılarını İstemcilere (Client) otomatik olarak kapatacaktır.

- Masaüstü uygulamamız (Private Key kullandığı için) çalışmaya devam edecektir.
- **Mobil uygulamamız ise veritabanından dışlanacak ve "Permission Denied" hatası vererek çökecektir.**

**🛠️ Çözüm (Mobil Geliştiricinin Yapması Gerekenler):**
Test süresi bitmeden önce (veya uygulama canlıya alınırken) mobil uygulamaya **Firebase Authentication (E-posta/Şifre ile Giriş)** entegre edilmelidir. Ardından Firebase Console üzerinden güvenlik kuralları aşağıdaki gibi güncellenerek "Sadece giriş yapan kullanıcılar veritabanına erişebilir" mantığına geçilmelidir:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null; // Sadece login olanlar erişebilir
    }
  }
}
```

<br>

## 🚨 TODO: İNTERNET BAĞLANTISI KONTROLÜ (OFFLINE YAKALAMA) 🚨

> **⚠️ GELİŞTİRİCİ NOTU:** Veritabanı mimarimiz doğrudan bulut (Firebase) tabanlı çalıştığı için, uygulamanın internetsiz ortamda çalıştırıldığı senaryolarda kilitlenmeleri ve çökmeleri engellemek adına acilen bir **"Bağlantı Kontrol Modülü"** eklenmelidir!

**Yapılacaklar:**

- Uygulama başlarken (özellikle _Login_ ve _Dashboard_ veri çekme aşamalarında) `socket` bağlantısı ile internet kontrolü yapılacak.
- Bağlantı yoksa arayüzde kullanıcıya belirgin bir hata mesajı çıkarılacak: _"FocuSync veritabanına bağlanılamıyor, lütfen internet bağlantınızı kontrol edin!"_
- **İleriki aşama:** Mümkünse verilerin yerel önbellekten (Local Cache) okunabilmesi için bir yapı kurulacak.

<div align="center">

_FocuSync — Odaklan, Geliş, Başar._

</div>
```
