import sqlite3
import sys
import getpass
from cryptography.fernet import Fernet, InvalidToken
    

valid_number = "\nMake sure to enter a valid number."
thank_you = "\nThank you for using Password-Manager-CLI made by BelacEr"


def load_or_generate_key():
    """
    Try loading the previously generated key. If the key doesn't exist,
    it will be created and saved to a file.
    """
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

        print("\nKey created! Keep it safe.")
        return key


def encrypt_password(password: str, key: bytes) -> bytes:
    """Encrypts a password using Fernet."""
    f = Fernet(key)
    return f.encrypt(password.encode())


def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    """Decrypt a password using Fernet."""
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()


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
        encrypted_password BLOB NOT NULL
    )
""")
    connect.commit()
    connect.close()


def add_password(service, username, password, key):
    """
    Add encryptd password function.
    """
    encrypted_pw = encrypt_password(password, key)

    connect = sqlite3.connect("passwords.db")
    cursor = connect.cursor()
    cursor.execute(
    "INSERT INTO passwords (service, username, encrypted_password) VALUES (?, ?, ?)",
    (service, username, encrypted_pw))
    connect.commit()
    connect.close()
    
    print(f"\nPassword for {service} added securely!")


def show_passwords(key):
    """
    Display all passwords (decrypted) saved in the database.
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
            decrypted_pw = decrypt_password(row[3], key)
            print(f"{row[0]:<2} | {row[1]:<12} | {row[2]:<15} | {decrypted_pw}")
        print("="*50)

    except sqlite3.Error as e:
        print("\nDatabase error: {e}")
    except InvalidToken:
        print("\nDecryption failed - invalid key or corrupted data")


def find_password_by_service(service_name, key):
    """
    Function to find the password (decrypted) for the specific service.
    """
    connect = sqlite3.connect("passwords.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM passwords WHERE service = ?", (service_name,))
    row = cursor.fetchone()

    if row:
        try:
            decrypted_pw = decrypt_password(row[3], key)
            # row[3] was changed to decrypted_pw to display the password.
            print(f"\nService: {row[1]}\nUsername: {row[2]}\nPassword: {decrypted_pw}")
        except InvalidToken:
            print("\nDecryption failed - invalid key or corrupted data.")
    else:
        print(f"There's no password for {service_name}.")


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
        except (ValueError, KeyboardInterrupt, EOFError):
            print(valid_number)
            sys.exit()


def main():
    key = load_or_generate_key()    # Create the key.
    init_db()
    while True:
        show_menu()
        choice = enter_number("Enter your choice: ")

        # Menu map
        if choice == 1:
            try:
                # Ask for the service, username and input with try-except for built-in exceptions.
                service = input("\nService: ").strip()
                username = input("Username: ").strip()
                password = getpass.getpass("Password: ").strip()    # getpass so that the password is not displayed
                add_password(service, username, password, key)
            except (KeyboardInterrupt, EOFError):
                print(thank_you)
                sys.exit()

        elif choice == 2:
            show_passwords(key)

        elif choice == 3:
            try:
                # Ask for the service to search with try-except for built-in exceptions.
                service = input("Name of the service you want the password for: ").strip()
            except (KeyboardInterrupt, EOFError):
                print(thank_you)
                sys.exit()

            find_password_by_service(service, key)

        elif choice == 4:
            print(thank_you)
            break

        else:
            print(valid_number)
