import os

from base64 import b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


class DataProtection:
    SALT = os.urandom(64)
    FILE_Path = "creds.json"

    @classmethod
    def get_master_key(cls):
        path = "masterKey.config"
        try:
            if not os.path.exists(path):
                master_key = b64encode(os.urandom(32)).decode('UTF-8')
                open(path, "w").write(master_key)
            else:
                master_key = open(path).read()
            return  master_key
        except Exception as err:
            print(err)
            raise

    @classmethod
    def get_key(cls, salt):
        # derive key from master key        
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt= salt,
            iterations=2145,
            backend=backend
        )
        return kdf.derive(b64encode(cls.get_master_key()))

    @classmethod
    def encrypt(cls, data):
        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(cls.get_key(salt=cls.SALT)),
            modes.GCM(iv),
            backend = default_backend()
        ).encryptor()

        ciphertext = encryptor.update(data) + encryptor.finalize()


# # DataProtection().get_master_key()

# print(DataProtection().get_key())