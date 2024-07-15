from commands.handler import CommandHandler
from database import get_user_by_email, add_user, delete_user, list_users, save_message, get_message, get_user_stats, list_incoming_emails, list_outgoing_emails, get_email_by_id

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
    global current_user
    if current_user:
        print("Ви вже увійшли в систему")
        return
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    if user['password'] != password:
        print("Неправильний пароль")
        return
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
    global current_user
    user = get_user_by_email(email)
    if not user:
        print("Користувача з такою електронною поштою не знайдено")
        return
    confirmation = input(f"Ви впевнені, що хочете видалити аккаунт {user['name']}? (так/ні): ")
    if confirmation.lower() != 'так':
        print("Видалення відмінено")
        return
    delete_user(email)
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

current_user = None

@handler.command('send_email')
def send_email(recipient_email, *args):
    global current_user
    if not current_user:
        print("Ви не увійшли в систему")
        return
    recipient = get_user_by_email(recipient_email)
    if not recipient:
        print("Отримувача не знайдено")
        return
    text = ' '.join(args)
    save_message(current_user['email'], recipient_email, text)
    print("Лист успішно відправлено")

@handler.command('reply_email')
def reply_email(message_id, *args):
    global current_user
    if not current_user:
        print("Спочатку увійдіть в систему")
        return
    original_message = get_message(message_id)
    if not original_message:
        print("Повідомлення не знайдено")
        return
    if original_message['receiver'] != current_user['email']:
        print("Ви не є отримувачем цього повідомлення")
        return
    text = ' '.join(args)
    save_message(current_user['email'], original_message['sender'], text, reply_to=message_id)
    print("Відповідь успішно відправлено")


@handler.command('account_info')
def account_info(identifier):
    user = get_user_by_email(identifier)
    if not user:
        print("Користувача не знайдено")
        return
    stats = get_user_stats(user['email'])
    print(f"Інформація про користувача {user['name']} ({user['email']}):")
    print(f"Відправлені повідомлення: {stats['sent']}")
    print(f"Отримані повідомлення: {stats['received']}")

@handler.command('list_inbox')
def list_inbox():
    global current_user
    if not current_user:
        print("Спочатку увійдіть в систему")
        return
    mails = list_incoming_emails(current_user['email'])
    if not mails:
        print("У вас немає вхідних листів")
        return
    for mail in mails:
        print(f"ID: {mail['id']}, Від: {mail['sender']}, Текст: {mail['text']}")

@handler.command('list_outbox')
def list_outbox():
    global current_user
    if not current_user:
        print("Спочатку увійдіть в систему")
        return
    mails = list_outgoing_emails(current_user['email'])
    if not mails:
        print("У вас немає вихідних листів")
        return
    for mail in mails:
        print(f"ID: {mail['id']}, Кому: {mail['receiver']}, Текст: {mail['text']}")

@handler.command('read_email')
def read_email(mail_id):
    global current_user
    if not current_user:
        print("Спочатку увійдіть в систему")
        return
    mail = get_email_by_id(current_user['email'], int(mail_id))
    if not mail:
        print("Лист не знайдено або у вас немає доступу до цього листа")
        return
    print(f"ID: {mail['id']}, Від: {mail['sender']}, Кому: {mail['receiver']}")
    print(f"Текст: {mail['text']}")
