import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request
import requests
import wallet

import data
#import flask

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = []
        self.publicKeys=[]



        # Create the genesis block
        if data.myPort==data.adminPort:
            self.current_transactions.append({
                'sender': 0,
                'recipient': data.publicKey,
                'amount': 100*data.numOfParticipants,
                'id':data.nextIndex
            })
            data.nextIndex=data.nextIndex+1
            self.new_block(previous_hash='1', proof=0)#genesis block


    def register_node(self, address,key):
        self.publicKeys.append(key)
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.append(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.append(parsed_url.path)
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
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'current_hash':"string"
        }
        block['current_hash']=self.hash(block)

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def imported_block(self, index, transactions,timestamp,proof,previous_hash,current_hash):
        block = {
            'index': index,
            'timestamp': timestamp,
            'transactions': transactions,
            'proof': proof,
            'previous_hash': previous_hash ,
            'current_hash':current_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount,id):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'id':id
        })
        data.nextIndex=id+1

        return self.last_block['index'] + 1

    def validate_transaction(self,values):
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        fakeBlock= {
            'index': block['index'],
            'timestamp': block['timestamp'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        block_string = json.dumps(fakeBlock, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
