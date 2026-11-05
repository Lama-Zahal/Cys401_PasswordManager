# CS401- cybersecurity project-Secure Password Manager
a small secure password manager made using python. It stores accounts passwords in single encrypted vault, generates strong random, and warns about weak or reused passwords.

## Features
- One **master password** unlocks the vault and is never stored anywhere. The program generates a 16 byte random salt when the vault is created and a key is derived from the password and the salt.
- **Encrypted vault file** entries are encrypted using AES via Fernet library.
- **Password generator** is done using python secret module
- **Strength checker** rates the password strength as weak, medium, strong
- **Reuse detector** flag passwords used more than once on diferent websites
- **Web Interface** built with streamlit

## Project Structure
password-manager/

├── crypto_utils.py    # key derivation, encrypt, decrypt

├── vault.py           # create, unlock, save, add/edit/delete entries

├── generator.py       # password generator, strength checker, reuse detector

├── ui.py              # Streamlit interface

├── requirements.txt   # libraries needed

├── .gitignore         # keeps vault files out of GitHub

└── README.md

## How to run
Python 3.9 or newer
in the terminal
- pip install -r requirements.txt
- streamlit run ui.py

## How it works
- First run: you choose a master password. The program creates a random salt, derives an encryption key from the password and salt, and saves an empty encrypted vault.
- Unlock: you type the master password. The program reads the salt from the file, derives the key again and tries to decrypt. If decryption succeeds, the password was correct. If it fails, the password was wrong.
- Use: entries are held in memory while the vault is unlocked.
- Save: every add, edit or delete encrypts the whole list again and overwrites the file.

## Security design
- Fernet (AES + HMAC) -->	A reviewed library, so we do not invent our own encryption. It also detects tampering.
- PBKDF2-HMAC-SHA256, 600,000 iterations -->	Deliberately slow, so guessing the master password is expensive for an attacker.
- Random 16-byte salt -->	Gives every vault a different key and defeats precomputed lookup tables.
- secrets instead of random	secrets --> is designed for security; random is predictable.
- No stored master password or hash	--> A wrong password produces a wrong key, and decryption fails. That failure is the login check.
