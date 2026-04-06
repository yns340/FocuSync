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
  "allowed_apps": ["string"]
  "daily_study_goal": "number",
  "email": "string",
  "name": "string",
  "password": "string",
  "role": "string"
  "school": "string"
  "surname": "string"
}
```

---

### 📚 Courses

| Alan               | Tip       | Açıklama            |
| ------------------ | --------- | ------------------- |
| `course_name`      | string    | Ders adı            |
| `difficulty_level` | number    | Zorluk seviyesi     |
| `exam_date`        | timestamp | Sınav tarihi        |
| **`user_id`**      | string    | Kullanıcı referansı |
| `weekly_hours`     | number    | Haftalık ders saati |

```json
{
  "course_name": "string",
  "difficulty_level": "string",
  "exam_date": "timestamp",
  "user_id": "string"
  "weekly_hours": "number",     // Örn: 4 (Okuldaki ders sıklığı/kredisi)
}
```

---

### 📅 Schedules

| Alan             | Tip       | Açıklama                   |
| ---------------- | --------- | -------------------------- |
| `schedule_name`  | string    | Program dönem adı          |
| `updated_at`     | timestamp | Programın yüklenme tarihi  |
| **`user_id`**    | string    | Kullanıcı referansı        |
| `weekly_routine` | object    | Günlere göre ders programı |

#### `weekly_routine[gun][]` — Dizi Elemanı

| Alan            | Tip    | Açıklama        |
| --------------- | ------ | --------------- |
| **`course_id`** | string | Ders referansı  |
| `course_name`   | string | Ders adı.       |
| `start_time`    | string | Başlangıç saati |
| `end_time`      | string | Bitiş saati     |
| `type`          | string | Etkinlik türü   |

```json
{
  "schedule_name": "string",
  "updated_at": "timestamp",
  "user_id": "string"
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
    "Salı": [
      {
        "course_id": "string",
        "course_name": "string",
        "start_time": "string",
        "end_time": "string",
        "type": "string"
      }
    ],
    "Çarşamba": [
      {
        "course_id": "string",
        "course_name": "string",
        "start_time": "string",
        "end_time": "string",
        "type": "string"
      }
    ],
    "Perşembe": [
      {
        "course_id": "string",
        "course_name": "string",
        "start_time": "string",
        "end_time": "string",
        "type": "string"
      }
    ],
    "Cuma": [
      {
        "course_id": "string",
        "course_name": "string",
        "start_time": "string",
        "end_time": "string",
        "type": "string"
      }
    ],
    "Cumartesi": [],
    "Pazar": []
  }
}
```

---

### 🧠 StudyPlans

| Alan              | Tip       | Açıklama                        |
| ----------------- | --------- | ------------------------------- |
| `plan_start_date` | timestamp | Planın başlangıç tarihi         |
| **`user_id`**     | string    | Kullanıcı referansı             |
| `weekly_sessions` | object    | Günlere göre çalışma oturumları |

#### `weekly_sessions[gun][]` — Dizi Elemanı

| Alan               | Tip     | Açıklama                       |
| ------------------ | ------- | ------------------------------ |
| **`session_id`**   | string  | Oturum ID (örn: `session1`, …) |
| **`course_id`**    | string  | Ders referansı                 |
| `course_name`      | string  | Ders adı.                      |
| `planned_duration` | number  | Planlanan süre (dakika)        |
| `is_completed`     | boolean | Tamamlandı mı?                 |

```json
{
  "plan_start_date": "timestamp",
  "user_id": "string"
  "weekly_sessions": {
    "Pazartesi": [
      {
        "session_id": "string", //Firebase dizide id üretmez o yüzden kendimiz session1 olarak başlatırız...
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Salı": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Çarşamba": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Perşembe": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Cuma": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Cumartesi": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ],
    "Pazar": [
      {
        "session_id": "string",
        "course_id": "string",
        "course_name": "string",
        "planned_duration": "number",
        "is_completed": "boolean"
      }
    ]
  }
}
```

---

### 🎯 FocusSessions

| Alan                        | Tip       | Açıklama                         |
| --------------------------- | --------- | -------------------------------- |
| **`study_plan_session_id`** | string    | StudyPlan `session_id` referansı |
| **`course_id`**             | string    | Ders referansı                   |
| `actual_focus_time`         | number    | Gerçek odak süresi (dakika)      |
| `focus_score`               | number    | Odak skoru                       |
| `status`                    | string    | Durum                            |
| `timestamp`                 | timestamp | Oturum zamanı                    |
| **`user_id`**               | string    | Kullanıcı referansı              |

```json
{
  "study_plan_session_id": "string", (weekly_sessions id lerine atanmalı)
  "course_id": "string",
  "actual_focus_time": "number",
  "focus_score": "number",
  "status": "string",
  "timestamp": "timestamp",
  "user_id": "string"
}
```

---

### 🚫 Violations

| Alan                   | Tip       | Açıklama                     |
| ---------------------- | --------- | ---------------------------- |
| **`focus_session_id`** | string    | FocusSession referansı       |
| `app_name`             | string    | İhlal eden uygulama adı      |
| `duration`             | number    | İhlal süresi (saniye/dakika) |
| `timestamp`            | timestamp | İhlal zamanı                 |
| **`user_id`**          | string    | Kullanıcı referansı          |

```json
{
  "focus_session_id": "string",
  "app_name": "string",
  "duration": "number",
  "timestamp": "timestamp",
  "user_id": "string"
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

<div align="center">

_FocuSync — Odaklan, Geliş, Başar._

</div>
