import os

from Encrypt import AESCipher

print("Hello world")

file = []



if __name__ == '__main__':
    key = 'siemakurwozajebanawdupe4567624//dsa5'
    cipher = AESCipher(key)

    cipher.encryptFile('test2.jpg')
    cipher.decryptFile('test2.encrypt')


    # with open("test2.jpg", "rb") as f:
    #     # byte = f.read(1)
    #     print(os.stat('test2.jpg').st_size)
    #     # os.remove('test2 — kopia.jpg')
    #     while True:
    #         # Do stuff with byte.
    #         byte = f.read(1)
    #         if not byte:
    #             break
    #         # print(ord(byte))
    #         file.append(ord(byte))
    #         # print(file)
    #
    # print(file)
    #
    # key = 'siemakurwozajebanawdupe4567624//dsa5'
    #
    # cipher = AESCipher(key)
    # # key = cipher.genKey()
    # print(key)
    # text = ''
    # flag = True
    # for x in file:
    #     if flag:
    #         text = str(x)
    #         flag = False
    #     else:
    #         text += ";" + str(x)
    #
    # path = ''
    #
    # print(text)
    # encrypted = cipher.encrypt(path) #, text.encode())
    # print(encrypted)
    #
    # decrypted = cipher.decrypt(key, encrypted)
    # print("decrypt")
    # print(decrypted.decode())
    # print(decrypted.decode() == text)
    #
    # final = decrypted.decode().split(';')
    # results = [int(i) for i in final]
    # print(results)
    #
    # with open('test.encrypt', 'w') as f:
    #     f.write(encrypted.decode())
    #
    # newFile = open("decrypt.jpg", "wb")
    # # write to file
    # for byte in results:
    #     newFile.write(byte.to_bytes(1, byteorder='big'))
