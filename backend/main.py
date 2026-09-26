from contextlib import closing
import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "todos.db"

app = FastAPI(title="Todo List API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with closing(get_connection()) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        count = connection.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
        if count == 0:
            connection.executemany(
                """
                INSERT INTO todos (title, description, completed)
                VALUES (?, ?, ?)
                """,
                [
                    ("Complete HTML structure", "Review the required page structure and elements.", 1),
                    ("Style the frontend", "Create a clean responsive layout using CSS.", 1),
                    ("Build the FastAPI backend", "Create the API and Pydantic Todo model.", 0),
                    ("Connect SQLite database", "Store and retrieve todo records from SQLite.", 0),
                    ("Test the integrated application", "Confirm that the browser loads all tasks from the API.", 0),
                ],
            )

        connection.commit()


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {"message": "Todo API is running"}


@app.get("/todos", response_model=list[Todo])
def get_todos():
    with closing(get_connection()) as connection:
        rows = connection.execute("SELECT * FROM todos").fetchall()
    return [Todo(**dict(row)) for row in rows]
