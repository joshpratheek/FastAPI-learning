# Lesson 01 — FastAPI Fundamentals

**Learning path:** Corey Schafer FastAPI video 1 → recap → independent StudyTrack practice.  
**Status:** Concepts reviewed and StudyTrack starter code written; local Swagger UI tests still to be confirmed.

## What I learned

### FastAPI application instance
```python
from fastapi import FastAPI  # Import FastAPI class from package

app = FastAPI()  # Create the application object (an instance)
```

`FastAPI` is the class; `app` is an instance. The app registers API routes and helps process HTTP requests.

### GET routes and decorators
```python
@app.get("/")  # Register a GET route for the root path
def home():
    return {"message": "Home Page"}

@app.get("/about")
def about():
    return {"message": "about page"}
```

A route matches an **HTTP method + URL path** to a Python function. `@app.get("/about")` registers `about()` as the GET handler for `/about`. It is not “calling the app instance” to display a page. GET can return static information; it need not query a database.

### Python objects versus JSON
```python
posts = [
    {"id": 1, "title": "First Post", "author": "Corey"},
    {"id": 2, "title": "Second Post", "author": "Alex"},
]

@app.get("/posts")
def get_posts():
    return posts  # Python list -> JSON array

@app.get("/first-post")
def get_first_post():
    return posts[0]  # Python dictionary -> JSON object
```

- `posts` is a **Python list containing dictionaries**.
- `posts[0]` gets the first dictionary by **list position**, not by the value of its `id`.
- FastAPI serializes common Python return values into JSON for the HTTP response.
- Python `list` → JSON array `[...]`; Python `dict` → JSON object `{...}`.
- Python `True`/`False` → JSON `true`/`false`; Python `None` → JSON `null`.

**Correction from revision:** Returning `posts` does not discard its list structure. The client receives a JSON **array**. Returning `posts[0]` produces a JSON **object**.

### Run the app and view auto-generated documentation
```powershell
python -m uvicorn main:app --reload
```

- `main`: module/file `main.py`
- `app`: FastAPI object defined in that module
- `--reload`: restart dev server after source code changes

Visit:
- `http://127.0.0.1:8000/` for the root route
- `http://127.0.0.1:8000/docs` for interactive Swagger UI
- `http://127.0.0.1:8000/redoc` for ReDoc API reference

FastAPI also supports HTML responses, but this lesson's practice uses JSON.

## Independent practice — StudyTrack API

Goal: create three in-memory study-session records and three GET routes without using a database.

**Final code written and reviewed:**
```python
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

# A Python list containing three dictionaries
study_sessions = [
    {"id": 1, "subject": "Hindi", "duration_minutes": 90},
    {"id": 2, "subject": "Telugu", "duration_minutes": 60},
    {"id": 3, "subject": "Python", "duration_minutes": 120}
]

@app.get("/")
def home():
    return {"message": "Welcome to StudyTrack"}

@app.get("/sessions")
def get_sessions():
    return study_sessions  # Entire list -> JSON array

@app.get("/first-session")
def get_first_session():
    return study_sessions[0]  # First dict -> JSON object
```

**Expected responses:**
- GET `/`: `{"message": "Welcome to StudyTrack"}`
- GET `/sessions`: JSON array with Hindi, Telugu, and Python sessions
- GET `/first-session`: `{"id": 1, "subject": "Hindi", "duration_minutes": 90}`

*These are expected results based on the code, not independently verified local test results.*

### Mistakes I corrected

1. **Duplicate IDs:** Initially both sessions had `"id": "1"`; changed to unique integer IDs 1, 2, and 3.
2. **Only two records:** Added a third to meet the challenge.
3. **Misleading function names:** Renamed `about()` / `get_posts()` on StudyTrack routes to `get_sessions()` / `get_first_session()`.
4. **Index versus ID:** If the Python session with ID 3 moves to list index 0, `study_sessions[0]` returns that Python session, not the session with ID 1.
5. **JSON misconception:** `return posts` sends a JSON array, not a single JSON object.

## Revision questions (with answers)

**1. Why both `app = FastAPI()` and `@app.get("/hello")`?**  
The first creates the application instance; the decorator registers a GET route with its handler.

**2. What does `return posts` return?**  
A Python list within the function; a JSON array in the HTTP response.

**3. What does `return posts[0]` return?**  
A Python dictionary within the function; a JSON object in the HTTP response.

**4. What happens if `titles = ["Python", "FastAPI", "SQLAlchemy"]` is returned?**  
Inside Python it is a list; the client receives the JSON array `["Python", "FastAPI", "SQLAlchemy"]`.

**5. Why doesn't `study_sessions[0]` always return ID 1?**  
Because `[0]` refers to the first position in the list, not the value of an `id` field.

## Interview-style explanations

- **What is FastAPI?** A Python web framework for creating APIs and web applications.
- **What is an endpoint?** A URL path plus HTTP method that a server can handle.
- **What is the purpose of the decorator?** It associates a handler function with a route.
- **What is JSON serialization?** Converting a supported Python return value to a JSON representation sent over HTTP.
- **What are `/docs` and `/redoc`?** FastAPI's automatically generated API documentation interfaces.

## Next steps

- [x] Video 1 watched and revised
- [x] StudyTrack GET endpoints written and reviewed
- [ ] Test `/`, `/sessions`, `/first-session` in local Swagger UI
- [ ] Move to Video 2 after tests

**Public-repo safety:** Before every Git commit or push, check staged files for passwords, API keys, tokens, private information, `.env` files and databases with sensitive records. A `.gitignore` is useful but is not a substitute for checking changes.
