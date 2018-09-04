import firebase_admin
from firebase_admin import credentials,db,storage
from firebase_admin import auth as admin_auth
import os
import pyrebase
config = {
    'apiKey' : "AIzaSyAvN2x2um6odkCrM4s4eDBOFbZlEjpSnp0",
    'authDomain': "cadmium75-5deb5.firebaseapp.com",
    'databaseURL': "https://cadmium75-5deb5.firebaseio.com",
    'projectId' : "cadmium75-5deb5",
    'storageBucket' : "cadmium75-5deb5.appspot.com",
    'messagingSenderId' : "196134275815"
  }
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'startacloud_admin.json')
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://cadmium75-5deb5.firebaseio.com/' }
)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def addFiletoFirebase(filename):
    storage.child('json_keys/' + filename).put('json_keys/' + filename)

def checkifValidUser(idToken):
    decoded_token = admin_auth.verify_id_token(idToken)
    uid = decoded_token['uid']
    ref = db.reference('User').child(uid).get()
    if ref==None:
        return None
    return uid

def loginFB(email,password):
    user = auth.sign_in_with_email_and_password(email, password)
    return user

def addAPISteptoDB(server_name,uid,step,status):
    db.reference('User').child(uid).child('Server Status').child(server_name).child(step).set(status)

def addDroplettoUser(ip_address,uid):
    db.reference('User').child(uid).child('Servers').child(ip_address.replace('.','-')).set(True)
    db.reference('Servers').child(ip_address.replace('.','-')).set(uid)
