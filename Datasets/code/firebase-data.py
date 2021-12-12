import pyrebase
import json

with open('../DONTEDIT/ppidb.json') as f:
    ppidb = json.load(f)

"""Set up firebase"""

pyrebase_config = {
    "apiKey": "AIzaSyB97xXrED09JJoEZqmEdAN1PlAL-CBLeeM",
    "authDomain": "ppidb-b0ac7.firebaseapp.com",
    "databaseURL": "https://ppidb-b0ac7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "ppidb-b0ac7",
    "storageBucket": "ppidb-b0ac7.appspot.com",
    "messagingSenderId": "113239765206",
    "appId": "1:113239765206:web:bb75ee1548eab999089977",
    "measurementId": "${config.measurementId}",
}

firebase = pyrebase.initialize_app(pyrebase_config)
db = firebase.database()



db.child("stats").set({"interactions": len(ppidb['interactions']), "proteins": len(ppidb['protiens'])})