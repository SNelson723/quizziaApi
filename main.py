from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from routers import login
from utils import get_current_user
from db.db import get_db_connection
from schemas.schemas import TokenData

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
  
@app.get("/auth_test")
# defines the endpoint function => db parameter tells FastAPI to run the connection function and pass its result (a db connection) as the db argument
# current_user parameter uses the get_current_user function to extract and validate the JWT token from the request headers
def auth_test(db=Depends(get_db_connection), current_user: TokenData = Depends(get_current_user)):
    try:
      # Return the auth_test in a structured format
      return {
          "success": True,
          "auth_test": "Working boii",
          "error": 0
      }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error": 1
        }
  
app.include_router(login.login, prefix="/auth", tags=["auth"])

# the command for running uvicorn on port 5000
# uvicorn main:app --reload --port 5000

# This allows React Native to also hit these endpoints
# uvicorn main:app --host 0.0.0.0 --reload --port 5000