import os

from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


class DataProtection:

    @classmethod
    def get_master_key(cls):
        try:
            if not os.path.exists('masterKey.config'):
                random = os.urandom(32)
                master_key = b64encode(random)
                print(master_key)
        except:
            master_key

DataProtection().get_master_key()