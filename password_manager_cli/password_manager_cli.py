import sqlite3
import sys
import getpass

valid_number = "\nMake sure to enter a valid number."
thank_you = "\nThank you for using Password-Manager-CLI made by BelacEr"


def init_db():
    """
    Function to initialize the database.
    """
    connect = sqlite3.connect("passwords.db")
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")
    connect.commit()
    connect.close()


def add_password(service, username, password):
    """
    Add password function.
    """
    connect = sqlite3.connect("passwords.db")
    cursor = connect.cursor()
    cursor.execute(
    "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
    (service, username, password)
    )
    connect.commit()
    connect.close()
    
    print(f"\nPassword for {service} added!")


def show_passwords():
    """
    Display all passwords saved in the database.
    """
    try:
        connect = sqlite3.connect("passwords.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM passwords")
        rows = cursor.fetchall()
        connect.close()

        if not rows:
            print("\nNo password saved yet.")
            return
        
        # Show the table
        print("\n" + "="*50)
        print("ID | Service      | Username       | Password")
        print("="*50)
        for row in rows:
            print(f"{row[0]:<2} | {row[1]:<12} | {row[2]:<15} | {row[3]}")
        print("="*50)

    except sqlite3.Error as e:
        print("\nDatabase error: {e}")


def find_password_by_service(service_name):
    """
    Function to find the password for the specific service.
    """
    connect = sqlite3.connect("passwords.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM passwords WHERE service = ?", (service_name,))
    row = cursor.fetchone()

    if row:
        print(f"\nService: {row[1]}\nUsername: {row[2]}\nPassword: {row[3]}")
    else:
        print(f"There's no password for {service_name}")


def show_menu():
    print("""
    ==== PASSWORD MANAGER CLI ====
1. Create password
2. Show all passwords
3. Find password by service name 
4. Exit
    """)


def enter_number(prompt):
    """
    Function that only accepts integers, used to the menu with try-except for built-in exceptions.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(valid_number)
            sys.exit()
        except KeyboardInterrupt:
            print(thank_you)
            sys.exit()
        except EOFError:
            print(thank_you)
            sys.exit()


def main():
    init_db()
    while True:
        show_menu()
        choice = enter_number("Enter your choice: ")

        # Temporal menu map
        if choice == 1:
            try:
                # Ask for the service, username and input with try-except for built-in exceptions.
                service = input("\nService: ").strip()
                username = input("Username: ").strip()
                password = getpass.getpass("Password: ").strip()    # getpass so that the password is not displayed
            except KeyboardInterrupt:
                print(thank_you)
                sys.exit()
            except EOFError:
                print(thank_you)
                sys.exit()

            add_password(service, username, password)

        elif choice == 2:
            show_passwords()

        elif choice == 3:
            try:
                # Ask for the service to search with try-except for built-in exceptions.
                service = input("Name of the service you want the password for: ").strip()
            except KeyboardInterrupt:
                print(thank_you)
                sys.exit()
            except EOFError:
                print(thank_you)
                sys.exit()

            find_password_by_service(service)

        elif choice == 4:
            print(thank_you)
            break

        else:
            print(valid_number)


# Run the program
if __name__ == '__main__':
    main()