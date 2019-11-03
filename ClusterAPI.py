import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Connect to Google Firebase API.
cred = credentials.Certificate('headsup-disaster--doxqbm-firebase-adminsdk-rmtzx-412ee01502.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://headsup-disaster-doxqbm.firebaseio.com/'
})

# This function takes in the number of relief camps is to be set up and returns the coordinates for them to be set up.
def clusterCenters(n_clusters):
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
    return cluster.cluster_centers_,person_list


##n_camps = int(input("Number of relief camps to set up: "))
##relief_camp_coordinates = clusterCenters(n_camps)
##print(relief_camp_coordinates)
