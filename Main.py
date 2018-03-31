from Encrypt import AESCipher

print("Hello world")

file = []



if __name__ == '__main__':

    with open("test2.jpg", "rb") as f:
        # byte = f.read(1)
        while True:
            # Do stuff with byte.
            byte = f.read(1)
            if not byte:
                break
            # print(ord(byte))
            file.append(ord(byte))
            # print(file)

    print(file)

    key = 'siemakurwozajebanawdupe4567624//dsa5'

    cipher = AESCipher()
    # key = cipher.genKey()
    print(key)
    text = ''
    flag = True
    for x in file:
        if flag:
            text = str(x)
            flag = False
        else:
            text += ";" + str(x)

    print(text)
    encrypted = cipher.encrypt(key, text.encode())
    print(encrypted)

    decrypted = cipher.decrypt(key, encrypted)
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
