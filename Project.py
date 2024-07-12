import json
from datetime import datetime

# Файл для хранения данных
DATA_FILE = 'mail_system.json'

# Инициализация базы данных
def initialize_database():
    try:
        with open(DATA_FILE, 'x') as file:
            json.dump({"accounts": [], "messages": []}, file)
    except FileExistsError:
        pass

class MailSystem:
    def __init__(self):
        self.load_data()

    def load_data(self):
        with open(DATA_FILE, 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        with open(DATA_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_account(self, email):
        if any(account['email'] == email for account in self.data['accounts']):
            print(f"Account with email {email} already exists.")
            return

        account = {
            "id": len(self.data['accounts']) + 1,
            "email": email,
            "sent_messages": 0,
            "received_messages": 0
        }
        self.data['accounts'].append(account)
        self.save_data()

    def get_account_by_email(self, email):
        return next((account for account in self.data['accounts'] if account['email'] == email), None)

    def get_account_by_id(self, account_id):
        return next((account for account in self.data['accounts'] if account['id'] == account_id), None)

    def send_message(self, sender_email, receiver_email, content):
        sender = self.get_account_by_email(sender_email)
        receiver = self.get_account_by_email(receiver_email)

        if not sender or not receiver:
            print("Sender or receiver does not exist.")
            return

        message = {
            "id": len(self.data['messages']) + 1,
            "sender_id": sender['id'],
            "receiver_id": receiver['id'],
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.data['messages'].append(message)

        sender['sent_messages'] += 1
        receiver['received_messages'] += 1
        self.save_data()

    def reply_to_message(self, message_id, sender_email, content):
        message = next((msg for msg in self.data['messages'] if msg['id'] == message_id), None)

        if not message:
            print("Message not found.")
            return

        receiver = self.get_account_by_id(message['sender_id'])  # Получатель оригинального сообщения

        self.send_message(sender_email, receiver['email'], content)  # receiver['email'] это email получателя

    def get_account_info(self, email_or_id):
        if isinstance(email_or_id, int):
            account = self.get_account_by_id(email_or_id)
        else:
            account = self.get_account_by_email(email_or_id)

        if not account:
            print("Account not found.")
            return

        print(f"Account ID: {account['id']}")
        print(f"Email: {account['email']}")
        print(f"Sent Messages: {account['sent_messages']}")
        print(f"Received Messages: {account['received_messages']}")

# Инициализация базы данных
initialize_database()
