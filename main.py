from cryptography import fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pymongo import MongoClient
import secrets
import string
import os
import base64

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

def fetch_user_credentials(site, username):
    db = get_db_connection()
    credentials_collection = db['credentials']
    doc = credentials_collection.find_one({'site_name': site, 'username': username}, {'_id': 0, 'password': 1})
    if doc:
        return doc['password']
    else:
        return None

def encrypt(pas):
    print("Encrypting password...")
    password = input("Enter encryption password: ").encode()
    en = os.getenv('enc_salt')
    if en is None:
        raise ValueError("Environment variable 'enc_salt' not set")
    salt = base64.b64decode(en)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = fernet.Fernet(key)
    encrypted_message = f.encrypt(pas.encode('utf-8'))
    return encrypted_message

def decrypt(encrypted_message):
    print("Decrypting password...")
    password = input("Enter encryption password: ").encode()
    en = os.getenv('enc_salt')
    if en is None:
        raise ValueError("Environment variable 'enc_salt' not set")
    salt = base64.b64decode(en)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = fernet.Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    
    return decrypted_message

def main():
    get_db_connection()

    print('Hi, What option do you want? (Use the number of the task)')
    print('1. Generate Password ')
    print('2. Retrieve password from database')

    choice = input('Enter your choice: ')

    if(choice == '1'):
        site = input("Enter the site name: ")
        user_name = input("Enter the username or email: ")

        print("Generating password")
        pas = generate_password()
        print(f"Password is:{pas}")

        print('Encrypting Password ...')
        encrypted_message = encrypt(pas)
         
        print("Saving to database...")
        save_user_credentials(site, user_name, encrypted_message)
    if(choice == '2'):
        site = input("Enter the site name: ")
        user_name = input("Enter the username or email: ")
        print("Fetching Password: ")
        decrypted_password = decrypt(fetch_user_credentials(site,user_name))
        print(decrypted_password.decode())

     
    

if __name__ == "__main__":
    main()
    



