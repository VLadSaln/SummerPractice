import hashlib
import psycopg2
import random
import string
from datetime import datetime, timedelta

def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


#def validate_password(password: str, hashed_password: str):
    
    #salt, hashed = hashed_password.split("$")
    #return hash_password(password, salt) == hashed


def create_user_token(username):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    expire = datetime.now() + timedelta(hours=2)
    cursor.execute(f"INSERT INTO token VALUES('{username}','{expire}');")
    conn.commit()

async def get_user_by_token(token: str):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute(f"select access_token from token where access_token='{token}';")
    results = cursor.fetchone()
    results = results[0].replace(" ","") 
    cursor.execute(f"select expire from token where access_token='{token}';")
    results1 = cursor.fetchone()
    results1 = results1[0].replace(" ","") 
    conn.commit()

    if (len(results) > 0 and results1 > datetime.now()):
        return await true

    


