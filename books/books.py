from fastapi import FastAPI

app = FastAPI()


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")  # path parameter
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title:
            return book


@app.get("/books")  # query parameter
async def read_all_books(category: str):
    books_in_category = []
    for book in BOOKS:
        if book.get('category').casefold() == category:
            books_in_category.append(book)
    return books_in_category


@app.get("/books/{author>")  # path and query parameter
async def read_all_books(category: str, author: str):
    books_in_category = []
    for book in BOOKS:
        if book.get('category').casefold() == category and book.get('author').casefold() == author:
            books_in_category.append(book)
    return books_in_category


BOOKS = [
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'fiction'},
    {'title': 'The Trial', 'author': 'Franz Kafka', 'category': 'fiction'},
    {'title': 'The Stranger', 'author': 'Albert Camus', 'category': 'fiction'},
    {'title': 'The Little Prince', 'author': 'Antoine de Saint-Exupéry', 'category': 'fiction'},
    {'title': 'The Brothers Karamazov', 'author': 'Fyodor Dostoevsky', 'category': 'fiction'},
    {'title': 'The Master and Margarita', 'author': 'Mikhail Bulgakov', 'category': 'fiction'},
]
