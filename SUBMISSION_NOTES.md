# Submission Notes

## 1. HTML elements identified from the reference image

The frontend was organized around the major interface elements required by the brief: a header area, profile placeholder and name, the “My Todo List” heading, a main task area, and individual todo cards. Each todo card contains a title, description, and visible completion state.

The structure is intentionally simple so the CSS can control the visual presentation while JavaScript supplies the task data.

## 2. Frontend challenges and investigation

One important requirement was to create the page without CSS first and then style it. The HTML therefore contains the semantic structure and an empty `todo-list` container. The final JavaScript creates the task elements dynamically.

Another issue to consider is displaying data safely. The implementation uses `textContent` rather than inserting todo values directly into `innerHTML`. This keeps task text separate from HTML markup.

## 3. Backend challenges and investigation

The backend needs to create the SQLite table when the application starts and must still work when the database already exists. `CREATE TABLE IF NOT EXISTS` handles the table initialization.

The application also needs at least five records. The startup initialization checks the number of existing records and inserts the supplied sample records only when the table is empty. This prevents duplicate sample records every time the server restarts.

## 4. How the problems were fixed

The SQLite connection uses `sqlite3.Row` as the row factory. This allows database columns to be accessed by name and converted into dictionaries.

The `/todos` endpoint selects all rows, converts each row into the Pydantic `Todo` model, and returns the list. The connection is closed after the query.

CORS middleware is enabled because the frontend and backend may run from different local origins. This allows browser requests from the frontend to reach FastAPI during development.

## 5. Data flow: SQLite → FastAPI → browser

1. SQLite stores the todo records in `todos.db`.
2. FastAPI starts and calls `initialize_database()`.
3. The browser loads `index.html` and then runs `script.js`.
4. JavaScript sends a GET request to `http://127.0.0.1:8000/todos`.
5. FastAPI executes `SELECT * FROM todos`.
6. Each SQLite row is converted into a Pydantic `Todo`.
7. FastAPI serializes the todo list as JSON.
8. JavaScript receives the JSON response.
9. `renderTodos()` creates the HTML elements for every todo.
10. Completed tasks receive the `completed` CSS class and show “Completed”; other tasks show “Incomplete”.

## Core code concepts to explain during review

### Pydantic model

`Todo` defines the expected shape and data types:

- `id`: integer
- `title`: string
- `description`: string
- `completed`: Boolean

### SQLite query

The main query is:

```sql
SELECT * FROM todos
```

It retrieves all todo records. The database stores Boolean-like completion values as integers: `0` for incomplete and `1` for completed.

### `/todos` endpoint

`GET /todos` opens the database, retrieves all rows, converts them to Pydantic objects, and returns JSON.

### JavaScript rendering

The frontend loops through the returned array. For every todo it creates an article, heading, status badge, and description, then appends the completed task card to `#todo-list`.

## Optional bonus questions

### 1. When a POST request is sent, is the item automatically stored in the database?

No. Sending a POST request only sends data to the backend. The backend must receive the data and execute an SQL `INSERT` operation.

### 2. What must the backend do before the new todo becomes permanent?

It must validate the request, execute an `INSERT INTO todos ...` statement, and commit the database transaction.

### 3. After creating a todo, how would you make it appear on the page?

The frontend can add the returned todo to the existing list, or fetch `GET /todos` again and re-render the list.

### 4. How would you avoid displaying thousands of todo items at the same time?

Use pagination or another form of limited querying, for example requesting only a fixed number of records per page with SQL `LIMIT` and `OFFSET`.

### 5. What information should the frontend send when a todo is marked complete?

It should send the todo's ID and its new completed Boolean value.

### 6. Why should SQL queries use parameters instead of placing user values directly inside the query string?

Parameterized queries keep values separate from the SQL statement and help prevent SQL injection and quoting-related SQL errors.
