from cryptography import fernet
from pymongo import MongoClient
import secrets
import string

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

def generate_key():
    return fernet.Fernet.generate_key()
def get_db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['password_db']
    return db
print(get_db_connection())