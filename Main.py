import os

from Encrypt import AESCipher
import timeit
print("Hello world")

file = []
file2 = []



if __name__ == '__main__':


    start = timeit.default_timer()

    # Your statements here


    key = 'siemakurwozajebanawdupe4567624//dsa5'
    cipher = AESCipher(key)
 #43.354206684931505
    cipher.encryptFile('test5.mkv')

    cipher.decryptFile('test5.encrypt')
    #
    # cipher.compare('test2.jpg', 'decoded2.rar')
    stop = timeit.default_timer()

    print (stop - start)

    #gowno


