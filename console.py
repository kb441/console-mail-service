def main():
    mail_system = MailSystem()

    while True:
        print("\n1. Add Account")
        print("2. Send Message")
        print("3. Reply to Message")
        print("4. Get Account Info")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            email = input("Enter email: ")
            mail_system.add_account(email)

        elif choice == '2':
            sender_email = input("Enter sender email: ")
            receiver_email = input("Enter receiver email: ")
            content = input("Enter message content: ")
            mail_system.send_message(sender_email, receiver_email, content)

        elif choice == '3':
            message_id = int(input("Enter message ID: "))
            sender_email = input("Enter sender email: ")
            content = input("Enter message content: ")
            mail_system.reply_to_message(message_id, sender_email, content)

        elif choice == '4':
            email_or_id = input("Enter email or account ID: ")
            try:
                email_or_id = int(email_or_id)
            except ValueError:
                pass
            mail_system.get_account_info(email_or_id)

        elif choice == '5':
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
