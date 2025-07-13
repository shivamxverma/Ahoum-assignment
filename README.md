# 🧘 Booking System for Sessions & Retreats

## 🔧 Tech Stack

- **Frontend**: React, TailwindCSS  
- **Backend**: Flask API  
- **Database**: PostgreSQL, SQLAlchemy ORM  

---

## 📂 Folder Structure

```

.
├── client        -> frontend (React)
├── server        -> main backend (Flask API)
└── crm\_server    -> CRM notification server (Flask)

````

---

## 🔐 Security Practices Used

- Hashed password before storing  
- JWT token for verification  
- Protected all sensitive frontend routes  
- Bearer token for CRM server authentication  

---

## ✅ Functionality

### 👤 User
- `POST /api/register` → Register a new user  
- `POST /api/login` → Login with email or username  
- `GET  /api/login/google` → Login using Google OAuth  

---

### 📅 Events
- `GET  /api/events/` → Fetch all events  
- `POST /api/events/book` → Book a session/event  
- `POST /notify` → Notify the CRM server on booking  

---

## 🧠 Extra Notes
- Sessions are linked with facilitators  
- Bookings stored with user-session linkage  
- Notification sent to separate CRM Flask server  

---

## 🚀 Setup Instructions

### Backend
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
````

### CRM Server

```bash
cd crm_server
python crm_app.py
```

### Frontend

```bash
cd client
npm install
npm run dev
```

---

## ✍️ Author

Shivam Verma 🚀


