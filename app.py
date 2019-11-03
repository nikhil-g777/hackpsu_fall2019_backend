from flask import Flask, jsonify, request
import requests
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import json

# Connect to Google Firebase API.
cred = credentials.Certificate('headsup-disaster--doxqbm-firebase-adminsdk-rmtzx-412ee01502.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://headsup-disaster-doxqbm.firebaseio.com/'
})

app = Flask(__name__)


@app.route('/cluster')
def cluster():
    n_clusters = int(request.args.get('camps'))
    person_list = []
    locations = []

    ref = db.reference('People')
    snapshot = ref.get()
    for person, data in snapshot.items():
        person_dict = {'latitude':data['latitude'],'longitude':data['longitude'],'status':data['status']}
        person_list.append(person_dict)
        locations.append(list((data['latitude'],data['longitude'])))
    locations = np.asarray(locations)

    cluster = KMeans(n_clusters)
    cluster.fit_predict(locations)

    plt.scatter(locations[:,0], locations[:,1], c=cluster.labels_, cmap='rainbow')
          
    for index, person in enumerate(person_list):
        person['cluster'] = cluster.labels_[index]
    res = json.dumps({'people': person_list})
    return res

if __name__ == '__main__':
    app.run()
