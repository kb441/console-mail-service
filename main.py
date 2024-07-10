from commands.commands_list import handler

print("Введіть команди (введіть 'exit', щоб вийти):")
while True:
    command_input = input("> ").strip()
    if command_input.lower() == 'exit':
        break
    parts = command_input.split()
    if len(parts) == 0:
        continue
    command_name = parts[0]
    args = parts[1:]
    handler.execute_command(command_name, *args)