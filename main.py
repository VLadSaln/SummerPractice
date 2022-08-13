from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from users import UserCreate, Token
import auth
from depend import get_current_user
import psycopg2

app = FastAPI()

@app.post('/signup')
def signup(user_details: UserCreate):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute(f"select username from users where username='{user_details.username}';")
    results = cursor.fetchall()

    if len(results) > 0:
        return HTTPException(status_code=400, detail='Username already used')

    hashed_password = auth.hash_password(user_details.password)
    cursor.execute(f"INSERT INTO users VALUES('{user_details.username}','{user_details.password}','{hashed_password}');")
    conn.commit()
    return {"successful registration"}

@app.post('/login')
def login(user_details: OAuth2PasswordRequestForm = Depends()):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute(f"select username from users where username='{user_details.username}';")
    results = cursor.fetchall()

    if len(results) == 0:
        return HTTPException(status_code=400, detail='Invalid username')
    
    cursor.execute(f"select password from users where username='{user_details.username}';")
    results = cursor.fetchone()
    results = results[0].replace(" ","") 
    
    cursor.execute(f"select hashedpassword from users where username='{user_details.username}';")
    results1 = cursor.fetchone()
    results1 = results1[0].replace(" ","")
    
    #user = auth.validate_password(results, results1) 

    #if not user:
        #raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return  auth.create_user_token(user_details.username)

@app.get('/secret')
def authorized(current_user: Token = Depends(get_current_user)):
    return current_user
   
   