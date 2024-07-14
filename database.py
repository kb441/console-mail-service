import json
import os

DATABASE_FILE = 'database.json'

def initialize_database():
    if not os.path.exists(DATABASE_FILE):
        data = {
            "users": [],
            "emails": []
        }
        write_database(data)

def read_database():
    if not os.path.exists(DATABASE_FILE):
        return {"users": [], "emails": []}
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
    email_id = len(data['emails']) + 1
    data['emails'].append({
        'id': email_id,
        'sender': sender,
        'receiver': receiver,
        'text': text,
        'reply_to': reply_to
    })
    write_database(data)

def get_message(message_id):
    data = read_database()
    for email in data['emails']:
        if email['id'] == message_id:
            return email
    return None

def get_user_stats(email):
    data = read_database()
    sent = sum(1 for email in data['emails'] if email['sender'] == email)
    received = sum(1 for email in data['emails'] if email['receiver'] == email)
    return {'sent': sent, 'received': received}

def list_incoming_emails(email):
    data = read_database()
    return [email for email in data['emails'] if email['receiver'] == email]

def list_outgoing_emails(email):
    data = read_database()
    return [email for email in data['emails'] if email['sender'] == email]

def get_email_by_id(email, email_id):
    data = read_database()
    for email in data['emails']:
        if email['id'] == email_id and (email['sender'] == email or email['receiver'] == email):
            return email
    return None
