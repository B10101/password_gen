from cryptography import fernet
from pymongo import MongoClient
import secrets
import string
import os

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))


def get_db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['password_db']
    return db

def save_user_credentials(site_name, username, encrypted_password):
    db = get_db_connection()
    credentials_collection = db['credentials']
    result = credentials_collection.insert_one({
        'site_name': site_name,
        'username': username,
        'password': encrypted_password
    })
    return result.inserted_id

def fetch_user_credentials():
    db = get_db_connection()
    credentials_collection = db['credentials']
    return list(credentials_collection.find({}, {'_id': 1, 'site_name': 1, 'username': 1, 'password': 1}))

def generate_key():
    return fernet.Fernet.generate_key()

