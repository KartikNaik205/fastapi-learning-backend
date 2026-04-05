# 🧠 AI Notes App

A full-stack notes application with AI-powered summarization.

---

## 🚀 Features

* 📝 Create, edit, delete notes
* 🤖 AI-powered note summarization (Gemini API)
* ⚡ Caching system for faster repeated summaries
* 🌐 Full-stack architecture (FastAPI + React)

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite

### Frontend

* React (Vite)
* Tailwind CSS

### AI Integration

* Google Gemini API

---

## 📂 Project Structure

```
backend/
  app/
    models/
    routes/
    database.py
  main.py

frontend/
  vite-project/
    src/
      App.jsx
```

---

## ⚙️ Setup Instructions

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 2. Frontend

```bash
cd frontend/vite-project
npm install
npm run dev
```

---

## 🌍 Access

* Frontend: http://localhost:5173
* Backend: http://localhost:8000

---

## 📌 Notes

* CORS enabled for frontend-backend communication
* Summaries are cached after first request for performance

---

## 📈 Future Improvements

* User authentication
* Better UI/UX
* Deployment (Docker / Cloud)
* Component-based React architecture

---

## 👨‍💻 Author

Kartik Naik
