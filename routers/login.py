from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas import User
from db.db import get_db_connection
from passlib.context import CryptContext
from utils import generate_token

login = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@login.post('/login')
def login_user(request: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:      
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
        column_names = [desc[0] for desc in cursor.description]
        user = cursor.fetchone()
        
        # If no user is found, return an error response
        if user is None:
            return JSONResponse(status_code=401, content={"success": False, "error": 2, "authenticated": False})
          
        # The password is accessible from the user dictionary established by psycopg2.extras.DictCurso => This allows us to access the password field directly
        hashed_password = user['password']
        
        # If the password does not match, return an error response => pwd_context.verify() checks the provided password against the hashed password
        if not pwd_context.verify(request.password, hashed_password):
            return JSONResponse(status_code=401, content={"success": False, "error": 1, "msg": "Invalid username or password"})
          
        # Generate a token for the user => the generate_token function creates a JWT token with the user's username
        access_token = generate_token(data={"username": user['username']})
        user_data = dict(zip(column_names, user))
        
        return {
          "access_token": access_token, 
          "token_type": "bearer", 
          "user": {
              'id': user_data['id'],
              'username': user_data['username'], 
              'email': user_data['email'], 
              'full_name': user_data['full_name'],
              'first_name': user_data.get('first_name', ''),
              'last_name': user_data.get('last_name', ''),
              'picture': user_data.get('picture', '')
          }, 
          "success": True, 
          "error": 0
        }
    except Exception as e:
        return JSONResponse(status_code=401, content={"success": False, "error": 1, "msg": str(e)})
    finally:
        if cursor:
            cursor.close()

  
@login.post('/create')
def create_user(request: User, db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        # Checking if username or email exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
        if cursor.fetchone():
            return JSONResponse(status_code=400, content={"success": False, "error": 1, "msg": "Username already exists"})
          
        cursor.execute("SELECT * FROM users WHERE email = ?", (request.email,))
        if cursor.fetchone():
            return JSONResponse(status_code=400, content={"success": False, "error": 1, "msg": "Email already exists"})

        hashed_password = pwd_context.hash(request.password)
        cursor.execute(
            "INSERT INTO users (username, password, email, username) VALUES (?, ?, ?, ?)",
            (request.username, hashed_password, request.email)
        )
        db.commit()

        return {"success": True, "error": 0}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": 1, "msg": str(e)})
    finally:
        cursor.close()


@login.post("/logout")
def logout_user(response: Response):
    # Delete the cookie by setting it empty with expiry=0 and deleting it via delete_cookie
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=False,
        samesite="lax",
        httponly= False
    )
    
    # Failsafe if the cookie doesn't get remove the cookie
    response.set_cookie(
        key="access_token",
        value="",
        max_age=0,
        expires=0,
        path="/",
        secure=False,
        samesite="lax",
        httponly=True,
    )
    return {"error": 0, "success": True, "message": "Logged out successfully"}

@login.post("/google_login")
def google_login(email: str, db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:      
        # Get the user by email
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        # If no user is found, return an error response
        if user is None:
            return JSONResponse(status_code=401, content={"success": False, "error": 2, "authenticated": False})
          
        # Generate a token for the user => the generate_token function creates a JWT token with the user's username
        access_token = generate_token(data={"username": user['username']})
        
        return {
          "access_token": access_token, 
          "success": True, 
          "error": 0
        }
    except Exception as e:
        return JSONResponse(status_code=401, content={"success": False, "error": 1, "msg": str(e)})
    finally:
        # Ensure the cursor is closed even if an error occurs
        if cursor:
            cursor.close()
  