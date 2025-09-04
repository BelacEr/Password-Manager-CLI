# Password-Manager-CLI

**Password-Manager-CLI** is a simple command-line tool to securely store and manage your passwords using encryption and a local SQLite database. Created by **BelacEr**, this tool encrypts your credentials using [Fernet symmetric encryption](https://cryptography.io/en/latest/fernet/), ensuring your data remains private and secure.

---

## 🔐 Features

* Add and encrypt passwords for your services
* Decrypt and view stored passwords
* Search for a password by service name
* All data stored locally in an SQLite database
* One-time key generation for encryption/decryption

---

## 📦 Requirements

* Python 3.7+
* [`cryptography`](https://pypi.org/project/cryptography/)

Install the required library using pip:

```bash
pip install cryptography
```

---

## 🚀 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Password-Manager-CLI.git
cd Password-Manager-CLI
```

2. **Run the CLI tool**

```bash
python3 password_manager.py
```

> On first run, a `secret.key` file will be created. This file is essential for encrypting and decrypting your passwords. **Keep it safe.** If you lose this file, you will not be able to decrypt your saved passwords.

---

## 📋 Menu Options

When running the tool, you’ll be presented with the following options:

```
==== PASSWORD MANAGER CLI ====
1. Create password
2. Show all passwords
3. Find password by service name 
4. Exit
```

### 1. Create password

Enter the service name, username, and password. The password will be encrypted and stored securely.

### 2. Show all passwords

Lists all stored passwords, decrypting them on the fly.

### 3. Find password by service name

Search for a specific service and view its credentials.

### 4. Exit

Closes the application safely.

---

## 🛑 Important Notes

* The encryption key is stored in `secret.key`. Do **not delete or share** this file.
* All passwords are stored in `passwords.db` using SQLite.
* Passwords are **not** recoverable without the original key file.


## 🧑‍💻 Author

Made with care by **BelacEr**.