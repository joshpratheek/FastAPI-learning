# FastAPI Learning Journey

Learning **Python backend development and REST APIs** using [freeCodeCamp's *Python API Development — Comprehensive Course for Beginners*](https://www.youtube.com/watch?v=0sOvCWFmrtA), taught by Sanjeev Thiyagarajan.

## My goal

Learn to design, build, test, and document FastAPI backends. Focus on Python, HTTP, JSON, validation, CRUD, databases, authentication, and API testing — **not** frontend design, Bootstrap, or Jinja2 templates.

## Projects

### freeCodeCamp tutorial — working locally

Following the instructor's social-media-style API project. My local tutorial folder is named `fcc-tut` (as shown in my workspace). **No tutorial source code is committed to this repository yet**, so the example below documents concepts rather than claiming to be a copy of my current local `main.py`.

### [StudyTrack — independent API project](studytrack/main.py)

Apply each lesson to my own study-session tracking API **after** completing the corresponding tutorial practice. The version currently committed has three in-memory study sessions and GET endpoints `/`, `/sessions`, and `/first-session`.

## Current progress — through HTTP requests, POST requests, request bodies, and parameters

**Course section reached:** Starting FastAPI (36:21), Path Operations (39:23), Postman introduction (53:22), and HTTP Requests / first POST request (57:34 onwards).  
**Next section:** Schema Validation with Pydantic (1:07:29).  
**Status:** Reached this point in the video. Practised sending JSON with FastAPI's Swagger UI and discussed its connection to Postman; the local Python source has not been independently inspected or committed here.

### Concepts learned so far

- **API / REST:** An HTTP interface for clients to access resources. GET commonly reads data; POST commonly submits data.
- **FastAPI app:** `app = FastAPI()` creates the application instance.
- **Path operations:** `@app.get("/")` and `@app.post("/createposts")` combine an HTTP method and URL path with a Python handler function.
- **Responses:** Returning a Python dictionary from a FastAPI endpoint sends a JSON response.
- **Postman:** An HTTP client for sending GET/POST requests and inspecting the status and response, without building a frontend.
- **Request body:** A POST request can carry JSON in its body. FastAPI can read the body as a Python dictionary.
- **`Body(...)`:** Declares that the handler expects a required request body.
- **`print(...)` versus `return`:** `print` writes to the server terminal; `return` produces the response sent to the client.

### My understanding — payload, Body, parameters and arguments

I learned that in this function:

```python
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload["title"])
    return {"message": "Successfully created posts"}
```

- **`payload` is a function parameter**, not a dictionary assigned at the moment of defining the function.
- **`: dict` is a type annotation:** FastAPI expects a JSON object and parses it as a Python dictionary.
- **`= Body(...)` declares that the value should come from the HTTP request body** and that the body is required. `...` is Python's `Ellipsis`, passed as an argument to `Body()`.
- **`Body` can be imported with `from fastapi import Body`.** The video may show a more specific import location, but the public import is sufficient.
- When Postman or Swagger UI sends `{"title": "Python", "content": "Learning APIs"}`, FastAPI extracts the JSON body and supplies that dictionary as the actual value of `payload`.
- `payload["title"]` accesses the value using the dictionary key, so `print(payload["title"])` prints `Python` in the server terminal.
- **Parameter versus argument:** `payload` is the parameter declared in `def create_posts(...)`. The incoming dictionary is the value supplied to it when FastAPI calls the endpoint. The `"/createposts"` string is also an argument to `app.post()`, and `...` is an argument to `Body()`.
- **Without `: dict`:** `payload = Body(...)` is valid but provides weaker type validation and less-specific generated API documentation. Keeping the type annotation is better.
- **POST does not automatically save data:** This example only receives the request and responds; storage logic is a separate step.

#### Swagger UI versus Postman — my practical test

I opened `POST /createposts` in `/docs` and observed **Request body required** and Swagger's generated `{"additionalProp1": {}}` placeholder. That placeholder appears because the endpoint accepts a generic dictionary without a defined field schema.

I replaced it with a JSON object and executed the request. **Swagger UI and Postman are both HTTP clients** that can send the same JSON to the same FastAPI endpoint; the server-side `payload` receives the data the same way regardless of which client sends it. Swagger UI is auto-generated from FastAPI's schema, while Postman is a separate API testing client.

**Question resolved:** The Pydantic class I remembered from earlier API practice is a *different way of declaring and validating a request body*. It is written in Python, not inside Swagger UI. We'll learn that next in the Pydantic section.

### Consolidated practice example for this stage

*This is a learning summary of the instructor's early route/request-body patterns, not a verified copy of my local project file.*

```python
from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "Here are your posts"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)  # Server terminal
    return {"message": "Successfully created posts"}  # JSON response
```

Example JSON sent by Postman to `POST http://127.0.0.1:8000/createposts`:

```json
{
  "title": "Learning FastAPI",
  "content": "Today I learned POST requests"
}
```

**Important:** This example receives JSON but does **not** save the new post. In-memory storage and full CRUD will be covered in later sections. Accepting `dict` also doesn't yet validate specific fields; Pydantic addresses that next.

### Test locally (in the tutorial directory)

```powershell
python -m uvicorn main:app --reload
```

- `http://127.0.0.1:8000/` — GET route.
- `http://127.0.0.1:8000/posts` — GET example.
- `http://127.0.0.1:8000/docs` — FastAPI's interactive documentation.
- In Postman, set method to **POST**, URL to `http://127.0.0.1:8000/createposts`, choose **Body → raw → JSON**, provide the JSON example, and press **Send**.

The actual route paths depend on the code currently saved in `fcc-tut/main.py`.

## Learning workflow

1. Watch the freeCodeCamp lesson in sequence.
2. Understand the logic behind the instructor's Python code.
3. Write and test the tutorial project myself.
4. Apply the same concepts independently to StudyTrack.
5. Update this README after meaningful lessons and explanations, documenting what I actually understood, questions resolved, code examples, mistakes, corrections, and confirmed test results. For longer lessons, use detailed notes in the `notes/` folder and link them here.

## Topics coming up

- Pydantic request validation and schemas
- CRUD and in-memory post storage
- Path parameters, status codes, and error handling
- PostgreSQL, SQLAlchemy, and databases
- Authentication and authorization
- API testing and deployment

## Safety

This is a **public repository**. Before committing or pushing, check for passwords, tokens, API keys, personal information, `.env` files, and private database contents. Do not assume `.gitignore` protects files that were already tracked.
