from fastapi import FastAPI, Query
import psycopg2
import random

app = FastAPI()

@app.get('/registration')
def regist(email: str=Query(..., min_length=5, max_length=15, description="Enter your email"),password: str=Query(..., min_length=5, max_length=15, description="Enter your password")):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    results=[1]

    while len(results) > 0:
        id = random.randint(1,1000)
        cursor.execute(f"select userid from registration where userid={id};")
        results = cursor.fetchall()
        print(results)
        
    cursor.execute(f"INSERT INTO registration VALUES('{id}','{email}','{password}');")
    conn.commit()

    return{"successful registration"}
