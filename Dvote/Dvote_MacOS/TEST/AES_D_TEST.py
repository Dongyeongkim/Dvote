import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def KeyLoader():
    f = open('key.txt', 'rb'); key = f.read()
    return key

def DataLoader():
    f = open('Data.json', 'r') ; Data = f.read()
    return Data

try:
    b64 =json.loads(DataLoader())
    print(b64)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    key = KeyLoader()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), 16)
    print("The message was: ", pt)
except(ValueError, KeyError):
    print("Incorrect Decryption")
    
