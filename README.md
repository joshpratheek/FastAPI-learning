# FastAPI Learning Journey

Learning **Python backend development and REST APIs** using [freeCodeCamp's *Python API Development — Comprehensive Course for Beginners*](https://www.youtube.com/watch?v=0sOvCWFmrtA), taught by Sanjeev Thiyagarajan.

## My goal

Learn to design, build, test, and document FastAPI backends. Focus on Python, HTTP, JSON, validation, CRUD, databases, authentication, and API testing — **not** frontend design, Bootstrap, or Jinja2 templates.

## Projects

### [freeCodeCamp tutorial — GET, POST, and Pydantic validation](fcc-tut/main.py)

Following the instructor's social-media-style backend API project in `fcc-tut`. The initial GET/POST code and the updated Pydantic validation code have both been committed to GitHub and reviewed.

### [StudyTrack — independent API project](studytrack/main.py)

Apply each lesson to my own study-session tracking API **after** completing the corresponding tutorial practice. The version currently committed has three in-memory study sessions and GET endpoints `/`, `/sessions`, and `/first-session`.

## Current progress — Pydantic models and beginning in-memory CRUD

**Course section reached:** Starting FastAPI (36:21), Path Operations (39:23), Postman introduction (53:22), and HTTP Requests / first POST request (57:34 onwards).  
**Most recently discussed:** Pydantic validation, `model_dump()`, generating IDs, and using a Python list to create and retrieve posts. **Now learning:** In-memory CRUD Operations (from 1:22:45). Database setup begins later (3:53:48).  
**Status:** Pydantic `Post` model and an earlier POST endpoint are committed to GitHub and reviewed. The latest in-memory CRUD code was shared in chat and reviewed but has **not yet been verified as pushed to GitHub**. Live tests have not been independently run by the assistant.

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

### Pydantic lesson — model, defaults, model_dump, and generated IDs

**Pydantic model progression:** The first draft below had a required `id`, but the **latest committed version no longer includes `id`**, since the client should not need to supply it.

```python
from typing import Optional
from pydantic import BaseModel

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

- **Purpose:** A Pydantic `BaseModel` declares the structure of incoming JSON, parses it, validates required fields and types, and informs the generated API documentation. It does **not** save anything to a database.
- **Required fields:** In this version `id`, `title` and `content` have no defaults, so all three are required. A missing `content` produces a 422 validation response before the route function runs.
- **Defaults:** When omitted, `published` becomes `True` and `rating` becomes `None`. `Optional[int]` needs `from typing import Optional`; on modern Python, `int | None` is an alternative.
- **Function parameter:** `def create_post(post: Post):` instructs FastAPI to read and validate the request body into a `Post` model. An explicit `Body(...)` is not required for this basic case.
- **Object versus dictionary:** `post` is a model instance and fields can be accessed as `post.title`. `post.model_dump()` returns a regular Python dictionary. Sanjeev's `post.dict()` is the older Pydantic v1 style and is deprecated under v2.
- **Accessing fields by key versus attribute:** A Pydantic model supports `post.title`; after `post_dict = post.model_dump()`, a regular Python dictionary supports `post_dict["title"]`. Both yield the same title value. `post["title"]` is not supported by a standard Pydantic `BaseModel` instance, and regular dictionaries do not support `post_dict.title` by default. `post.model_dump()["title"]` is valid when a dictionary is needed immediately. The old raw-body `payload: dict = Body(...)` was *already a dictionary*, so `payload["title"]` worked without conversion.
- **Printing:** With input `{"id":1,"title":"Python","content":"Learning FastAPI"}`, `print(post)` shows `id=1 title='Python' content='Learning FastAPI' published=True rating=None`. By contrast, `print(post.model_dump())` prints a dictionary with keys and Python values.
- **Returning:** Both `return {"msg": post}` and `return {"msg": post.model_dump()}` yield equivalent JSON in FastAPI. `model_dump()` is useful when we need to manipulate the fields as a dictionary, not obligatory just for a response.
- **Syntax correction:** `post.__dict()` raises a `TypeError` because `__dict__` is an attribute, not a callable method. Prefer `post.model_dump()`.
- **Who creates IDs?** Typically the server/database, not the client. If IDs are server-generated, omit required `id` from the incoming `Post` schema. For in-memory examples, the server can assign unique IDs; later a database identity/sequence can do this automatically. An ID assignment alone does not persist a post.
- **Design note:** A request schema and a database model can have different responsibilities. Pydantic validation does not itself create database tables or rows.

**Learning check answered correctly:** The learner identified that missing required `content` is rejected, and that `published` defaults to `True` while `rating` defaults to `None`.

### Verified tutorial code on GitHub

The actual [`fcc-tut/main.py`](fcc-tut/main.py) at the first committed checkpoint contains:

```python
from fastapi import FastAPI
from fastapi.params import Body

app= FastAPI()

@app.get("/")
def root():
    return {"msg" : "hello world"}

@app.get("/posts")
def get_posts():
    return {"data" : "These are your posts"}

@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"msg" : "Post Created"}
```

**Code review:** All three routes, the FastAPI instance, and the required dictionary request body are valid for this stage. Importing `Body` from `fastapi.params` works; `from fastapi import Body` is the recommended public import. The POST endpoint currently echoes only a success message and does **not** persist posts; this is expected at this point. Tests were not executed by the reviewer.

**Historical checkpoint:** The example immediately above is the first commit's code. The **current code** linked in `fcc-tut/main.py` uses `Post(BaseModel)` and `create_post(post: Post)` instead.

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

## Pydantic — first independently written model (review in progress)

The next lesson introduces **Pydantic request validation**. In discussion, I correctly explained why a model with required `title` and `content` fields rejects a request missing `content`: validation runs before the endpoint handler.

I drafted this model locally (shared in chat, **not yet verified as committed**):

```python
from pydantic import BaseModel
from typing import Optional  # Correction: needed for Optional[int]

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

**Review notes:**
- `id`, `title`, and `content` are required because they have no default values.
- `published` is optional in the request and defaults to `True`.
- `rating` accepts `int` or `None`, with default `None`; the default makes it optional in incoming JSON.
- I initially forgot to import `Optional` from `typing`, which would prevent the module from loading.
- I wrote `post.__dict()`, but `__dict__` is a dictionary attribute, not a callable method. In Pydantic v2, use `post.model_dump()` when I want a normal Python dictionary. Calling `model_dump()` alone does not store data.
- Returning `{"msg": post}` is supported: FastAPI can serialize a Pydantic model into JSON.
- The client currently needs to supply `id`; later, when persistence is implemented, server-generated IDs are generally preferable.
- Declaring an endpoint parameter as `post: Post` makes FastAPI parse and validate the HTTP JSON request body using the model.
- **Update:** The missing `Optional` import was fixed, and the incorrect `post.__dict()` call was replaced with `post.model_dump()` in the committed version. Since `id` was removed, test a request with `title` and `content`, omitting `published` and `rating`, to confirm the default values.

### GitHub review checkpoint

Reviewed the connected public repository on 2026-11-20: `fcc-tut/main.py` now contains a valid `Post(BaseModel)` with required `title` and `content`, plus `published: bool = True` and `rating: Optional[int] = None`. It correctly declares `create_post(post: Post)` and returns the model in a JSON response. The `id` field was removed, and `Optional` was imported correctly.

**Minor cleanup:** The standalone `post.model_dump()` line produces a dictionary but doesn't use its return value. Either remove that line and return the model as is, or assign the result and use it. The previous `Body` import is unused and may be removed. These aren't blockers for continuing. The code was inspected on GitHub but not executed.

## In-memory CRUD — first GET and POST storing posts

**Latest code shared in conversation (not yet verified on GitHub):**

```python
from random import randint

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randint(1, 100000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}
```

What I understand:
- The same URL path can support **GET /posts** (read the list) and **POST /posts** (create a new post) because the HTTP method distinguishes the operation.
- `post: Post` validates request-body fields with Pydantic before the handler runs.
- `post.model_dump()` returns a regular Python dictionary, which can be accessed or modified by key, e.g. `post_dict["title"]`.
- `randint(1, 100000)` generates a possible ID and `post_dict["id"] = ...` adds it to the dictionary, but random IDs can collide with existing IDs.
- `my_posts.append(post_dict)` **actually stores** the post in the in-memory list, unlike the previous endpoint that only returned a success message. A following GET request can show the new entry.
- **Limitations:** This data is lost on server restart and isn't shared reliably across multiple worker processes. A real database is introduced later.
- **Code review:** Correct for this tutorial stage. `from fastapi.params import Body` is now unused and can be removed. The example above only shows the changed parts; it depends on the existing `Post(BaseModel)` in the same file.

**Next practical check:** Send a JSON POST request to `/posts` in Swagger UI, then GET `/posts` and verify the list grew by one. Review and commit the working version before assuming GitHub reflects the code in VS Code.

## Topics coming up

- [x] Pydantic request validation and schemas (committed checkpoint)
- [In progress; shared in chat, not yet verified as pushed] CRUD and in-memory post storage
- Path parameters, status codes, and error handling
- PostgreSQL, SQLAlchemy, and databases
- Authentication and authorization
- API testing and deployment

## Safety

This is a **public repository**. Before committing or pushing, check for passwords, tokens, API keys, personal information, `.env` files, and private database contents. Do not assume `.gitignore` protects files that were already tracked.
