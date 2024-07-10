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
