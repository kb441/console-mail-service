import json
import os

DATABASE_FILE = 'database.json'

def read_database():
    if not os.path.exists(DATABASE_FILE):
        return {'users': [], 'mails': []}
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_database(data):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_by_email(email):
    data = read_database()
    for user in data['users']:
        if user['email'] == email:
            return user
    return None

def add_user(name, email, password):
    data = read_database()
    data['users'].append({'name': name, 'email': email, 'password': password})
    write_database(data)

def delete_user(email):
    data = read_database()
    data['users'] = [user for user in data['users'] if user['email'] != email]
    write_database(data)

def list_users():
    return read_database()['users']

def add_mail(sender, receiver, subject, content):
    data = read_database()
    mail_id = len(data['mails']) + 1
    data['mails'].append({
        'id': mail_id,
        'sender': sender,
        'receiver': receiver,
        'subject': subject,
        'content': content
    })
    write_database(data)
    return mail_id

def list_incoming_mails(email):
    data = read_database()
    return [mail for mail in data['mails'] if mail['receiver'] == email]

def list_outgoing_mails(email):
    data = read_database()
    return [mail for mail in data['mails'] if mail['sender'] == email]

def get_mail_by_id(email, mail_id):
    data = read_database()
    for mail in data['mails']:
        if mail['id'] == mail_id and (mail['sender'] == email or mail['receiver'] == email):
            return mail
    return None
