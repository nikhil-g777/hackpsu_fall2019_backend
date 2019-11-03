from flask import Flask, jsonify, request
import requests
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
from sklearn.cluster import KMeans
import json

# Connect to Google Firebase API.
cred = credentials.Certificate('headsup-disaster--doxqbm-firebase-adminsdk-rmtzx-412ee01502.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://headsup-disaster-doxqbm.firebaseio.com/'
})

app = Flask(__name__)

@app.route('/weather')
def weather():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    params = {
        'apikey': '1aB2facNJTGUj29A7GxRGRlpD38clNDP',
        'q': latitude + ',' + longitude
    }

    r = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search', params)
    city = r.json()['Key']
    r = requests.get('http://dataservice.accuweather.com/alarms/v1/5day/'+city+'?apikey=1aB2facNJTGUj29A7GxRGRlpD38clNDP')
    danger = r.json()
    if len(danger) == 0:
        danger = 'None'
    r = requests.get('http://dataservice.accuweather.com/currentconditions/v1/'+city+'?apikey=1aB2facNJTGUj29A7GxRGRlpD38clNDP')
    weather = r.json()[0]['WeatherText']
    temp = r.json()[0]['Temperature']['Imperial']['Value']
    conditions = ('Weather: '+weather+', Temperature: '+str(temp)+'F, Danger: '+danger)
    return conditions


@app.route('/cluster')
def cluster():
    n_clusters = int(request.args.get('camps'))
    person_list = []
    locations = []

    ref = db.reference('People')
    snapshot = ref.get()
    for person, data in snapshot.items():
        person_dict = {'latitude':data['latitude'],'longitude': data['longitude'],'status':data['status']}
        person_list.append(person_dict)
        locations.append(list((data['latitude'],data['longitude'])))
    locations = np.asarray(locations)

    cluster = KMeans(n_clusters)
    cluster.fit_predict(locations)

    # plt.scatter(locations[:,0], locations[:,1], c=cluster.labels_, cmap='rainbow')
    print(cluster)
    for index, person in enumerate(person_list):
        person['cluster'] = int(cluster.labels_[index])
    camps = []
    for center in cluster.cluster_centers_:
        camps.append({
            'latitude': center[0],
            'longitude': center[1]
        })
        person['cluster'] = int(cluster.labels_[index])

    res = json.dumps({'camps': camps, 'people': person_list})
    return res

if __name__ == '__main__':
    app.run(port=3000)