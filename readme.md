# Scrap the asins from file and save in Excel file

## To run the code
 - install pip3 and python3
 - install librares using <pip3 install libraryname>
 - run <python3 main.py> , can specify the path if it doesnt work /home/dev/pyy/file.py

 ## Steps
 - run get_links.py to get the product's page link scraped and stored in csv
 - run get_data.py to get the specific product's variation in size and color
  
 ## To Edit file
 - In <get_links.py> 
   - line 47 to change asins file
 - In <get_data.py>
   - line 45; give the link of csv file extracted from get_links.py 
  
## Why I've used Scraper API as proxy because Proxy setting can vary from system to system as this is a free service to use
## Prices can be same for same product as they are displayed through DOM and cannot be scraped as is.