import json
import os

DATABASE_FILE = 'database.json'

def read_database():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_database(data):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_by_email(email):
    users = read_database()
    for user in users:
        if user['email'] == email:
            return user
    return None

def add_user(name, email, password):
    users = read_database()
    users.append({'name': name, 'email': email, 'password': password})
    write_database(users)

def delete_user(email):
    users = read_database()
    users = [user for user in users if user['email'] != email]
    write_database(users)

def list_users():
    return read_database()
