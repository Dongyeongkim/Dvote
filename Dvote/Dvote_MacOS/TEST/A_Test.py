import json
from base64 import b64decode
from base64 import b64encode
from ecdsa import VerifyingKey, BadSignatureError



def DataLoader():
    f = open('Data.json', 'r') ; Data = f.read()
    return Data

    
b64 = json.loads(DataLoader())

iv = b64decode(b64['iv']); print(iv)
ct = b64decode(b64['ciphertext']); print(ct)
S_iv = b64decode(b64['S_iv']); print(S_iv)
S_ct = b64decode(b64['S_ct']); print(S_ct)

