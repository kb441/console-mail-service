class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, handler):
        self.commands[command_name] = handler

    def execute_command(self, command_name, *args):
        if command_name in self.commands:
            try:
                self.commands[command_name](*args)
            except Exception as e:
                print(f"Помилка виконання команди '{command_name}': {e}")
        else:
            print(f"Команда '{command_name}' не розпізнається")

    def command(self, name):
        def decorator(func):
            self.register_command(name, func)
            return func
        return decorator