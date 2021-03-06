from flask import Flask, request, jsonify
from firebase_admin import auth, db
import requests
from . import routes


@routes.route('/createMsg', methods=['POST'])
def createMsg():

    senderUid = request.json.get('senderUid')
    receiverUid = request.json.get('receiverUid')
    message = request.json.get('message') 
    timestamp = request.json.get('timestamp')
    # roomKey = request.json.get('roomKey')

    if((senderUid==None) | (receiverUid==None) | (message==None) | (timestamp==None)):
        return {
            "success":False,
            "message":"ya 7ywan eb3at eldata kolha"
        }
    
    # if (roomKey == None):
        
    roomKey = db.reference('users/{0}/messages/{1}/roomKey'.format(senderUid, receiverUid)).get()

    if (roomKey == None):
        roomKey = db.reference('messages').push("new Message").key
        
        senderUser = db.reference('users/{0}'.format(senderUid)).get()
        receiverUser = db.reference('users/{0}'.format(receiverUid)).get()

        print("sss dsadsad asdsasadsa {0}".format(senderUser))

        db.reference('users/{0}/messages/{1}'.format(senderUid, receiverUid)).update({
            # "avatar": receiverUser["avatar"],
            "roomKey": roomKey,
            "name": "{0} {1}".format(receiverUser["firstName"], receiverUser["lastName"])
        })

        db.reference('users/{0}/messages/{1}'.format(receiverUid, senderUid)).update({
            # "avatar": senderUser["avatar"],
            "roomKey": roomKey,
            "name": "{0} {1}".format(senderUser["firstName"], senderUser["lastName"])
        })

    db.reference('messages/{0}/{1}'.format(roomKey, timestamp)).update({
        "message": message,
        "senderUid": senderUid
    })

    return {
        "success": True,
        "message": "Message created {0}".format(roomKey),
    }

