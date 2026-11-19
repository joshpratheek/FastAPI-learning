# FastAPI Learning Journey

Learning **backend API development** with Python and FastAPI, using freeCodeCamp's *Python API Development — Comprehensive Course for Beginners* (Sanjeev Thiyagarajan).

**Course:** https://www.youtube.com/watch?v=0sOvCWFmrtA

## Goal

Build REST APIs confidently: HTTP routes, request and response handling, data validation, CRUD, databases, authentication and testing. The focus is on **Python backend development**, not HTML, CSS, Bootstrap or server-rendered templates.

## Projects

### freeCodeCamp tutorial project (upcoming)

Follow the course's Python backend/social-media API project. Write and test the tutorial code step by step as each topic is covered. No tutorial application code has been committed yet.

### StudyTrack (independent practice)

[StudyTrack starter API](studytrack/main.py) is my separate study-session tracker, where I apply what I learn **after** completing the corresponding tutorial lesson.

Current saved implementation uses a Python list of three study sessions with GET endpoints: `/`, `/sessions`, and `/first-session`. These endpoints have been written and reviewed; local Swagger UI testing has not yet been confirmed.

## Learning process

1. Watch a short freeCodeCamp course section in order.
2. Understand the Python and FastAPI logic, not just copy syntax.
3. Write and test the instructor's backend tutorial code.
4. Apply the same concept independently to StudyTrack.
5. Record confirmed learning, mistakes, fixes and progress here or in the `notes/` folder.

## Current progress

- **Course selected:** freeCodeCamp's FastAPI / Python API Development course.
- **Hands-on progress in this course:** Not yet started.
- **Concepts already discussed:** FastAPI app instances, GET routes, endpoint responses, Python lists/dictionaries versus JSON, and a basic understanding of REST APIs and HTTP methods.
- **Next lesson:** Course introduction/project overview, virtual environment setup, and the first FastAPI application.

## Planned topics (not yet marked complete)

- HTTP methods and REST API design
- Route, path and query parameters
- Pydantic models and validation
- CRUD endpoints
- PostgreSQL and SQLAlchemy
- Authentication and authorization
- API testing and deployment

## Run the current StudyTrack starter

From the `studytrack` directory with FastAPI and Uvicorn installed:

    python -m uvicorn main:app --reload

Then visit `http://127.0.0.1:8000/docs`.

## Public repository safety

Never commit passwords, tokens, credentials, `.env` files, or personal information. Review changes before every commit and push.
