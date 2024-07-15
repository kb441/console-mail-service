import json
import os

DATABASE_FILE = 'database.json'

def initialize_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": [], "messages": []}, f, indent=4, ensure_ascii=False)

def read_database():
    if not os.path.exists(DATABASE_FILE):
        return {"users": [], "messages": []}
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

def save_message(sender, receiver, text, reply_to=None):
    data = read_database()
    message_id = len(data['messages']) + 1
    data['messages'].append({
        'id': message_id,
        'sender': sender,
        'receiver': receiver,
        'text': text,
        'reply_to': reply_to
    })
    write_database(data)

def get_message(message_id):
    data = read_database()
    for message in data['messages']:
        if message['id'] == int(message_id):
            return message
    return None

def list_messages():
    return read_database()['messages']

def get_user_stats(email):
    data = read_database()
    sent = sum(1 for message in data['messages'] if message['sender'] == email)
    received = sum(1 for message in data['messages'] if message['receiver'] == email)
    return {'sent': sent, 'received': received}

def list_incoming_emails(email):
    data = read_database()
    return [mail for mail in data['messages'] if mail['receiver'] == email]

def list_outgoing_emails(email):
    data = read_database()
    return [mail for mail in data['messages'] if mail['sender'] == email]

def get_email_by_id(email, mail_id):
    data = read_database()
    for mail in data['messages']:
        if mail['id'] == mail_id and (mail['sender'] == email or mail['receiver'] == email):
            return mail
    return None
