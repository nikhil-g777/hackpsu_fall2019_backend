import firebase_admin
from firebase_admin import credentials, db
import random
from twilio.rest import Client

# Connect to Google Firebase API.
cred = credentials.Certificate('headsup-disaster--doxqbm-firebase-adminsdk-rmtzx-412ee01502.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://headsup-disaster-doxqbm.firebaseio.com/'
})

emergency_victims_list = []

ref = db.reference('People')
snapshot = ref.get()
for person, data in snapshot.items():
    if data['status'] == 'emergency':
        emergency_victims_list.append((person,data))

randindex = random.randint(0,len(emergency_victims_list))
victim = emergency_victims_list[randindex]
victim_message = victim[1]['message']

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACc578344cdd3dce189af7c467191cdaae'
auth_token = '2f52aca1166f563f631512622ea60f9b'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body=victim_message,
                     from_='+14847188111',
                     to='+19172873402'
                 )

print(message.sid)
