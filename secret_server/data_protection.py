# Data is stored in base64 format. Initially it was binary data
# Format used in this encryption module.
# inspired by AndiDittrich
# +--------------------+-----------------------+----------------+----------------+
# | SALT               | Initialization Vector | Auth Tag       | Payload        |
# | Used to derive key | AES GCM XOR Init      | Data Integrity | Encrypted Data |
# | 64 Bytes, random   | 16 Bytes, random      | 16 Bytes       | (N-96) Bytes   |
# +--------------------+-----------------------+----------------+----------------+
# This module doesn't take care of data persistence, it's assumed the consuming method/class will do so.
# This was done to maximize flexibility. Similar to how Encryption as a Service works
import os
import platform

from base64 import (b64encode, b64decode)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


class DataProtection:

    SALT = os.urandom(64)

    @classmethod
    def get_home_directory(cls):
        # This method gets the home directory for the user, and adds the AppData/Local dir path if it's a windows users
        # for better ACLs
        home_path = os.path.expanduser("~")
        if platform.system() is "Windows":
            home_path = os.path.join(home_path, "AppData", "Local")
            return home_path
        return home_path

    @classmethod
    def get_master_key(cls):
        # We generate a master key and store it in the user path to leverage ACL protections
        # The master key is used to derive the AES256 key using a KDF
        path = os.path.join(cls.get_home_directory(), ".thycotic", "thycotic-python-client")
        name = os.path.join(path, "masterKey.config")
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                master_key = b64encode(os.urandom(32)).decode("UTF-8")
                open(name, "w").write(master_key)
            elif not os.path.isfile(name):
                master_key = b64encode(os.urandom(32)).decode("UTF-8")
                open(name, "w").write(master_key)
            else:
                master_key = open(name).read()
            return master_key.encode("UTF-8")
        except IOError as e:
            raise IOError(e)
        except ValueError as e:
            raise ValueError(e)

    @classmethod
    def get_key(cls, salt):    
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=2145,
            backend=backend
        )
        try:
            return kdf.derive(cls.get_master_key())
        except IOError as e:
            raise IOError(e)

    @classmethod
    def encrypt(cls, data):
        # Here we initialize our Cipher and attempt to encrypt the data
        salt = cls.SALT
        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(cls.get_key(salt=salt)),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        try:
            # Encrypt and finalize the data
            ciphertext = encryptor.update(data.encode("UTF-8")) + encryptor.finalize()
            payload = salt + iv + encryptor.tag + ciphertext
            # Then we base64 encode the data and return it so it can be saved
            return b64encode(payload).decode("UTF-8")
        except Exception as e:
            raise Exception(e)

    @classmethod
    def decrypt(cls, file_name):
        # Decryption is similar, we get the filename
        try:
            # read the base64 data and decode it back to bytes
            raw = b64decode(open(file_name, 'r').read())
        except IOError as e:
            raise IOError(e)
        # slice the bytes to get the salt, iv, tag, and the ciphertext
        salt = raw[:64]
        iv = raw[64:80]
        tag = raw[80:96]
        ciphertext = raw[96:]

        decryptor = Cipher(
            algorithms.AES(cls.get_key(salt=salt)),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        try:
            # decrypt the ciphertext and return it as UTF-8
            decrypted = (decryptor.update(ciphertext) + decryptor.finalize())
            return decrypted.decode("UTF-8")
        except Exception as e:
            raise Exception(e)
