import json
import os
from cryptography.fernet import InvalidToken
from crypto_utils import keySalt, deriveKey, encrypt, decrypt

VaultFile = "vault.dat" #the vault file name

class Vault: 
    def __init__(self, path = VaultFile): 
        self.path = path
        self.key = None
        self.salt = None
        self.entries: [] #innitialize empty list to store passwrod info: site, username, password

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def createVault(self, masterPassword: str):
        """First-time setup create a new empty vault that is encrypted"""
        self.salt = keySalt() #generate a new salt
        self.key = deriveKey(masterPassword, self.salt) #derives the key using the typed password and the salt generated
        self.entries = []
        self.save()

    def unlockVault(self, masterPassword: str) ->bool:
        """Returns true if the master password is correct--> used to unlock the vault"""
        with open(self.path, "rb") as file:
            data = file.read #open file in read binary mode and reads the content as bytes
        salt, token = data[:16], data[16:] #salt is the first 16 bytes, everything after is the data named as token
        key = deriveKey(masterPassword, salt) #derive the key by using the password and the salt
        try: 
            plaintext = decrypt(token, key) #decrypt the encrypted data in the file
        except InvalidToken:
            return False
        self.salt, self.key = salt, key
        self.entries = json.loads(plaintext.decode())
        return True

    def saveVault(self): 
        """Converts password entries to JSON text then encrypts it and 
        then writes salt and the entries (tokens) to the file
        """
        token = encrypt(json.dumps(self.entries).encode(), self.key)
        with open(self.path, "wb") as file: #writes in bytes
            file.write(self.salt + token) #write sault first in the file then the entries

    def addPassEntry(self, site, username, password):
        """Writes a new password entry to the file and saves it"""
        self.entries.append(
            {"site":site, "username": username, "password": password}
        )
        self.save()

    def updatePassEntry(self, index, site, username, password): 
        """Replaces an entry in the file at a certain position then saves it"""
        self.entries[index] = {
            "site":site, "username":username, "password":password
        }
        self.save()

    def deletePassEntry(self, index):
        """Deletes an entry at a certain position the saves it"""
        del self.entries[index]
        self.save()


