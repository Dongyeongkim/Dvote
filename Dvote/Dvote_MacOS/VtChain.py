import hashlib;import json
from time import time; from urllib.parse import urlparse
from uuid import uuid4; from ecdsa import VerifyingKey, BadSignatureError
import requests; from flask import Flask, jsonify, request
from base64 import b64decode; from base64 import b64encode

def DataLoader():
    f = open('Data.json', 'r') ; Data = f.read()
    return Data

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        
    def DataLoader(self):
        f = open('Data.json', 'r') ; Data = f.read()
        return Data

    def register_node(self, address):
        # Add New Node 

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # URL
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
  

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
    

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # RePlace...
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self,proof,SE_Ballot,E_Ballot,SIV, IV, previous_hash):
        Vlog = list(self.chain); VVlog = self.current_transactions
        if(Vlog == []):
            pass
                   
        else:
            last_block = self.last_block; previous_hash = self.hash(last_block)
            SE_Ballot = VVlog[0]; E_Ballot = VVlog[1];
            SIV = VVlog[2]; IV = VVlog[3]
        
        block = {'index': len(self.chain) + 1,'timestamp': time(),
                    'E_Ballot':E_Ballot,'IV':IV,
                    'SE_Ballot':SE_Ballot,'SIV':SIV,'proof': proof,
                    'previous_hash': previous_hash or self.hash(self.chain[-1]),
                 }
        self.current_transactions = []
        self.chain.append(block)
        
        return block

    def new_transaction(self, SE_Ballot, E_Ballot, SIV, IV):
        self.current_transactions.append(SE_Ballot)
        self.current_transactions.append(E_Ballot)
        self.current_transactions.append(SIV)
        self.current_transactions.append(IV)

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]
   

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, SE_Ballot, E_Ballot, SIV, IV):
        V_Log = self.current_transactions; print(V_Log)
        try:
            proof = 0; f = open("PuKey/PuKey"+str(proof)+".pem","rb");
            V_key = VerifyingKey.from_pem(f.read())
            while self.valid_proof(SE_Ballot, E_Ballot,SIV, IV, V_key) is False:
                proof += 1; print(proof);
                f = open("PuKey/PuKey"+str(proof)+".pem","rb")
                V_key = VerifyingKey.from_pem(f.read())
            return proof
        except FileNotFoundError:
            return False

    @staticmethod
    def valid_proof(SE_Ballot, E_Ballot, SIV, IV, V_Key):
        try:
            SE_Ballot = b64decode(SE_Ballot);E_Ballot = b64decode(E_Ballot);
            SIV = b64decode(SIV);IV= b64decode(IV);
            print(V_Key.verify(SE_Ballot, E_Ballot))
            print(V_Key.verify(SIV,IV))
            print("Signature is Authentic")
        except BadSignatureError:
            print("Signature is Not Authentic")
            return False
        

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Here Need To get Some Log....
    Vlog = blockchain.chain; print(Vlog)
    VVlog = blockchain.current_transactions
    if(Vlog == []):
        K = blockchain.DataLoader(); b64 = json.loads(K)
        IV = b64decode(b64['iv']);IV = b64encode(IV).decode('utf-8')
        E_Ballot = b64decode(b64['ciphertext']); E_Ballot = b64encode(E_Ballot).decode('utf-8')
        SIV = b64decode(b64['S_iv']); SIV = b64encode(SIV).decode('utf-8')
        SE_Ballot = b64decode(b64['S_ct']); SE_Ballot = b64encode(SE_Ballot).decode('utf-8')
        print(type(SIV),type(IV),type(E_Ballot),type(SE_Ballot))
        print(SIV+","+IV+","+E_Ballot+","+SE_Ballot)
        previous_hash = "D9B749CF0530549B3D0863935992EA177B19F2313A19DACF546466B5DCAC0F07"
        proof = 0
        block = blockchain.new_block(proof,SE_Ballot,E_Ballot,SIV, IV, previous_hash)
        response = {'message': "New Block Forged",'index': block['index'],
        'SE_Ballot':block['SE_Ballot'],'E_Ballot':block['E_Ballot'],
                    'SIV':block['SIV'], 'IV':block['IV'],
                    'previous_hash': block['previous_hash'],}
        return jsonify(response), 200
    else:
        try:
            SE_Ballot =VVlog[0]; E_Ballot =VVlog[1]; SIV =VVlog[2]; IV = VVlog[3]
            proof = blockchain.proof_of_work(SE_Ballot, E_Ballot, SIV, IV)
            last_block = blockchain.last_block
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, SE_Ballot,E_Ballot, SIV, IV, previous_hash)
            response = {'message': "New Block Forged",'index': block['index'],
                        'SE_Ballot':block['SE_Ballot'],'E_Ballot':block['E_Ballot'],
                        'SIV':block['IV'],'IV':block['SIV'],
                        'previous_hash': block['previous_hash'],}
            return jsonify(response), 200
        except IndexError:
            print("Ballot is not submitted.. Please Wait...")
            response = {'message' : "Ballot is not submitted.. Please Wait..."}
            return jsonify(response), 200


@app.route('/transactions/new', methods=['GET','POST'])
def new_transaction():
    data = [];
    with open('Voted_Ballot/Data.json') as f:
        data = json.load(f)
    print(data);print(type(data)); values = data
    required = ['S_ct', 'ciphertext', 'S_iv', 'iv']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['S_ct'], values['ciphertext'],
                                       values['S_iv'], values['iv'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    Chain = blockchain.chain; 
    print(type(Chain)); 
    #f = open("Chain_Json/chain.json",'a')
    #f.write(Chain)

    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host= '', port=port)
