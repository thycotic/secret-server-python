import os

from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


class DataProtection:

    @classmethod
    def get_master_key(cls):
        path = "masterKey.config"
        try:
            if not os.path.exists('masterKey.config'):
                master_key = b64encode(os.urandom(32)).decode('utf-8')
                open(path, "w").write(master_key)
            else:
                master_key = open(path).read()
            return  master_key
        except Exception as err:
            print(err)
            raise
    
    @classmethod
    def encrypt(cls):

DataProtection().get_master_key()