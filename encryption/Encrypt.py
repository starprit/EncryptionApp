import hashlib
import base64
import os

from Cryptodome import Random
from Cryptodome.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.globalKey = hashlib.sha256(key.encode('utf-8')).digest()

    def genKey(self):
        return os.urandom(1024)

    def encrypt(self, key, raw):

        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def encryptFile(self, path):
        hashKey = hashlib.sha256(self.genKey()).digest()
        encryptKey = self.encrypt(self.globalKey, hashKey)
        print(os.stat(path).st_size)
        size = self.encrypt(hashKey, str(os.stat(path).st_size).encode())
        name = self.encrypt(hashKey, os.path.basename(path).encode())
        basename = os.path.dirname(os.path.abspath(path)) + '\\' + os.path.splitext(os.path.basename(path))[0]
        string = ''
        print(basename)

        out_file = open(str(basename + '.enc'), 'wb')  # open for [w]riting as [b]inary

        with open(path, "rb") as file:
            out_file.write(encryptKey + b'\n')
            out_file.write(size + b'\n')
            out_file.write(name + b'\n')
            while True:
                byte = file.read()
                if not byte:
                    break
                out_file.write(self.encrypt(hashKey, byte) + b'\n')

        file.close()
        out_file.close()
        os.remove(path)


    def decrypt(self, key, enc):
        # zmiany
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def decryptFile(self, path):
        file = open(path, "r")
        encryptArray = file.readlines()
        file.close()

        hashKey = self.decrypt(self.globalKey, encryptArray[0].strip('\n').encode())
        size = self.decrypt(hashKey, encryptArray[1].strip('\n').encode())
        name = self.decrypt(hashKey, encryptArray[2].strip('\n').encode())

        decPath = os.path.dirname(os.path.abspath(path)) + '\\' + name.decode()
        newFile = open(decPath, "wb")
        # write to file
        for byte in range(3, len(encryptArray)):
            newFile.write(self.decrypt(hashKey, encryptArray[byte]))

        newFile.close()
        print("Decode of a file sucess")
        os.remove(path)


    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    def unpad(self, s):
        return s[0:-s[-1]]