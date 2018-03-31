import hashlib
import base64
import os

from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(key.encode('utf-8')).digest()
    
    def genKey(self):
        return os.urandom(256)

    def encrypt(self, raw):
        #zmiany
        hashKey = hashlib.sha256(self.genKey()).digest()
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(hashKey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        #zmiany
        hashKey = hashlib.sha256(self.genKey()).digest()
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(hashKey, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    def unpad(self, s):
        return s[0:-s[-1]]
