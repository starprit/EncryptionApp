import hashlib
import base64
import os

from Crypto import Random
from Crypto.Cipher import AES


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
        # print(os.stat('decoded.jpg').st_size)
        size = self.encrypt(hashKey, str(os.stat(path).st_size).encode())
        name = self.encrypt(hashKey, os.path.basename(path).encode())
        basename = os.path.splitext(os.path.basename(path))[0]
        string = ''
        print(hashKey)

        with open(path, "rb") as file:
            flag = True
            while True:
                byte = file.read(1)
                if not byte:
                    break
                if flag:
                    string = str(ord(byte))
                    flag = False
                else:
                    string += ";" + str(ord(byte))
        encryptString = self.encrypt(hashKey, string.encode())

        with open(str(basename + '.encrypt'), 'w') as f:
            string = encryptKey.decode() + '\n' + \
                     size.decode() + '\n' + \
                     name.decode() + '\n' + \
                     encryptString.decode()
            f.write(string)
            print("Encrypt of a file success")

    def decrypt(self, key, enc):
        # zmiany
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def decryptFile(self, path):

        file = open(path, "r")
        encryptArray = file.readlines()
        # print("Name of the file: ", fo.name)
        hashKey = self.decrypt(self.globalKey, encryptArray[0].strip('\n').encode())
        size = self.decrypt(hashKey, encryptArray[1].strip('\n').encode())
        name = self.decrypt(hashKey, encryptArray[2].strip('\n').encode())
        decodeString = self.decrypt(hashKey, encryptArray[3].encode()).decode().split(';')

        print(hashKey)
        parse = [int(i) for i in decodeString]
        decPath = name.decode().replace('test2', 'decoded')
        newFile = open(decPath, "wb")
        # write to file
        for byte in parse:
            newFile.write(byte.to_bytes(1, byteorder='big'))

        print()
        print(size.decode(), os.stat(decPath).st_size)
        print("Decode of a file sucess")
        print()
        print(os.stat('decoded.jpg').st_size)
        print(os.path.getsize('decoded.jpg'))
        print(os.path.getsize('test2.jpg'))

    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    def unpad(self, s):
        return s[0:-s[-1]]
