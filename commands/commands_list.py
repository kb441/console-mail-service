from commands.handler import CommandHandler

handler = CommandHandler()

@handler.command('greet')
def greet(name):
    print(f"Hello, {name}!")

@handler.command('add')
def add(a, b):
    try:
        result = float(a) + float(b)
        print(f"The result of adding {a} and {b} is {result}")
    except ValueError:
        print("Both arguments must be numbers")