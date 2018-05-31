import firebase_admin
from firebase_admin import auth,credentials,db

cred = credentials.Certificate('cloudeity_admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://cloudeity-a3022.firebaseio.com/' }
)
