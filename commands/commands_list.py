from commands.handler import CommandHandler
from database import get_user_by_email, add_user, delete_user, list_users

handler = CommandHandler()

@handler.command('register')
def register(name, email, password, password_confirm):
    if password != password_confirm:
        print("Паролі не збігаються")
        return
    if get_user_by_email(email):
        print("Користувач з такою електронною поштою вже існує")
        return
    add_user(name, email, password)
    print("Реєстрація пройшла успішно")

@handler.command('login')
def login(email, password):
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    if user['password'] != password:
        print("Неправильний пароль")
        return
    global current_user
    current_user = user
    print(f"Ласкаво просимо, {user['name']}")

@handler.command('logout')
def logout():
    global current_user
    if not current_user:
        print("Ви не увійшли в систему")
        return
    print(f"До побачення, {current_user['name']}")
    current_user = None

@handler.command('delete_account')
def delete_account(email):
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    confirmation = input(f"Ви впевнені, що хочете видалити аккаунт {user['name']}? (так/ні): ")
    if confirmation.lower() != 'так':
        print("Видалення відмінено")
        return
    delete_user(email)
    global current_user
    if current_user and current_user['email'] == email:
        current_user = None
    print("Аккаунт успішно видалено")

@handler.command('list_accounts')
def list_accounts():
    users = list_users()
    if not users:
        print("Немає зареєстрованих користувачів")
        return
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user['name']} - {user['email']}")

# Змінна для зберігання поточного користувача
current_user = None



from commands.handler import CommandHandler
from database import get_user_by_email, add_user, delete_user, list_users, save_message, get_message, list_messages, get_user_stats
import json

handler = CommandHandler()

@handler.command('register')
def register(name, email, password, password_confirm):
    if password != password_confirm:
        print("Паролі не збігаються")
        return
    if get_user_by_email(email):
        print("Користувач з такою електронною поштою вже існує")
        return
    add_user(name, email, password)
    print("Реєстрація пройшла успішно")

@handler.command('login')
def login(email, password):
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    if user['password'] != password:
        print("Неправильний пароль")
        return
    global current_user
    current_user = user
    print(f"Ласкаво просимо, {user['name']}")

@handler.command('logout')
def logout():
    global current_user
    if not current_user:
        print("Ви не увійшли в систему")
        return
    print(f"До побачення, {current_user['name']}")
    current_user = None

@handler.command('delete_account')
def delete_account(email):
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    confirmation = input(f"Ви впевнені, що хочете видалити аккаунт {user['name']}? (так/ні): ")
    if confirmation.lower() != 'так':
        print("Видалення відмінено")
        return
    delete_user(email)
    global current_user
    if current_user and current_user['email'] == email:
        current_user = None
    print("Аккаунт успішно видалено")

@handler.command('list_accounts')
def list_accounts():
    users = list_users()
    if not users:
        print("Немає зареєстрованих користувачів")
        return
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user['name']} - {user['email']}")

@handler.command('send_email')
def send_email(recipient_email, text):
    if not current_user:
        print("Ви не увійшли в систему")
        return
    recipient = get_user_by_email(recipient_email)
    if not recipient:
        print("Отримувача не знайдено")
        return
    save_message(current_user['email'], recipient_email, text)
    print("Лист успішно відправлено")

@handler.command('reply_email')
def reply_email(message_id, text):
    if not current_user:
        print("Ви не увійшли в систему")
        return
    original_message = get_message(message_id)
    if not original_message or original_message['recipient'] != current_user['email']:
        print("Повідомлення не знайдено або ви не є отримувачем")
        return
    save_message(current_user['email'], original_message['sender'], text, reply_to=message_id)
    print("Відповідь успішно відправлено")

@handler.command('account_info')
def account_info(identifier):
    if '@' in identifier:
        user = get_user_by_email(identifier)
    else:
        user = get_user_by_id(identifier)
    if not user:
        print("Користувача не знайдено")
        return
    stats = get_user_stats(user['email'])
    print(f"Інформація про користувача {user['name']} ({user['email']}):")
    print(f"Відправлені повідомлення: {stats['sent']}")
    print(f"Отримані повідомлення: {stats['received']}")

# Змінна для зберігання поточного користувача
current_user = None

# Функції для роботи з базою даних
def save_message(sender, recipient, text, reply_to=None):
    with open('database.json', 'r+') as file:
        data = json.load(file)
        message_id = len(data['messages']) + 1
        data['messages'].append({
            'id': message_id,
            'sender': sender,
            'recipient': recipient,
            'text': text,
            'reply_to': reply_to
        })
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def get_message(message_id):
    with open('database.json', 'r') as file:
        data = json.load(file)
        for message in data['messages']:
            if message['id'] == message_id:
                return message
    return None

def list_messages():
    with open('database.json', 'r') as file:
        data = json.load(file)
        return data['messages']

def get_user_stats(email):
    with open('database.json', 'r') as file:
        data = json.load(file)
        sent = sum(1 for message in data['messages'] if message['sender'] == email)
        received = sum(1 for message in data['messages'] if message['recipient'] == email)
        return {'sent': sent, 'received': received}
