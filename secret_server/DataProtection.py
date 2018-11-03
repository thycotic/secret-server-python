# Data is stored in base64 format. Initially it was binary data
# Format used in this encryption module.
# inspired by AndiDittrich
# +--------------------+-----------------------+----------------+----------------+
# | SALT               | Initialization Vector | Auth Tag       | Payload        |
# | Used to derive key | AES GCM XOR Init      | Data Integrity | Encrypted Data |
# | 64 Bytes, random   | 16 Bytes, random      | 16 Bytes       | (N-96) Bytes   |
# +--------------------+-----------------------+----------------+----------------+
# This module doesn't take care of data persistence, it's assumed the consuming method/class/package will do so.
# This was done to maximize flexibility. Similar to how Encryption as a Service works

import platform

from os import (urandom, path, makedirs, remove)
from base64 import (b64encode, b64decode)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


class DataProtection:

    SALT = urandom(64)

    @classmethod
    def home_path(cls):
        # This method gets the home directory for the user, and adds the AppData/Local dir path if it's a windows users
        # for better ACLs
        home_path = path.expanduser("~")
        if platform.system() is "Windows":
            home_path = path.join(home_path, "AppData", "Local")
            return home_path
        return home_path

    @classmethod
    def master_key(cls):
        # We generate a master key and store it in the user path to leverage ACL protections
        # The master key is used to derive the AES256 key using a KDF
        full_path = path.join(cls.home_path(), ".thycotic", "thycotic-python-client")
        file_name = path.join(full_path, "masterKey.config")
        try:
            if not path.exists(full_path):
                makedirs(full_path)
                master_key = b64encode(urandom(32)).decode("UTF-8")
                open(file_name, "w").write(master_key)
            elif not path.isfile(file_name):
                master_key = b64encode(urandom(32)).decode("UTF-8")
                open(file_name, "w").write(master_key)
            else:
                master_key = open(file_name).read()
            return master_key.encode("UTF-8")
        except IOError as e:
            raise IOError(e)
        except ValueError as e:
            raise ValueError(e)

    @classmethod
    def aes_key(cls, salt):
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=2145,
            backend=backend
        )
        try:
            return kdf.derive(cls.master_key())
        except IOError as e:
            raise IOError(e)

    @classmethod
    def encrypt(cls, data):
        # Here we initialize our Cipher and attempt to encrypt the data
        salt = cls.SALT
        iv = urandom(16)
        encryptor = Cipher(
            algorithms.AES(cls.aes_key(salt=salt)),
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
            bytes_data = b64decode(open(file_name, 'r').read())
        except IOError as e:
            raise IOError(e)
        # slice the bytes to get the salt, iv, tag, and the ciphertext
        salt = bytes_data[:64]
        iv = bytes_data[64:80]
        tag = bytes_data[80:96]
        ciphertext = bytes_data[96:]
        # initialize our decryptor
        decryptor = Cipher(
            algorithms.AES(cls.aes_key(salt=salt)),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        try:
            # decrypt the ciphertext and return it as UTF-8
            decrypted = (decryptor.update(ciphertext) + decryptor.finalize())
            return decrypted.decode("UTF-8")
        except Exception as e:
            raise Exception(e)

    @classmethod
    def remove_master_key(cls):
        full_path = path.join(cls.home_path(), ".thycotic", "thycotic-python-client")
        file_name = path.join(full_path, "masterKey.config")
        try:
            if not path.exists(full_path):
                return
            elif not path.isfile(file_name):
                return
            else:
                remove(file_name)
            return
        except IOError as e:
            raise IOError(e)
        except ValueError as e:
            raise ValueError(e)
