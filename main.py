from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return "Welcome to the Quizzia API. Please visit /docs for API documentation."
  
  

# the command for running uvicorn on port 5000
# uvicorn main:app --reload --port 5000

# This allows React Native to also hit these endpoints
# uvicorn main:app --host 0.0.0.0 --reload --port 5000