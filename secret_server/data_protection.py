import os
import platform
import json 

from uuid import uuid4
from base64 import (b64encode, b64decode)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

class DataProtection:
    SALT = os.urandom(64)

    @classmethod
    def get_home_directory(cls):
        home_path = os.path.expanduser("~")
        if platform.system() is "Windows":
            home_path = os.path.join(home_path, "AppData", "Local")
            return home_path
        return home_path

    @classmethod
    def get_master_key(cls):
        path= os.path.join(cls.get_home_directory(), ".thycotic", "thycotic-python-client")
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
            return  master_key.encode("UTF-8")
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
            salt= salt,
            iterations=2145,
            backend=backend
        )
        try:
            return kdf.derive(cls.get_master_key())
        except IOError as e:
            raise IOError(e)

    @classmethod
    def encrypt(cls, data):

        salt = cls.SALT
        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(cls.get_key(salt=salt)),
            modes.GCM(iv),
            backend = default_backend()
        ).encryptor()

        try:
            ciphertext = encryptor.update(json.dumps(data).encode("UTF-8")) + encryptor.finalize()
            payload = salt + iv + encryptor.tag + ciphertext
            return b64encode(payload).decode("UTF-8")
        except Exception as e:
            raise Exception(e)

    @classmethod
    def decrypt(cls, file):
        try:
            raw = b64decode(open(file, 'r').read())
        except IOError as e:
           raise IOError(e)
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
            decrypted = (decryptor.update(ciphertext) + decryptor.finalize())
            return json.loads(decrypted.decode("UTF-8"))
        except Exception as e:
            raise Exception(e)