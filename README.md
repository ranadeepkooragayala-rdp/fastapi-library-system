FastAPI Library Book Management System

A robust Backend API built with FastAPI to manage library inventory, member borrowings, and automated waitlists. This project demonstrates advanced RESTful API concepts including complex data filtering, custom sorting, and manual pagination.

Key Features of the project:
• REST APIs with FastAPI
• Pydantic data validation
• CRUD operations
• Multi-step workflows
• Search, sorting, and pagination
• API testing using Swagger UI

The Endpoints the API has are:
/Books
/books/{book_id}
/borrow-records
/books/summary
/borrow
/books/filter
/books/{book_id}
/queue/add
/return/{book_id}
/books/search
/borrow-records/search
/books/browse

Technical Stack
Language: Python 3.9+
Framework: FastAPI
Validation: Pydantic Models
Web Server: Uvicorn

How to Run
1. Install Dependencies:
pip install fastapi uvicorn

2.Start the Server:
uvicorn main:app --reload

3.Access Documentation:
Open your browser and navigate to http://127.0.0.1:8000/docs to interact with the Swagger UI.



