import pyrebase

firebase_config = {
   "apiKey": "AIzaSyACugKFIdT7kYVWAwg7Oa2olyNOZBtiHO0",
   "authDomain": "growth-mindset-app-challenge.firebaseapp.com",
   "databaseURL": "https://growth-mindset-app-challenge-default-rtdb.firebaseio.com/",
   "projectId": "growth-mindset-app-challenge",
   "storageBucket": "growth-mindset-app-challenge.appspot.com",
   "messagingSenderId": "359138635801",
   "appId": "1:359138635801:web:85f78e71de515d816e3a88",
   "measurementId": "G-X5M0H8RC06"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
