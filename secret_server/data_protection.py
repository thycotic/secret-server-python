import os

from base64 import (b64encode, b64decode)
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
                master_key = b64encode(os.urandom(32))
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
        try:
            return kdf.derive(cls.get_master_key())
        except Exception as e:
            raise Exception(e.message)

    @classmethod
    def encrypt(cls, data):
        if type(data) is dict:
            data = str(data)

        salt = cls.SALT
        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(cls.get_key(salt=salt)),
            modes.GCM(iv),
            backend = default_backend()
        ).encryptor()

        try:
            ciphertext = encryptor.update(data) + encryptor.finalize()
            tag = encryptor.tag
        except Exception as e:
            raise Exception(e.message)
        
        payload = salt + iv + tag + ciphertext

        try:
            open("test.json" , "w").write(b64encode(payload))
        except IOError as e:
            raise IOError("Couldn't Save creds.json: " + e.message)

    @classmethod
    def decrypt(cls):
        try:
            raw = b64decode(open('test.json', 'r').read())
        except IOError as e:
           "Couldn't Open creds.json: " + e.message
           raise
        #slice the bytes to get the salt, iv, tag, and the ciphertext
        salt =  raw[:64]
        iv = raw[64:80]
        tag = raw[80:96]
        ciphertext = raw[96:]

        decryptor = Cipher(
            algorithms.AES(cls.get_key(salt=salt)),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        try:
            return decryptor.update(ciphertext) + decryptor.finalize()
        except Exception as e:
            raise Exception(e.message)