# flickr-API-Scraper
These simple Python scripts allow you to scrape data from the vast FLICKR repository. You can use this to track visitors... to your city. Simply change the X and Y coordinates and the radius in the main scraper and then use the other scripts to gather the location of those users and the date those photos were taken. You can then use tools like Tableau10 to provide a visualisation or compare your city to other cities.... If you plan on using these scrapers, I'd like to be credited for writing them. 


##Scripts (this is the order you'll want them to run):
1) City Scraper.py
You'll need to edit this script and provide your own API key and secret for it to work. Next add X and Y coordinates and a radius to scrape Flickr for the data you want.

2) Get unique user IDs.py
This script goes over the data acquired by (1)) and creates a file with the unique users.

3) User Scraper.py
This script goes over the users created by (2)) and gets their location. If no location is set, a null is written to the outfile. The country and city is collected from FLICKR. Please note that countries/cities have no fixed input and that users can write whatever they want. If you use Tableau to visualise this data, you can group them together. Alternatively you can write a stemming script that goes over the entire file and modifies it.
  Example==> België, Belgium, Belgique, belgie, Belgien ==> all of these refer to one country. You can easily write a stemming script that overwrites these different values to a value of your choosing. (For added benefit you can use the .lower() method in Python so that Belgium and belgium are considered as one and the same thing)
  
4) Timescraper.py
This script goes over all photos that are part of the dataset, it gets the time they were taken (YYYY-MM-DD HH:MM:SS) and the date they were uploaded (in UNIXtime). You can use this to create timeseries of your data. A TRY and EXCEPT clause have been added since it may happen that users delete a photo, if this is the case, then "null" values will be written in the outputfile.


NOTES:
- All files create .CSV files, any .TXT file that gets created in the process is used to track progress, these can be deleted once all data has been scraped.

- Be sure to get your own API Keys.

- Written for Python2

Best of luck
Frédéric Pietowski. 
