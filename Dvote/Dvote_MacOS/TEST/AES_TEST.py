import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def DataSaver(result):
    f = open("Data.json",'w'); f.write(result)
    f.flush(); f.close()
def KeySaver(key):
    f = open("key.txt",'wb');f.write(key)
    f.flush();f.close()
data =input("Input Your Data").encode(); print(data)
key = get_random_bytes(16); print (key)
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, 16))
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'iv':iv, 'ciphertext': ct})
print(result)

DataSaver(result)

KeySaver(key)


