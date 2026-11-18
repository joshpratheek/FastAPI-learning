from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

# In-memory study sessions: a list of Python dictionaries.
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
    # Returns a JSON array of study sessions.
    return study_sessions


@app.get("/first-session")
def get_first_session():
    # Returns the first study session as a JSON object.
    return study_sessions[0]
