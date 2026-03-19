# 📚 FastAPI Library Book Management System
---
A robust Backend API built with FastAPI to manage library inventory, member borrowings, and automated waitlists. This project demonstrates advanced RESTful API concepts including complex data filtering, custom sorting, and manual pagination.
---

## 🚀 Project Overview

This API allows efficient handling of library operations such as:
- Managing books (add, update, delete)
- Borrowing and returning books
- Handling waitlists for unavailable books
- Searching, filtering, and sorting data

---

## ✨ Key Features

- RESTful API development with FastAPI  
- Data validation using Pydantic  
- Full CRUD operations  
- Borrowing system with due-date logic  
- Automated waitlist (queue) system  
- Search, filtering, and sorting functionality  
- Interactive API testing with Swagger UI  

---

## 📌 API Endpoints

### 📖 Book Management
- GET /books – Retrieve all books  
- POST /books – Add a new book  
- GET /books/{book_id} – Get book by ID  
- PUT /books/{book_id} – Update book  
- DELETE /books/{book_id} – Delete book  

### 📊 Insights & Utilities
- GET /books/summary – Library statistics  
- GET /books/filter – Filter books  
- GET /books/search – Search books  
- GET /books/sort – Sort books  

### 🔄 Borrowing System
- POST /borrow – Borrow a book  
- GET /borrow-records – View borrow records  

### ⏳ Queue Management
- POST /queue/add – Add to waitlist  
- GET /queue – View waitlist  
- POST /return/{book_id} – Return book
  

---

📁 Project Structure
library-management-system/
│
├── app/
│   ├── main.py                # Entry point (FastAPI app)
│   ├── models.py              # Pydantic models
│   ├── routes/
│   │   ├── books.py           # Book-related endpoints
│   │   ├── borrow.py          # Borrowing logic
│   │   ├── queue.py           # Waitlist management
│   │
│   ├── services/
│   │   ├── book_service.py    # Business logic for books
│   │   ├── borrow_service.py  # Borrow logic
│   │   ├── queue_service.py   # Queue logic
│   │
│   ├── utils/
│   │   ├── helpers.py         # Helper functions
│
│   └── data/
│       ├── db.py              # In-memory data (books, records)
│
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Ignore unnecessary files


## 🛠️ Tech Stack

- Language: Python 3.9+  
- Framework: FastAPI  
- Validation: Pydantic  
- Server: Uvicorn  

---

## ⚙️ Installation & Setup

### 1. Install Dependencies
```bash
pip install fastapi uvicorn
```

### 2. Run the Server
```bash
uvicorn main:app --reload
```

### 3. Open API Docs
Go to:
```
http://127.0.0.1:8000/docs
```

---

## 📌 Project Highlights

- Clean and modular code structure  
- Real-world backend implementation  
- Efficient handling of edge cases  
- Follows REST API best practices  

---

## 👨‍💻 Author

Developed as part of backend development practice using FastAPI & My internship project under Innomatics Research Labs
