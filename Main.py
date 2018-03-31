import hashlib
import os
import sys
import base64
from Crypto import Random
from Crypto.Cipher import AES

print("Hello world")

file = []

class AESCipher(object):
    def __init__(self, key):
        self.BS = 16
        # self.cipher = AES.new(key, AES.MODE_ECB)
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[16:]))

    def _pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS).encode()

    def _unpad(self, s):
        return s[0:-s[-1]]

if __name__ == '__main__':

    with open("test2.jpg", "rb") as f:
        # byte = f.read(1)
        while True:
            # Do stuff with byte.
            byte = f.read(1)
            if not byte:
                break
            file.append(ord(byte))
            # print(file)

    print(file)


    # key = os.urandom(16)
    key = 'siemakurwozajebanawdupe4567624//dsa5'

    cipher = AESCipher(key)
    text = ''
    flag = True
    for x in file:
        if flag:
            text = str(x)
            flag = False
        else:
            text += ";" + str(x)

    print(text)
    encrypted = cipher.encrypt(text.encode())
    print(encrypted)

    decrypted = cipher.decrypt(encrypted)
    print("decrypt")
    print(decrypted.decode())
    print(decrypted.decode() == text)

    final = decrypted.decode().split(';')
    results = [int(i) for i in final]
    print(results)

    with open('test.encrypt', 'w') as f:
        f.write(encrypted.decode())

    newFile = open("decrypt.jpg", "wb")
    # write to file
    for byte in results:
        newFile.write(byte.to_bytes(1, byteorder='big'))
