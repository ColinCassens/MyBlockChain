from flask import Flask, request
from Block import Block, BlockChain
import time
import json

# Init flask app
app = Flask(__name__)

# Init blockchain object
blockchain = BlockChain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()

    for field in ['author', 'content']:
        if not data.get(field):
            return "Invalid TX Data", 404

    data['timestamp'] = time.time()
    blockchain.add_transaction(data)
    return 'Success', 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return json.dumps({'length': len(chain_data),
                       'chain': chain_data})

