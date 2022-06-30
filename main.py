from fastapi import FastAPI, Query
import psycopg2
import random

app = FastAPI()

@app.get('/registration')
def regist(email: str=Query(..., min_length=5, max_length=15, description="Enter your email"),password: str=Query(..., min_length=5, max_length=15, description="Enter your password")):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute(f"select useremail from registration where useremail='{email}';")
    results = cursor.fetchall()
    if len(results) > 0:
        return {"email already used"} 

    id = random.randint(1,1000)

    while len(results) > 0:
        id = random.randint(1,1000)
        cursor.execute(f"select userid from registration where userid={id};")
        results = cursor.fetchall()
        print(results)
         
    cursor.execute(f"INSERT INTO registration VALUES('{id}','{email}','{password}');")
    conn.commit()

    return{"successful registration"}
@app.get('/authorization')
def autho(email: str=Query(..., min_length=5, max_length=15, description="Enter your email"),password: str=Query(..., min_length=5, max_length=15, description="Enter your password")):
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
    password='postgres1234', host='localhost', port='5432')
    cursor = conn.cursor()
    cursor.execute(f"select useremail from registration where useremail='{email}';")
    results1 = cursor.fetchall()
    
    if len(results1) == 0:
        return {"email doesnt exist"}
    
    cursor.execute(f"select userpassword from registration where useremail='{email}';")
    results2 = cursor.fetchall() 
    check = str(results2[0])
    check = check[2:len(check)-3]
    check = check[:len(password)]

    if password != check:
        return {"invalid email or password"}
    
    conn.commit()
    
    return{"succsesful authorization"}


    
