#!/usr/bin/python
# _*_ coding:utf-8 _*_

import flickrapi
import json
import time

#Flickrapi documentation:   https://stuvel.eu/flickrapi-doc/2-calling.html


#FIRST: get your own API-keys!

api_key = u"YOUR_API_KEY_HERE"        #Request your own key and place the key inside the quotes.
api_secret = u"YOUR_API_SECRET_HERE"                     #Request your own key and place the secret inside the quotes.

flickr_founded = "1076284800"                       #Unixtime

timeframe = 43200                     #Unixtime for 12 hours == 60seconds *60minutes *24hours; This will query the API for a certain time. Increase this number if there aren't any decent results...
one_week = 604800                   #Unixtime for one week == 60seconds *60minutes *24hours* 7days (Scope is too large to be used - only a fraction of the data that is available gets returned)
                                    #Need a Unix convertor?: http://www.unixtimestamp.com/
                                    #Alternatively you can use the built in time module of Python.

raw_file = open("raw_data.csv", "a")                #where your datapoints will be stored at
history = open("done_ids.txt", "r")                 #all photo_ID's that have been added in the past.

donepre = history.readlines()                      #Preventing adding the same photo twice.
history.close()

done = []
for item in donepre:
    item = item.strip()
    done.append(item)

donepids = open("done_ids.txt", "a")
print "Ready loading history."

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
flickr.authenticate_via_browser(perms='read')                       #Requires read authentification: https://www.flickr.com/services/api/flickr.photos.getWithGeoData.html (Needs to be done once per Computer running this)

add_data = True                         #needed for the while loop



        #################THESE ARE YOUR UPPER AND LOWER LIMITS - HARDCODED IN THE SCRIPT!###############

firstdate = 1462822400                  #Bottom time limit, we shall call for all photo's that are uploaded after this timepoint.
finaldate = firstdate + timeframe        #Upper time limit for our small call, the while loop will keep using this untill it reaches the enddate.)

curtime = time.time()                   #gets the current time in unixcode.
curtime = int(curtime)

#curtime = 1376284800                    #overwrites curtime with a value set in the past. You can comment this line out of you wish to go from point X to now. Carefull however, as calling flickr too long on one end may cause connection termination.
#Moet nog lopen!! 29/3/2017

        ################City variables: Latitude, Longitude, radius(in KM) HARDCODED, replace according to the example and leave within quotes!##############
latitude = "51.215539"
longitude = "2.928629"
rad = "5"

while add_data:

    page = 1
    startdate = str(firstdate)
    enddate = str(finaldate)
    shots = flickr.photos.search(page=str(page), has_geo="1", extras="geo, owner_name", privacy_filter="1", per_page="250", min_upload_date=startdate, max_upload_date=enddate, radius_units="km", radius=rad, lat=latitude, lon=longitude)     #There's a max limin on per_page of 250!!
    parsed = json.loads(shots.decode('utf-8'))          #returns a dictionary
    for key in parsed:
        part = parsed["photos"]
        total_pages =  part["pages"]

    print "There are %s pages returned by flickr" %(total_pages)
    #print finaldate
    while page <= total_pages:
        shots = flickr.photos.search(page=str(page), has_geo="1", extras="geo, owner_name", privacy_filter="1", per_page="250", min_upload_date=startdate, max_upload_date=enddate, radius_units="km", radius=rad, lat=latitude, lon=longitude)
        parsed = json.loads(shots.decode('utf-8'))
        for key in parsed:
            x =  type(parsed[key])
            if str(x) == "<type 'dict'>":   
                newdict = parsed[key]       
                for key in newdict:
                    y =  type(newdict[key])
                    if str(y) == "<type 'list'>":
                        for item in newdict[key]:
                            for key in item:
                                photo_id = str(item["id"].encode("utf-8"))

                            if photo_id not in done:
                                done.append(photo_id)
                                longt = str(item["longitude"])
                                lat = str(item["latitude"])
                                user_internal_id = str(item["owner"].encode("utf-8"))
                                user_name = str(item["ownername"].encode("utf-8"))
                                visit = "https://www.flickr.com/photos/" + user_internal_id + "/" + photo_id
                                #print lat
                                #print longt

                                raw_file.write('"'+ photo_id + '";"' + user_internal_id + '";"' + user_name + '";"' + lat + '";"' + longt + '";"' + visit + '"\n')
                                donepids.write(photo_id + "\n")
                            else:
                                pass
                                #print "double"



        print str(page) + " of " + str(total_pages) + " is done."
        page = page+1

        #print "page UP"
        #print "taking new data"
    firstdate = firstdate + timeframe
    finaldate = finaldate + timeframe
    #print firstdate
    print finaldate

    if curtime < firstdate:
        add_data = False

#
raw_file.close()                            #Closing the CSV file
donepids.close()                            #Closing the progress tracker file

print "Process complete"

ext = raw_input("Press enter to terminate the program")

