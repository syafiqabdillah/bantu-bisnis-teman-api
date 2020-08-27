import os
import psycopg2
import datetime
from dotenv import load_dotenv
import json
import uuid
import string 
import random 
import bcrypt

load_dotenv()

DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')

def execute_get(query, val):
    connection = psycopg2.connect(
        user=DB_USER,
        host=DB_HOST,
        database=DB_NAME,
        password=DB_PASS,
    )
    cursor = connection.cursor()
    cursor.execute(query, val)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

## query must include RETURNING ID in the end 
def execute_post(query, val):
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(query, val)
        connection.commit()
        returning_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return {
            'message': 'success',
            'data': {
                'returning_id': returning_id
            }
        }
    except Exception as e:
        return {
            'message': 'failed'
        }

# USERS 
def get_all_users():
    query = """
            select * from users
            """
    lst = execute_get(query, ())
    result = []
    for item in lst:
        print(item)
        result.append(item)
    return result

# REGISTER
def register(nama, email):
    # generate random password 
    random_string, hashed_password = generate_password()
    try:
        query = "insert into users(nama, email, password) values (%s, %s, %s) returning id"
        value = (nama, email, hashed_password)
        user_id = execute_post(query, value)
        return {
            'message': 'success',
            'data': {
                'id': user_id,
                'random_string': random_string
            }
        }
    except Exception as e:
        return {
            'message': 'failed',
        }

# LOGIN
def login(email, password):
    query = "select password from users where email=%s"
    val = (email, )
    hashed = execute_get(query, val)[0][0].encode()
    if password_matches(password, hashed):
        return {
            'message': 'success'
        }
    else :
        return {
            'message': 'failed'
        }

def generate_password(length=10):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    hashed_password = bcrypt.hashpw(random_string.encode(), bcrypt.gensalt()).decode()
    return random_string, hashed_password

def password_matches(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
