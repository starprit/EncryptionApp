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

        out_file = open(str(basename + '.encrypt'), 'wb')  # open for [w]riting as [b]inary

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
                # else:
                #     string += ";" + str(ord(byte))
        # encryptString = self.encrypt(hashKey, string.encode())

        # with open(str(basename + '.encrypt'), 'w') as f:
        #     string = encryptKey.decode() + '\n' + \
        #              size.decode() + '\n' + \
        #              name.decode() + '\n' + \
        #              encryptString.decode()
        #     f.write(string)
        #     print("Encrypt of a file success")
        out_file.close()
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
        # print("Name of the file: ", fo.name)

        # with open(path, "rb") as f:
        #     while True:
        #         byte = file.read(512)
        #         if not byte:
        #             break
        #         out_file.write(self.encrypt(hashKey, byte) + b'\n')
        #
        # f.close()


        hashKey = self.decrypt(self.globalKey, encryptArray[0].strip('\n').encode())
        size = self.decrypt(hashKey, encryptArray[1].strip('\n').encode())
        name = self.decrypt(hashKey, encryptArray[2].strip('\n').encode())
        # decodeString = self.decrypt(hashKey, encryptArray[3].encode()).decode().split(';')

        print(hashKey)
        # parse = [int(i) for i in decodeString]
        decPath = name.decode().replace('test', 'decoded')
        newFile = open(decPath, "wb")
        # write to file
        for byte in range(3, len(encryptArray)):
            newFile.write(self.decrypt(hashKey, encryptArray[byte]))
            print("yes")
            # newFile.write(byte.to_bytes(1, byteorder='big'))

        newFile.close()
        print()
        print(int(size.decode()) == os.stat(decPath).st_size)
        print(size.decode(), os.stat(decPath).st_size)
        print("Decode of a file sucess")
        print()


    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    def unpad(self, s):
        return s[0:-s[-1]]