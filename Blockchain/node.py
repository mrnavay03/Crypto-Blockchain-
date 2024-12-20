from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods = ['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        respond = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        
        return jsonify(respond), 201
    else:
        respond = {
            'message': 'Saving keys failed!'
        }
        return jsonify(respond), 500

  

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)

        respond = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(respond), 201
    else:
        respond = {
            'message': 'Saving keys failed!'
        }
        return jsonify(respond), 500
        

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        respond = {
            'message': 'Successfully fetched balance',
            'funds': balance
        }
        return jsonify(respond), 200
    else:
        respond = {
            'message': 'Loading balance failed!',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(respond), 500


@app.route('/broadcast_transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        respond = {'message': 'No data found!'}
        return jsonify(respond), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required):
        respond = {'message': 'Some data is missing!'}
        return jsonify(respond), 400
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        respond = {
            'message': 'Successfully added transaction!',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(respond), 201
    else:
        respond = {
            'message': 'Creating a transaction failed!'
        }
        return jsonify(respond), 500
    

@app.route('/broadcast_block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        respond = {'message': 'No data found!'}
        return jsonify(respond), 400
    if 'block' not in values:
        respond = {'message': 'Some data is missing!'}
        return jsonify(respond), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            respond = {'message': 'Block added'}
            return jsonify(respond), 201
        else:
            respond = {'message': 'Block is invalid'}
            return jsonify(respond), 409
    elif block['index'] > blockchain.chain[-1].index:
        respond = {'message': 'Blockchain seems different from local one!'}
        blockchain.resolve_conflicts = True
        return jsonify(respond), 200
    else:
        respond = {'message': 'Blockchain seems shorter, block not added!'}
        return jsonify(respond), 409






@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        respond = {
            'message': 'No wallet set up!'
        }
        return jsonify(respond), 400
    values = request.get_json()
    if not values:
        respond = {
            'message': 'No data found!'
        }
        return jsonify(respond), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        respond = {
            'message': 'Required data is missing!'
        }
        return jsonify(respond), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transactions(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        respond = {
            'message': 'Successfully added transaction!',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(respond), 201
    else:
        respond = {
            'message': 'Creating a transaction failed!'
        }
        return jsonify(respond), 500


@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        respond = {'message': 'Resolve conflicts first, Block not added!'}
        return jsonify(respond), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        respond = {
            'message': 'Block added successfully!',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(respond), 201
    else:
        respond = {
            'message': 'Adding a block failed!',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(respond), 500
    

@app.route('/resolve_conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        respond = {'message': 'Chain was replaced!'}
    else:
        respond = {'message': 'Local chain kept'}
    return jsonify(respond), 200


@app.route('/transactions', methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200



@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snap = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snap]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        respond = {
            'message': 'No data found!'
        }
        return jsonify(respond), 400
    if 'node' not in values:
        respond = {
            'message': 'No node data found!'
        }
        return jsonify(respond), 400
    
    node = values['node']
    blockchain.add_peer_node(node)
    respond = {
        'message': 'Node added successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(respond), 201

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        respond = {
            'message': 'No node found!'
        }
        return jsonify(respond), 400
    blockchain.remove_remove_peer_node(node_url)
    respond = {
            'message': 'Node removed!',
            'all_nodes': blockchain.get_peer_nodes()
        }
    return jsonify(respond), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    respond = {
        'all_nodes': nodes
    }
    return jsonify(respond), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type = int, default=5000)
    args =  parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='127.0.0.1', port = port)
