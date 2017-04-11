#!/usr/bin/python
# _*_ coding:utf-8 _*_

import flickrapi
import json
import time
import os


#Flickrapi documentation:   https://stuvel.eu/flickrapi-doc/2-calling.html


#FIRST: get your own API-keys!

api_key = u"YOUR_API_KEY_HERE"        #Request your own key and place the key inside the quotes.
api_secret = u"YOUR_API_SECRET_HERE"                     #Request your own key and place the secret inside the quotes.


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
flickr.authenticate_via_browser(perms='read')                       #Requires read authentification: https://www.flickr.com/services/api/flickr.photos.getWithGeoData.html (Needs to be done once per Computer running this)


userfile = open("users.txt", "r")
users = userfile.readlines()

print str(len(users)) + " users will be looked up with the flickr API"
print "This may take some time, please ensure a decent internet connection."
print "A progress-file will be created to keep track of all done users"
print "This progress-file will come in handy if you interrupt the script, or if the connection gets interrupted"

state = os.path.isfile("prog.txt")
if state == True:
    prog = open("prog.txt", "r")
    progr = prog.readlines()
    progress = []
    for item in progr:
        item = item.strip()
        progress.append(item)
    prog.close()
else:
    saveto= open("userlocations.csv", "w")
    prog = open("prog.txt", "w")
    saveto.close()
    prog.close()
    progress = []


prog = open("prog.txt", "a")
saveto = open("userlocations.csv", "a")

print "All preparations done."
time.sleep(5)

for user in users:
    user = user.strip()
    if user not in progress:
        location_var = flickr.profile.getProfile(api_key= api_key, user_id = user)
        parsedloc = json.loads(location_var.decode('utf-8'))

        for key in parsedloc:
            a = type(parsedloc[key])
            if str(a) == "<type 'dict'>":
                b = parsedloc[key]
                for key in b:
                    try:
                        country = str(b["country"].encode("utf-8"))
                        city = str(b["city"].encode("utf-8"))
                    except:                         #This will write 'null' for every user who has no location set!
                        country = "null"
                        city = "null"

        if len(country) ==0:
            country = "null"
        if len(city) ==0:
            city = "null"

        print city
        print country
        saveto.write('"' + user+ '";"' + country + '";"' + city + '";"' + "\n")
        prog.write(user+ "\n")
