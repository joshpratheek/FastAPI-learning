# FastAPI Learning Journey

Learning **Python backend development and REST APIs** using [freeCodeCamp's *Python API Development — Comprehensive Course for Beginners*](https://www.youtube.com/watch?v=0sOvCWFmrtA), taught by Sanjeev Thiyagarajan.

## My goal

Learn to design, build, test, and document FastAPI backends. Focus on Python, HTTP, JSON, validation, CRUD, databases, authentication, and API testing — **not** frontend design, Bootstrap, or Jinja2 templates.

## Projects

### [freeCodeCamp tutorial — Pydantic and in-memory CRUD](fcc-tut/main.py)

Following the instructor's social-media-style backend API project in `fcc-tut`. The initial GET/POST code and the updated Pydantic validation code have both been committed to GitHub and reviewed.

### [StudyTrack — independent API project](studytrack/main.py)

Apply each lesson to my own study-session tracking API **after** completing the corresponding tutorial practice. The version currently committed has three in-memory study sessions and GET endpoints `/`, `/sessions`, and `/first-session`.

## Current progress — CRUD review complete; learning Python packages

**Course section reached:** Starting FastAPI (36:21), Path Operations (39:23), Postman introduction (53:22), and HTTP Requests / first POST request (57:34 onwards).  
**Most recently discussed:** GET by ID, route ordering, HTTP status codes, DELETE using `enumerate()` and `pop()`, PUT using indexed list assignment, and Python package/module imports. **Current lesson reached:** organizing `main.py` under an `app/` package. Database setup begins later in the course.  
**Status:** An earlier Pydantic `Post` model and POST endpoint are committed to GitHub. All four in-memory CRUD operations were written/reviewed in chat; the `app/` directory and imports were reviewed conceptually. **These newer changes have NOT yet been verified in the repository's `fcc-tut/main.py`.** The learner plans to update, test and push that file locally. The reviewer has not executed the local API.

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

## In-memory CRUD — first GET and POST storing posts (earlier checkpoint)

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

## Learning checkpoint — GET by ID through CRUD completion and Python packages (2026-11-23)

**Source of this section:** Code and explanations written and reviewed in conversation, **not** verified as committed code. The checked GitHub `fcc-tut/main.py` still contains the earlier Pydantic/POST version at this checkpoint.

### GET one post, 404 errors, and path ordering

```python
def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    # Implicit None if no match

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return {"post_details": post}
```

- `/posts/{id}` is a dynamic path. With `id: int`, FastAPI validates/converts a path segment such as `"2"` into `2`; `"latest"` fails integer validation if it is captured by that route.
- **Route order matters:** register a specific route such as `/posts/latest` before a conflicting dynamic route `/posts/{id}` to avoid the dynamic route capturing `latest`.
- `find_post` performs a linear scan and returns the entire matching dictionary; if it finds none, Python implicitly returns `None`.
- Check `post is None` to raise `HTTPException(status_code=404)`, otherwise the matching post is returned.
- **Learning check:** The learner correctly explained that a found dictionary skips the exception block, and that a path parameter's type is validated by FastAPI.

### HTTP response status versus body

- `@app.post("/posts", status_code=201)` sets the **HTTP status** to `201 Created` after successful execution.
- `return {"new_post": post_dict}` sets the **response body**; FastAPI serializes the Python dictionary to JSON for the client.
- `200 OK` is a common successful GET/update response; `404 Not Found` indicates missing requested posts; `422` indicates request/path validation failure.
- A successful DELETE can use `204 No Content`: **do not return a JSON body** along with 204. The learner initially set `status_code=204` while still returning `{"post_details": deleted_post}`, and corrected this conceptual mismatch.

### DELETE: from post ID to list index

```python
def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    my_posts.pop(post_index)
```

- `enumerate(my_posts)` yields the index and dictionary as each iteration proceeds.
- `my_posts.pop(index)` removes (and returns) an item **by list index**, not by its `"id"` value.
- **The difference:** `find_post(id)` returns a dictionary for GET; `find_index_post(id)` returns its list index for DELETE/PUT.
- Check for `None` **before** `pop`; calling `pop(None)` when no match exists raises a Python error rather than the intended 404.
- `0 is None` is `False`: list index 0 is valid. `if not post_index` would incorrectly reject index 0 because 0 is falsy.
- **Mistakes corrected:** Initial `find_index_post` returned the first `(index, post)` pair without comparing IDs; the corrected version compares `post["id"] == id` and returns only the index. Initial DELETE annotated `id: id` instead of `id: int`, and called `pop` before checking for a missing post.
- **Important clarification prompted by DSA-style reasoning:** Removing a post shifts subsequent **list indexes**, but doesn't alter the `"id"` values inside the remaining dictionaries. After deleting ID 1, GET ID 1 should return 404 even if another post moves into index 0.

### UPDATE (PUT): replace a post while preserving its ID

```python
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {"updated_post": my_posts[post_index]}
```

- `id: int` comes from the URL and identifies **which** post to update. `post: Post` comes from the JSON body and contains **what** data to use.
- `post.model_dump()` has no `id` because the request model doesn't declare one; the existing ID must be restored with `post_dict["id"] = id`.
- Replace at the correct list index using `my_posts[post_index] = post_dict`. This does **not** append or remove an element.
- **Mistakes corrected:** `my_posts(post_index)` incorrectly tries to call a list as a function; `my_posts["id"] = post_index` incorrectly indexes a list by a string, confuses list position with ID, and modifies the wrong object. Correct assignment adds `id` to `post_dict`, then stores it in `my_posts[post_index]`.
- **Learning check:** For `PUT /posts/20` where the target is at list index 1, the updated dictionary must retain `"id": 20`, not 1. The learner answered this correctly.

### CRUD operations at a glance

| Operation | Method/path | In-memory action |
| --- | --- | --- |
| Create | `POST /posts` | Validate, `model_dump()`, assign ID, `my_posts.append(post_dict)`; respond 201 |
| Read all | `GET /posts` | Return `my_posts` |
| Read one | `GET /posts/{id}` | Scan for matching `"id"`; 404 if absent |
| Update | `PUT /posts/{id}` | Find index, preserve ID, assign `my_posts[index] = post_dict` |
| Delete | `DELETE /posts/{id}` | Find index, check missing, `my_posts.pop(index)`; respond 204 without body |

**Current limitations:** Storage is in memory and is reset on server restart. `randint` can generate colliding IDs. This is appropriate tutorial practice, not yet a production database-backed API.

### Python modules and packages — organizing under `app/`

Planned project layout once local code is reorganized:

```text
fcc-tut/
└── app/
    ├── __init__.py
    └── main.py
```

- A **module** is a Python file (such as `main.py`). A **package** groups modules under a package name (here `app`); `__init__.py` conventionally marks an ordinary package and may remain empty. Modern Python also supports namespace packages without this file.
- After moving `main.py` into `app/`, start Uvicorn **from the `fcc-tut/` directory** with `python -m uvicorn app.main:app --reload`.
- Pattern: `package.module:instance`. In `app.main:app`, the first `app` is the package, `main` is the file/module, and the last `app` is the variable holding `FastAPI()`.
- Example variation: `backend/server.py` with `api = FastAPI()` runs as `python -m uvicorn backend.server:api --reload`. The learner initially answered `server.main:app` and corrected the naming concept.
- For `app/models.py` with class `User`, valid imports from `app/main.py` are `from app.models import User` (**absolute**) or `from .models import User` (**relative**), assuming `main.py` is imported as part of the package. The learner arrived at both valid forms.
- The existing endpoint logic need not change merely because `main.py` is moved, but module imports and the launch command may need updating.

**Next steps for the learner:** Copy/rewrite the reviewed CRUD handlers into local `main.py`; create `app/__init__.py` and move `main.py` inside `app/`; run the new Uvicorn command; test POST, GET by ID, PUT, DELETE, missing-ID 404s, and 204 without a body; then commit and push. These tests and the rearranged files have **not yet been verified** in the GitHub repository.

## Topics coming up

- [x] Pydantic request validation and schemas (committed checkpoint)
- [x] CRUD and in-memory post storage (reviewed in chat; push pending)
- [x] Path parameters, route ordering, status codes, and error handling (reviewed in chat; push pending)
- [x] Python packages, `app/` folder, imports and Uvicorn entry point (conceptual review; local restructure pending)
- PostgreSQL, SQLAlchemy, and databases
- Authentication and authorization
- API testing and deployment

## Safety

This is a **public repository**. Before committing or pushing, check for passwords, tokens, API keys, personal information, `.env` files, and private database contents. Do not assume `.gitignore` protects files that were already tracked.
