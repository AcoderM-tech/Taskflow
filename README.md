# ✅ TaskFlow — Vazifalarni Boshqarish Tizimi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Vazifalaringizni rejalashtiring, kuzating va o'z vaqtida bajaring.**

</div>

---

## 📋 Mundarija

- [Loyiha haqida](#-loyiha-haqida)
- [Asosiy imkoniyatlar](#-asosiy-imkoniyatlar)
- [Texnologiyalar](#-texnologiyalar)
- [O'rnatish](#-ornatish)
- [Muhit o'zgaruvchilari](#-muhit-ozgaruvchilari)
- [Ishga tushirish](#-ishga-tushirish)
- [Loyiha tuzilmasi](#-loyiha-tuzilmasi)
- [Litsenziya](#-litsenziya)

---

## 🎯 Loyiha haqida

**TaskFlow** — foydalanuvchilar o'z vazifalarini yaratishi, muddatlarini belgilashi va bajarilish holatini kuzatishi mumkin bo'lgan Django asosidagi veb-ilova. Har bir foydalanuvchi faqat o'z vazifalarini ko'radi. Kechikkan, bugungi va kelajakdagi vazifalar alohida ko'rsatiladi.

---

## ✨ Asosiy imkoniyatlar

### 📝 Vazifalar
- Sarlavha, matn va muddat (deadline) bilan vazifa qo'shish
- Vazifani bajarildi deb belgilash
- Vazifani tahrirlash va o'chirish
- Sarlavha yoki matn bo'yicha qidiruv
- Sana bo'yicha filtrlash

### 📊 Dashboard
- Jami, bajarilgan, faol va kechikkan vazifalar soni
- Bajarilish foizi
- Bugungi, kelajakdagi va kechikkan vazifalar bo'limlari
- Arxiv (bajarilgan vazifalar tarixi)

### 👤 Foydalanuvchi profili
- Ro'yxatdan o'tish (ism, familiya, email, telefon, manzil, tug'ilgan sana)
- Profil rasmi yuklash
- Profilni tahrirlash
- Parol almashtirish (validatsiya bilan)
- Profil to'liqlik foizi

### 🔒 Xavfsizlik
- Maxsus parol validatori (harf + raqam majburiy)
- 15 daqiqa nofaollikda avtomatik chiqish
- Login talab qilinadigan sahifalar himoyasi
- CSRF muhofazasi

---

## 🛠 Texnologiyalar

| Qatlam | Texnologiya |
|--------|-------------|
| Backend | Django 5.2 |
| Ma'lumotlar bazasi | SQLite |
| Autentifikatsiya | Django Auth (CustomUser) |
| Rasm ishlash | Pillow |

---

## ⚙️ O'rnatish

### Talablar

- Python 3.11+
- pip

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/AcoderM/Taskflow.git
cd Taskflow
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash

```bash
cp .env.example .env
```

`.env` faylini tahrirlang va `SECRET_KEY` ni to'ldiring.

### 5. Ma'lumotlar bazasini tayyorlash

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔧 Muhit o'zgaruvchilari

`.env.example` dan nusxa oling:

```env
# Majburiy
SECRET_KEY=your-very-strong-secret-key

DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🚀 Ishga tushirish

```bash
python manage.py runserver
```

Brauzerda oching: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Loyiha tuzilmasi

```
Taskflow/
├── config/                 # Django konfiguratsiyasi
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mainapp/                # Asosiy ilova
│   ├── models.py           # CustomUser, Post
│   ├── views.py            # Barcha view funksiyalar
│   ├── validators.py       # Maxsus parol validatori
│   └── admin.py
├── templates/              # HTML shablonlar
│   ├── base.html           # Dashboard
│   ├── landing.html        # Asosiy sahifa
│   ├── login.html
│   └── signup.html
├── static/                 # CSS, JS, rasmlar
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 📄 Litsenziya

Bu loyiha **MIT litsenziyasi** asosida tarqatiladi. Batafsil ma'lumot uchun [LICENSE](LICENSE) fayliga qarang.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/AcoderM-tech">AcoderM</a>
</div>
