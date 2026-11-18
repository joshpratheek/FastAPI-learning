from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()


# Define a basic GET endpoint
@app.get("/")
def home():
    return {"message": "Corey FastAPI project is running"}