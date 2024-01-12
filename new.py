import hashlib

string = input("Введите строку: ")

for nonce in range(10000000000):
    if hashlib.sha256(hashlib.sha256(string.encode()).hexdigest().encode() + str(nonce).encode()).hexdigest()[0:4] == "0000":
        print(nonce)
        break
