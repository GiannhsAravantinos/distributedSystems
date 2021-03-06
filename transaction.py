from time import time
from flask import Flask, jsonify, request
import requests
import json
import threading

from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64
import copy

import data
import utilities

class transaction:

    def __init__(self,sender, recipient, amount,timestamp, inputs,outputs, id=None, signature=None):
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        self.timestamp=timestamp

        self.inputs=inputs
        self.outputs=outputs
        self.id=id
        self.signature=signature

    def calculateId(self):
        tempDict={
            "sender":self.sender,
            "recipient":self.recipient,
            "timestamp":self.timestamp
        }

        asString=json.dumps(tempDict,sort_keys=True)
        hash = utilities.hashStringToString(asString)
        return hash

    def asDictionary(self):
        tempDict={
            "sender":self.sender,
            "recipient":self.recipient,
            "amount":self.amount,
            "timestamp":self.timestamp,
            "inputs":self.inputs,
            "outputs":self.outputs,
            "id":self.id,
            "signature":self.signature

        }
        return tempDict




    def sign(self):
        rsa_key = RSA.importKey(data.privateKey) # δημιουργία αντικειμένου τύπου κλειδιού
        signer = PKCS1_v1_5.new(rsa_key) # δημιουργία του υπογραφέα
        signedId=SHA384.new(self.id.encode()) # αντικείμενο πρός υπογραφή
        self.signature = base64.b64encode(signer.sign(signedId)).decode() # υπογραφή




    def verify_signature(self):

        try:
            if self.id != self.calculateId():
                return False
            rsa_key1 = RSA.importKey(self.sender)
            signedId=SHA384.new(self.id.encode())
            verifier = PKCS1_v1_5.new(rsa_key1)
            ver= verifier.verify(signedId, base64.b64decode(self.signature))
            
            return ver
        except Exception as e:
            print(f'verify_signature: {e.__class__.__name__}: {e}')
            return False

    def validate_transaction(self):#validates a trans and changes our current state
        try:                       #true trans is valid , flase trans not valid
            with data.lock:
                if not data.hasReceivedGenesisBlock:
                    data.utxos[0][self.id]=self.amount
                    data.hasReceivedGenesisBlock=True
                    return True
                else:
                    if self.sender==self.recipient:
                        print("Sender is Recipient")
                        return False
                    if self.amount<0:
                        print("Negate amount")
                        return False

                    indexOfSender=data.allPublicKeys.index(self.sender)
                    indexOfRecipient=data.allPublicKeys.index(self.recipient)

                    tempCopyOfUtxosSender=copy.deepcopy(data.utxos[indexOfSender])#θα δουλευουμε σε αντιγραφα ωστε αν κατι παει λαθος αν μην χαλασει τα δεδομενα μας
                    tempCopyOfUtxosRecipient=copy.deepcopy(data.utxos[indexOfRecipient])
                    allMoney=0

                    for transId in self.inputs:
                        if transId in tempCopyOfUtxosSender:
                            allMoney=allMoney+ tempCopyOfUtxosSender[transId]#παιρνουμε τα λεφτα που πηρε απο εκεινο το trans
                            tempCopyOfUtxosSender.pop(transId)#το αφαιρουμε για να μην τα ξαναμετρησουμε
                        else:
                            print("A past transaction was not found")
                            return False

                    if(allMoney<self.amount):
                        print("Not enough money")
                        return False
                    #δεν πηγε κατι λαθος, παιρνει ο καθενας τα λεφτα του και ολοι ειμαστε μια χαρα
                    if allMoney-self.amount>0:
                        tempCopyOfUtxosSender[self.id]=allMoney-self.amount#ο sender παιρνει τα ρεστα του
                    tempCopyOfUtxosRecipient[self.id]=self.amount

                    data.utxos[indexOfSender]=tempCopyOfUtxosSender
                    data.utxos[indexOfRecipient]=tempCopyOfUtxosRecipient
                    return True

        except Exception as e:
            print(f'validate_transaction: {e.__class__.__name__}: {e}')
            return False

'''
def new_transaction(self, sender, recipient, amount,id):
    self.current_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'id':id
    })
    data.nextIndex=id+1

    return self.last_block['index'] + 1


'''
def createTranasactionFromDictionary(dictionary):
    b=dictionary
    return transaction(b['sender'], b['recipient'], b['amount'],b['timestamp'], b['inputs'],b['outputs'], b['id'], b['signature'])

def create_transaction(rec_address,amount):

    with data.lock:
        inputs=utilities.getListOfKeys( data.utxos[data.id]  )# για input βαζουμε ο,τι συναλλαγη εχω στο ονομα μου

        new_trans=transaction(data.publicKey,data.allPublicKeys[rec_address],amount,time(),inputs,[])

    new_trans.id=new_trans.calculateId()
    new_trans.sign()
    return new_trans

def createGenesisTransaction():#mono o admin to ektelei

    timestamp=time()
    genTransaction=transaction(0,data.publicKey,100*data.numOfParticipants,timestamp,[],[])
    genTransaction.id= genTransaction.calculateId()

    return genTransaction
