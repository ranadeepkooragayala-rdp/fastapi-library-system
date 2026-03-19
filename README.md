# 📚 FastAPI Library Book Management System
---
A scalable and well-structured backend API built using FastAPI for managing a library’s book inventory, borrowing system, and waitlist queue. This project demonstrates real-world backend development practices, including RESTful API design, request validation, and multi-step workflows.

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
Project Structure
```
library-management-system/
│
├── main.py
├── requirements.txt
├── README.md
│
├── screenshots/
│   ├── Q1_home_route.png
│   ├── Q2_get_all_books.png
│   ├── Q3_get_book_by_id.png
│   └── Q20_browse_endpoint.png

```
---
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
