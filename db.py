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
def register(nama, email, password):
    hashed_password = hash_password(password);
    try:
        query = "insert into users(nama, email, password) values (%s, %s, %s) returning id"
        value = (nama, email, hashed_password)
        user_id = execute_post(query, value)['data']['returning_id']
        toko_id = create_new_store(user_id)['data']['returning_id'] # creating new store to the user
        return {
            'message': 'success',
            'data': {
                'user_id': user_id,
                'toko_id': toko_id,
            }
        }
    except Exception as e:
        return {
            'message': 'failed',
        }

def create_new_store(user_id):
    try:
        query = "insert into toko(user_id, nama, alamat, nohp, shopee, tokopedia, instagram) values (%s, '-', '-', '-', '-', '-', '-' ) returning id"
        value = (user_id,)
        toko_id = execute_post(query, value)
        return toko_id
    except Exception as e:
        return 0

# TOKO
def update_toko(toko_id, nama, alamat, nohp, shopee, tokopedia, instagram):
    try:
        query = """
                update toko set nama=%s, alamat=%s, nohp=%s, shopee=%s, tokopedia=%s, instagram=%s where id=%s returning id
                """
        value = (nama, alamat, nohp, shopee, tokopedia, instagram, toko_id)
        toko_id = execute_post(query, value)
        return {
            "message": "success"
        }
    except Exception as e:
        print(e)
        return {
            "message": "failed"
        }

def get_toko(user_id):
    query = """
            select * from toko where user_id=%s
            """
    toko = execute_get(query, (user_id))[0]

    return {
        "nama": toko[2],
        "alamat": toko[3],
        "nohp": toko[4],
        "shopee": toko[5],
        "tokopedia": toko[6],
        "instagram": toko[7]
    }

def add_product(toko_id, nama, harga, imageUrl):
    try:
        query = """
                insert into produk (toko_id, nama, harga, imageUrl)
                values (%s, %s, %s, %s) returning id
                """
        value = (toko_id, nama, harga, imageUrl)
        product_id = execute_post(query, value)
        return {
            "message": "success",
            "product_id": product_id
        }
    except Exception as e:
        return {
            "message": "failed"
        }

# LOGIN
def login(email, password):
    query = """
            select users.password, users.nama, users.email, users.id, toko.id
            from users join toko on users.id=toko.user_id
            where users.email=%s
            """
    val = (email, )
    result = execute_get(query, val)[0]
    hashed = result[0].encode()
    nama = result[1]
    email = result[2]
    user_id = result[3]
    toko_id = result[4]
    if password_matches(password, hashed):
        return {
            'message': 'success',
            'nama': nama,
            'email': email,
            'user_id': user_id,
            'toko_id': toko_id
        }
    else :
        return {
            'message': 'failed'
        }

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def password_matches(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
