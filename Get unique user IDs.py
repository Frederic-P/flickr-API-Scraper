#!/usr/bin/python
# _*_ coding:utf-8 _*_

import time

x = open("raw_data.csv", "r")
filecontent = x.readlines()
x.close()

allusers = []

for line in filecontent:
    line = line.split(";")
    user = line[1]
    user = user.strip('"')
    if user not in allusers:
        allusers.append(user)


print str(len(filecontent)) +" records"
print str(len(allusers)) +" unique users"

userout = open("users.txt", "w")
for uid in allusers:
    userout.write(uid+"\n")

userout.close()

print "User ID's are written to users.txt; you can now use those ID's to scrape Flickr for the location data."
print "script closes in 10 seconds."
time.sleep(10)
exit()
