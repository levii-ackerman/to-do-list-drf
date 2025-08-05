# ✅ Taskify — Django DRF asosidagi To-Do & Group Task Management System

**Taskify** — bu Django REST Framework asosida yaratilgan kuchli va zamonaviy to-do ilovasi bo‘lib, foydalanuvchilarga shaxsiy va guruh tasklarini boshqarish, 
do‘stlar bilan aloqada bo‘lish, eslatmalar olish va tasklarga tag qo‘shish imkonini beradi.

---

## ✨ Asosiy imkoniyatlar

- 👤 Foydalanuvchi ro‘yxatdan o‘tishi va tizimga kirishi (`JWT` autentifikatsiya orqali)
- ✅ Oddiy (shaxsiy) tasklar yaratish, o‘chirish, tahrirlash
- 👥 Guruhlar yaratish, foydalanuvchilarni qo‘shish
- 📋 Guruh tasklarini yaratish va a'zolarga biriktirish
- 🏷 Tasklarga `#tag` belgilari qo‘shish
- 🔔 Deadline oldidan avtomatik eslatmalar yuborish
- 🤝 Do‘stlik tizimi va so‘rovlar yuborish
- 🕒 Task o‘zgarishlari tarixini yuritish (`TaskLog`)

---

## 🧱 Texnologiyalar

| Texnologiya  | Tavsif |
|--------------|--------|
| **Django**   | Backend web-framework |
| **Django REST Framework (DRF)** | RESTful API yaratish |
| **SimpleJWT** | JWT asosida autentifikatsiya |
| **SQLite** yoki **PostgreSQL** | Ma’lumotlar bazasi |
| **Python 3.13** | Loyiha Python versiyasi |

---


---

## 📦 O‘rnatish (bosqichma-bosqich)

### 1. Reponi klon qiling
```bash
git clone https://github.com/username/taskify-drf.git
cd taskify-drf


python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

Agarda Pipfile bo'lsa
pip install pipenv
pipenv install

#Kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt

#Migratsiyani ishga tushirish
python manage.py migrate

| Model                   | Tavsifi                                                   |
| ----------------------- | --------------------------------------------------------- |
| **User**                | Foydalanuvchi modeli (`AbstractUser` yoki default `User`) |
| **Task**                | Shaxsiy tasklar (foydalanuvchiga biriktirilgan)           |
| **TaskLog**             | Task tarixini saqlovchi model                             |
| **FriendRequest**       | Do‘stlik so‘rovlari modeli                                |
| **Friendship**          | Qabul qilingan do‘stlar                                   |
| **Group**               | Guruhlar: “Oila”, “Jamoa”, “Do‘stlar”                     |
| **GroupMember**         | Guruhdagi a’zolar                                         |
| **GroupTask**           | Guruhga oid tasklar                                       |
| **GroupTaskAssignment** | GroupTask’ga biriktirilgan foydalanuvchilar               |
| **Tag**                 | Tasklarga belgilovchi `#tag` lar                          |
| **Notification**        | Deadline eslatmalari uchun model                          |

✅ Rejalashtirilgan funksiyalar
 WebSocket orqali real-time xabarlar
 Oldingi task versiyalarini ko‘rish
 Frontend interfeys (Next.js yoki React)
 Mobil ilova (Flutter / React Native)

📩 Muallif
Agar sizda savollar, takliflar yoki muammolar bo‘lsa — bemalol murojaat qiling:
Email: leviackermanw71@gmail.com
