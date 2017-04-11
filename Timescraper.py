#!/usr/bin/python
# _*_ coding:utf-8 _*_

import flickrapi
import json
import time
import os

statei = os.path.isfile("done_time_ids.txt")
statef = os.path.isfile("raw_time_data.csv")

if statei == False:
    stateicreate = open("done_time_ids.txt", "w")
    stateicreate.close()
else:
    pass

if statef == False:
    statefcreate = open("raw_time_data.csv", "w")
    statefcreate.close()
else:
    pass

#Flickrapi documentation:   https://stuvel.eu/flickrapi-doc/2-calling.html
#FIRST: get your own API-keys!

api_key = u"YOUR_API_KEY_HERE"        #Request your own key and place the key inside the quotes.
api_secret = u"YOUR_API_SECRET_HERE"                     #Request your own key and place the secret inside the quotes.


raw_time_file = open("raw_time_data.csv", "a")                #where your datapoints will be stored at
history = open("done_time_ids.txt", "r")                 #all photo_ID's that have been added in the past.

donepre = history.readlines()                      #Preventing adding the same photo twice.
history.close()

done = []
for item in donepre:
    item = item.strip()
    done.append(item)

donepids = open("done_time_ids.txt", "a")

all_photos = open("done_ids.txt", "r")
all_pids = all_photos.readlines()
print str(len(all_pids)) + " + photos will be checked"


print "Ready loading history."

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
flickr.authenticate_via_browser(perms='read')                       #Requires read authentification: https://www.flickr.com/services/api/flickr.photos.getWithGeoData.html (Needs to be done once per Computer running this)

add_data = True                         #needed for the while loop

d = 0
d = d +len(done)
tot = str(len(all_pids))

while int(d) != int(len(all_pids)):

    pid = str(all_pids[d])
    pid = pid.strip()
    if pid not in donepre:
        try: 
            print "Processing photo-id: " + str(pid) +" at: " + str(d+1) + " of " + tot +"."
            timeframe = flickr.photos.getInfo(photo_id=pid)
            parsed = json.loads(timeframe.decode("utf-8"))          #returns a dictionary

            data = parsed["photo"]
            uploadtime = data["dateuploaded"]
            shottime = data["dates"]
            shottakentime = shottime["taken"]

            donepre.append(pid)
            donepids.write(pid + "\n")

            raw_time_file.write('"' + pid + '";"' + shottakentime + '";"' + uploadtime  + '" \n')
        except:
            print "Error with photo " + str(pid) +"."
            raw_time_file.write('"' + pid + '";"null"' + '";null" \n')

    d = d+1

#
raw_time_file.close()                            #Closing the CSV file


print "Process complete"

ext = raw_input("Press enter to terminate the program")
