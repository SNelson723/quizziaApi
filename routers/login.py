from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from db.db import get_db_connection
from passlib.context import CryptContext
import psycopg2.extras

login = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

