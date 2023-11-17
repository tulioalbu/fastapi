from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="ID is not needed")
    title: str = Field(min_length=3, max_length=100, description="Title must be between 3 and 100 characters")
    author: str = Field(min_length=1, max_length=100, description="Author must be between 1 and 100 characters")
    description: str = Field(min_length=10, max_length=300, description="Description must be between 10 and 300 "
                                                                        "characters")
    rating: int = Field(gt=0, lt=6, description="Rating must be between 1 and 5")
    publish_date: int = Field(gt=1900, lt=2023, description="Publish date must be between 1900 and 2023")

    class Config:
        schema_extra = {
            "example": {
                "title": "Game of Thrones",
                "author": "George R. R. Martin",
                "description": "Game of Thrones is the first novel in A Song of Ice and Fire, a series of fantasy ",
                "rating": 5,
                "publish_date": "1996"
            }
        }


BOOKS = [
    Book(1, "The Hobbit", "J. R. R. Tolkien", "The Hobbit is a children's fantasy novel by English author J. R. R. "
                                              "Tolkien. It was published on 21 September 1937 to wide critical "
                                              "acclaim, being nominated for the Carnegie Medal and awarded a prize "
                                              "from the New York Herald Tribune for best juvenile fiction.", 4, 1937),
    Book(2, "The Lord of the Rings", "J. R. R. Tolkien", "The Lord of the Rings is an epic high fantasy novel by the "
                                                         "English author and scholar J. R. R. Tolkien. Set in "
                                                         "Middle-earth, the world at some distant time in the past, "
                                                         "the story began as a sequel to Tolkien's 1937 children's "
                                                         "book The Hobbit, but eventually developed into a much "
                                                         "larger work.", 5, 1954),
    Book(3, "The Silmarillion", "J. R. R. Tolkien", "The Silmarillion is a collection of mythopoeic works by English "
                                                    "writer J. R. R. Tolkien, edited and published posthumously by "
                                                    "his son, Christopher Tolkien, in 1977, with assistance from Guy "
                                                    "Gavriel Kay.", 4, 1977),
    Book(4, "The Children of Húrin", "J. R. R. Tolkien", "The Children of Húrin is an epic fantasy novel which forms "
                                                         "the completion of a tale by J. R. R. Tolkien. He wrote the "
                                                         "original version of the story in the late 1910s, "
                                                         "revised it several times later, but did not complete it "
                                                         "before his death in 1973.", 3, 2007),
    Book(5, "The Fall of Gondolin", "J. R. R. Tolkien", "The Fall of Gondolin is, in the writings of J.R.R. Tolkien, "
                                                        "one of the original Lost Tales which formed the basis for a "
                                                        "section in his later work, The Silmarillion. A stand-alone, "
                                                        "book-length version of the story was published on 30 August "
                                                        "2018.", 4, 2018),
    Book(6, "The Book of Lost Tales", "J. R. R. Tolkien", "The Book of Lost Tales is a collection of early stories by "
                                                          "English writer J. R. R. Tolkien, published as the first "
                                                          "two volumes of Christopher Tolkien's 12-volume series The "
                                                          "History of Middle-earth, in which he presents and analyzes "
                                                          "the manuscripts of those stories, which were the earliest "
                                                          "form of the complex fictional myths that would eventually "
                                                          "comprise The Silmarillion.", 3, 1983),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books")
async def read_book_by_rating(rating: int):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            books_by_rating.append(book)
    return books_by_rating


@app.get("/books/publish/")
async def read_book_by_publish_date(publish_date: int):
    books_by_publish_date = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_by_publish_date.append(book)
    return books_by_publish_date


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.put("/books/update_book")
async def update_book(book: Book):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return BOOKS[i]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return BOOKS[i]
