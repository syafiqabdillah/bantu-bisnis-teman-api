import os 
import jwt 
from dotenv import load_dotenv

load_dotenv()

SECRET=os.getenv('DB_HOST')

encoded_jwt = jwt.encode({'some': 'payload'}, SECRET, algorithm='HS256')

def create_jwt(data):
    return jwt.encode(data, SECRET, algorithm='HS256')

def read_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])

if __name__ == "__main__":
    jawato = create_jwt({
        'tes':123,
        '234': "yiha"
    })
    print(jawato)
    print(read_jwt(jawato))