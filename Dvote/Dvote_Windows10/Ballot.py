import json; import sys
from base64 import b64encode
from base64 import b64decode
from ecdsa import SigningKey
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def DataSaver(result):
    f = open("Voted_Ballot/Data.json",'w'); f.write(result)
    f.flush(); f.close()
def KeySaver(key):
    f = open("AES_Key/key.txt",'wb');f.write(key)
    f.flush();f.close()

def DataLoader():
    f = open("Voted_Ballot/Data.json", 'r') ; Data = f.read()
    return Data


data = input("Select Your Candidate Between 1 to 5")
try:
    if(int(data)>5):
        print("This is Unvaild Value")
        sys.exit(0)
    elif(int(data)<1):
        print("This is Unvaild Value")
        sys.exit(0)
    else:
         pass
         

except ValueError:
    print("This is Unvaild Value")
    sys.exit(0)
    
data = str(data); data = ("THE CHOICE OF BALLOT IS"+data+".").encode('utf-8')
key = get_random_bytes(16); print("Your AES-128 bit Encryption Key is Saved in AES_Key folder") 
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, 16))
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'iv':iv, 'ciphertext': ct})

DataSaver(result)

KeySaver(key)

b64 =json.loads(DataLoader()); 
iv = b64decode(b64['iv']); print(iv)
ct = b64decode(b64['ciphertext']); print(ct); K = open("PrKey/PrKey.pem")
sk = SigningKey.from_pem(K.read())
Sig_iv = sk.sign(iv); Sig_ct = sk.sign(ct)
print(Sig_iv,Sig_ct)

Sig_iv = b64encode(Sig_iv).decode('utf-8')
Sig_ct = b64encode(Sig_ct).decode('utf-8')
iv = b64encode(iv).decode('utf-8'); ct = b64encode(ct).decode('utf-8') 
result = json.dumps({'iv':iv,'ciphertext':ct,'S_iv':Sig_iv,'S_ct':Sig_ct})
DataSaver(result)






