from fastapi import FastAPI, Query, HTTPException, Path
from pydantic import BaseModel, Field

app = FastAPI(title="Library Management System")

# Books Data 
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "is_available": True},
    {"id": 2, "title": "A Brief History of Time", "author": "Stephen Hawking", "genre": "Science", "is_available": True},
    {"id": 3, "title": "Sapiens", "author": "Yuval Noah Harari", "genre": "History", "is_available": False},
    {"id": 4, "title": "Clean Code", "author": "Robert C. Martin", "genre": "Tech", "is_available": True},
    {"id": 5, "title": "The Silent Patient", "author": "Alex Michaelides", "genre": "Fiction", "is_available": True},
    {"id": 6, "title": "Python Crash Course", "author": "Eric Matthes", "genre": "Tech", "is_available": False},
]

borrow_records = []
record_counter = 1
waiting_list_queue = []

# Pydantic Model for Borrow Request
class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    borrow_days: int = Field(..., gt=0, le=60)
    member_id: str = Field(..., min_length=4)
    member_type: str = "regular"

# Pydantic Model for adding new book
class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = True

# Helper Functions 
# Function to find book using id
def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None
# Function to find the Due Date
def calculate_due_date(borrow_days: int, member_type: str):
    if member_type.lower() == "premium":
        actual_days_by_the_user = min(borrow_days, 60)
    else:
        actual_days_by_the_user = min(borrow_days, 30)
    return f"Return by: Day {actual_days_by_the_user}"
# Function to filter the books
def filter_books_logic(all_books, genre: str = None, author: str = None, is_available: bool = None):
    filtered = all_books
    if genre is not None:
        filtered = [b for b in filtered if b["genre"].lower() == genre.lower()]
    if author is not None:
        filtered = [b for b in filtered if author.lower() in b["author"].lower()]
    if is_available is not None:
        filtered = [b for b in filtered if b["is_available"] == is_available]
    return filtered
# Function to find is a member is in Queue
def is_already_in_queue(member_name, book_id):
    for entry in waiting_list_queue:
        if entry["member_name"] == member_name and entry["book_id"] == book_id:
            return True
    return False

# --- ROUTES ---
# Endpoint for Home
@app.get("/")
def home():
    return {'message': 'Welcome to City Public Library'}
# Endpoint for Getting the books
@app.get("/books")
def get_books():
    total_count = len(books)
    available_count = len([book for book in books if book["is_available"] == True])
    return {
        "books": books,
        "total": total_count,
        "available_count": available_count
    }
# Endpoint to Post Books
@app.post("/books", status_code=201)
def adding_book(book_request: NewBook):
    for existing_book in books:
        if existing_book["title"].lower() == book_request.title.lower():
            return {"error": f"A book with the title {book_request.title} already exsists"}
    new_id = len(books) + 1
    added_book = {
        "id": new_id,
        "title": book_request.title,
        "author": book_request.author,
        "genre": book_request.genre,
        "is_available": book_request.is_available
    }
    books.append(added_book)
    return {"message": f"A new book {book_request.title} is successfully added"}
# Endpoint To Get Summary
@app.get("/books/summary")
def get_books_summary():
    total_books = len(books)
    available_count = len([b for b in books if b["is_available"]])
    borrowed_count = total_books - available_count
    genre_breakdown_into_dict = {}
    for b in books:
        genre = b["genre"]
        genre_breakdown_into_dict[genre] = genre_breakdown_into_dict.get(genre, 0) + 1
    return {
        "total_books": total_books,
        "available_count": available_count,
        "borrowed_count": borrowed_count,
        "genre_breakdown": genre_breakdown_into_dict
    }

# Static Routes
# Endpoint to sort the books
@app.get("/books/sort")
def sort_books(
    sort_by: str = Query("title"), 
    order: str = Query("asc")
):
    
    allowed_sort_fields = ["title", "author", "genre"]
    allowed_orders = ["asc", "desc"]

    if sort_by.lower() not in allowed_sort_fields:
        return {
            "error": f"Invalid sort_by value: '{sort_by}'. Allowed values are: {', '.join(allowed_sort_fields)}"
        }
    
    if order.lower() not in allowed_orders:
        return {
            "error": f"Invalid order value: '{order}'. Allowed values are: 'asc' or 'desc'"
        }

    is_reverse = True if order.lower() == "desc" else False
    
    sorted_list = sorted(
        books, 
        key=lambda x: x[sort_by.lower()].lower(), 
        reverse=is_reverse
    )

    return {
        "status": "Success",
        "metadata": {
            "sorted_by": sort_by.lower(),
            "order": order.lower(),
            "total_count": len(sorted_list)
        },
        "results": sorted_list
    }
# Endpoint to filter books
@app.get("/books/filter")
def filter_books(genre: str = Query(None), author: str = Query(None), is_available: bool = Query(None)):
    results = filter_books_logic(books, genre, author, is_available)
    return {"count": len(results), "results": results}
# Endpoint to search books
@app.get("/books/search")
def searching_book(keyword: str = Query(..., min_length=1)):
    search_book = keyword.lower()
    search_result = [book for book in books if search_book in book["title"].lower() or search_book in book["author"].lower()]
    if not search_result:
        return {"status": "No Match", "message": f"No results for '{keyword}'"}
    return {"total_found": len(search_result), "results": search_result}
# Endpoint to Page
@app.get("/books/page")
def get_paginated_books(
    page: int = Query(1, gt=0), 
    limit: int = Query(3, gt=0)
):
    #  Calculating the start and end index for slicing
    start_index = (page - 1) * limit
    end_index = start_index + limit
    
    sliced_books = books[start_index:end_index]
    
    total_books = len(books)
    
    total_pages = total_books // limit
    if total_books % limit > 0:
        total_pages += 1
    
    return {
        "total": total_books,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "books": sliced_books
    }

# Endpoint to Search Borrow Records by Member Name
@app.get("/borrow-records/search")
def search_borrow_records(member_name: str = Query(..., min_length=2)):
    search_name = member_name.lower()
    
    results = [
        r for r in borrow_records 
        if search_name in r["member_name"].lower()
    ]
    
    if not results:
        return {"message": f"No borrow records found for '{member_name}'"}
        
    return {
        "search_term": member_name,
        "total_found": len(results),
        "results": results
    }

#  Endpoint to Paginate Borrow Records
@app.get("/borrow-records/page")
def paginate_borrow_records(
    page: int = Query(1, gt=0), 
    limit: int = Query(2, gt=0)
):
    start = (page - 1) * limit
    end = start + limit
    
    sliced_records = borrow_records[start:end]
    
    total_records = len(borrow_records)
    total_pages = total_records // limit
    if total_records % limit > 0:
        total_pages += 1
        
    return {
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "records": sliced_records
    }

# Endpoint to Browse the books combining keyword,sort,order,page,limit
@app.get("/books/browse")
def browse_books(
    keyword: str = Query(None),
    sort_by: str = Query("title"),
    order: str = Query("asc"),
    page: int = Query(1, gt=0),
    limit: int = Query(2, gt=0)
):
    # FILTERING
    if keyword:
        search_keyword = keyword.lower()
        filtered_list = [
            b for b in books 
            if search_keyword in b["title"].lower() or search_keyword in b["author"].lower()
        ]
    else:
        filtered_list = books.copy()

    # SORTING
    allowed_sort_fields = ["title", "author", "genre"]
    field = sort_by.lower() if sort_by.lower() in allowed_sort_fields else "title"
    is_reverse = True if order.lower() == "desc" else False
    
    # Sort the filtered results
    sorted_list = sorted(filtered_list, key=lambda x: x[field].lower(), reverse=is_reverse)

    #  PAGINATION
    total_found = len(sorted_list)
    start = (page - 1) * limit
    end = start + limit
    paginated_results = sorted_list[start:end]

    # Calculate Total Page
    total_pages = total_found // limit
    if total_found % limit > 0:
        total_pages += 1
    # Output for the Get Browse
    return {
        "status": "Success",
        "search_metadata": {
            "keyword_used": keyword,
            "sort_by": field,
            "order": order.lower()
        },
        "pagination_metadata": {
            "total_found": total_found,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit
        },
        "results": paginated_results
    }

# Dynamic Routes
# Endpoint to Get Book by id
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int = Path(..., gt=0)):
    book = find_book(book_id)
    if book:
        return book
    return {"error": "Book not found"}
# Endpoint to Put books
@app.put("/books/{book_id}")
def update_book(book_id: int = Path(..., gt=0), genre: str = Query(None), is_available: bool = Query(None)):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Not found")
    if genre is not None:
        book["genre"] = genre
    if is_available is not None:
        book["is_available"] = is_available
    return {"updated_book": book}

# Endpoint to delete a book from the library
@app.delete("/books/{book_id}")
def delete_book_by_id(book_id: int = Path(..., gt=0)):
    choosed_book_to_delete = find_book(book_id)
    if not choosed_book_to_delete:
        raise HTTPException(status_code=404, detail="Not found")
    deleted_title = choosed_book_to_delete["title"]
    books.remove(choosed_book_to_delete)
    return {"message": f"Book {deleted_title} removed", "deleted_id": book_id}

# --- BORROWING & QUEUE ---
# Endpoint to Post Borrow
@app.post("/borrow")
def borrow_book(request: BorrowRequest):
    global record_counter
    book = find_book(request.book_id)
    if not book:
        return {"error": "Book not found"}
    if not book["is_available"]:
        return {"error": "Book is already borrowed"}
    if request.member_type.lower() == "regular" and request.borrow_days > 30:
        return {"error": "Regular members max 30 days."}
    due_info = calculate_due_date(request.borrow_days, request.member_type)
    book["is_available"] = False
    new_record = {"record_id": record_counter, "member_name": request.member_name, "due_date": due_info}
    borrow_records.append(new_record)
    record_counter += 1
    return new_record
# Endpoint to get Borrow Records
@app.get("/borrow-records")
def get_borrow_records():
    return {"records": borrow_records}
# Endpoint to Post or add queue
@app.post("/queue/add")
def add_to_waitlist(member_name: str, book_id: int):
    book = find_book(book_id)
    if not book or book["is_available"]:
        return {"error": "Invalid request"}
    waitlist_entry = {"member_name": member_name, "book_id": book_id}
    waiting_list_queue.append(waitlist_entry)
    return {"message": "Added to queue"}
# Endpoint Get Queue
@app.get("/queue")
def view_waitlist():
    return {"waitlist": waiting_list_queue}
# Endpoint to return the book
@app.post("/return/{book_id}")
def return_book_and_check_queue(book_id: int):
    global record_counter
    
    book = find_book(book_id)
    if not book:
        return {"error": "Book not found"}
    
    if book["is_available"]:
        return {"message": "Book is already in the library"}

    book["is_available"] = True

    queue_match_index = -1
    for index, entry in enumerate(waiting_list_queue):
        if entry["book_id"] == book_id:
            queue_match_index = index
            break

    # Re-assigning or Leave on Shelf
    if queue_match_index != -1:

        next_person = waiting_list_queue.pop(queue_match_index)
        
        due_info = calculate_due_date(7, "regular")
        
        new_record = {
            "record_id": record_counter,
            "member_name": next_person["member_name"],
            "due_date": due_info,
            "member_type": "regular",
            "book_title": book["title"]
        }
        
        borrow_records.append(new_record)
        record_counter += 1
        book["is_available"] = False 
        
        return {
            "status": "returned and re-assigned",
            "message": f"Book '{book['title']}' was returned and immediately issued to {next_person['member_name']} from the waitlist.",
            "new_record": new_record
        }
    
    return {
        "status": "returned and available",
        "message": f"Book '{book['title']}' is now back on the shelf."
    }