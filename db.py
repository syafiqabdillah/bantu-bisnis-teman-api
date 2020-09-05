import os
import psycopg2
import datetime
from dotenv import load_dotenv
import json
import uuid
import string
import random
import bcrypt
import time

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


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

# query must include RETURNING ID in the end


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


def email_available(email):
    query = "select nama from users where email=%s"
    value = (email, )
    lst = execute_get(query, value)
    return len(lst) < 1


def register(nama, email, password):
    hashed_password = hash_password(password)
    try:
        query = "insert into users(nama, email, password) values (%s, %s, %s) returning id"
        value = (nama, email, hashed_password)
        user_id = execute_post(query, value)['data']['returning_id']
        # creating new store to the user
        toko_id = create_new_store(user_id)['data']['returning_id']
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


def kontak_toko(toko_id):
    query = """
            select * from toko where id=%s
            """
    detail = execute_get(query, (toko_id,))[0]
    return {
        "id": detail[0],
        "nama": detail[2],
        "alamat": detail[3],
        "nohp": detail[4],
        "shopee": detail[5],
        "tokopedia": detail[6],
        "instagram": detail[7]
    }

# KATEGORI


def add_kategori(nama):
    query = "insert into kategori (nama) values (%s) returning id"
    value = (nama,)
    kategori = execute_post(query, value)
    return kategori


def kategori():
    query = "select * from kategori"
    list_kategori = execute_get(query, ())
    objected_list_kategori = [
        {
            'id': kat[0],
            'nama': kat[1]
        }
        for kat in list_kategori]
    return objected_list_kategori

# PRODUCT


def add_product(toko_id, kategori_id, nama, harga, imageUrl):
    query = """
            insert into produk (toko_id, kategori_id, nama, harga, imageUrl)
            values (%s, %s, %s, %s, %s) returning id
            """
    value = (toko_id, kategori_id, nama, harga, imageUrl)
    query_result = execute_post(query, value)
    return query_result


def update_product(produk_id, nama, kategori_id, harga, imageUrl, status):
    query = """
            update produk set nama=%s, kategori_id=%s, harga=%s, imageUrl=%s, status=%s
            where id=%s returning id 
            """
    value = (nama, kategori_id, harga, imageUrl, status, produk_id)
    query_result = execute_post(query, value)
    return query_result


def products(toko_id):
    try:
        query = """
                select id, nama, harga, imageUrl, status, kategori_id from produk where toko_id=%s
                """
        products = execute_get(query, (toko_id,))
        results = [{
            "id": product[0],
            "nama": product[1],
            "harga": str(product[2]),
            "imageUrl": product[3],
            "status": product[4],
            "kategori_id": product[5]
        } for product in products]
        return results
    except Exception as e:
        return None


def all_products():
    try:
        query = """
                select produk.id, produk.nama, produk.harga, produk.imageUrl, toko.nama, toko.id, users.nama 
                from users join toko on users.id = toko.user_id
                join produk on toko.id=produk.toko_id
                where produk.status='active'
                order by random()
                limit 10
                """
        products = execute_get(query, ())
        results = [{
            "id": product[0],
            "namaProduk": product[1],
            "harga": str(product[2]),
            "imageUrl": product[3],
            "namaToko": product[4],
            "idToko": product[5],
            "namaSeller": product[6],
            "key": product[0] + int(time.time())
        } for product in products]
        return results
    except Exception as e:
        return None


def search_products(search_query):
    try:
        query = """
                select produk.id, produk.nama, produk.harga, produk.imageUrl, toko.nama, toko.id, users.nama 
                from users join toko on users.id = toko.user_id
                join produk on toko.id=produk.toko_id
                where lower(produk.nama) like %s 
                or lower(toko.nama) like %s 
                or lower(users.nama) like %s
                order by random()
                limit 20
                """
        search = f'%{search_query}%'
        products = execute_get(query, (search, search, search))
        results = [{
            "id": product[0],
            "namaProduk": product[1],
            "harga": str(product[2]),
            "imageUrl": product[3],
            "namaToko": product[4],
            "idToko": product[5],
            "namaSeller": product[6],
            "key": product[0] + int(time.time())
        } for product in products]
        return results
    except Exception as e:
        return None


def search_products_by_category(kategori_id):
    try:
        query = """
                select produk.id, produk.nama, produk.harga, produk.imageUrl, toko.nama, toko.id, users.nama 
                from users join toko on users.id = toko.user_id
                join produk on toko.id=produk.toko_id
                where produk.kategori_id=%s
                order by random()
                limit 20
                """
        products = execute_get(query, (kategori_id, ))
        results = [{
            "id": product[0],
            "namaProduk": product[1],
            "harga": str(product[2]),
            "imageUrl": product[3],
            "namaToko": product[4],
            "idToko": product[5],
            "namaSeller": product[6],
            "key": product[0] + int(time.time())
        } for product in products]
        return results
    except Exception as e:
        return None

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
    else:
        return {
            'message': 'failed'
        }


def get_view_sum(produk_id):
    query = "select count(1) from produk_view where produk_id=%s"
    value = (produk_id, )
    view_sum = execute_get(query, value)[0][0]
    return view_sum


def add_view(produk_id):
    query = "insert into produk_view(produk_id, timestamp) values (%s, %s) returning id"
    value = (produk_id, datetime.datetime.now())
    return execute_post(query, value)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def password_matches(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
