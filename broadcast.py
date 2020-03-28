import data
from flask import Flask, jsonify, request
import requests
import json
import threading
import time


def broadcast_transaction(new_trans):
    kwargs = {}
    kwargs['timeout'] = 25
    trans_dict=new_trans.asDictionary()
    #print(trans_dict)
    for node in data.allUrls:
        #print(node+"/receiveATransaction")
        response=requests.post(node+"/receiveATransaction",json=trans_dict,**kwargs)
        #print(response.status_code)
        print ("time to reciece the transaction")


def broadcast_a_block(block):
    kwargs = {}
    kwargs['timeout'] = 25
    for node in data.allUrls:
        response=requests.post(node+"/receiveABlock",json=block.asDictionary(),**kwargs)
        #print(response.status_code)
