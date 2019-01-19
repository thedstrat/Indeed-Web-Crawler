#Beautiful Soup project

import bs4 as bs
from urllib.request import urlopen, Request
import pandas as pd
import re

#Create a header to prevent 404 error. This is necessary on sites like Angelist.
headers={'User-Agent': 'Mozilla/5.0'}

#Request an Indeed.com Webpage
source = ('https://www.indeed.com/jobs?q=data+scientist&l=Austin%2C+TX')
req = Request(url = source, headers = headers)
html = urlopen(req).read()

#Create a parse tree with beautifulsoup
soup = bs.BeautifulSoup(html, 'lxml')


#Get all Job Titles
tagarray = []

#Search through bs parse tree to find text with the below properties (which are all the job titles)
for tag in soup.findAll('a', {'target': "_blank", 'title': True, 'data-tn-element':"jobTitle"}):
    tagarray.append(tag.get_text()) #output text-based results to array

jobtitles = pd.DataFrame(data = tagarray) #output to pandas df


#Get all Job Links
urlarray = []

#Search through bs parse tree to find links in href tag with 'clk' in them
for url in soup.findAll('a', {'href': re.compile('clk')}, {'href': re.compile('company')}):
    urlarray.append("www.indeed.com" + url.get('href')) #add 'www.indeed.com' to the href and append to array

joblinks = pd.DataFrame(data = urlarray) #ouput to pandas df

    
#Join DataFrames and rename columns
result = pd.concat([jobtitles, joblinks], axis = 1)
result.columns = ['Job Titles', 'Job Links'] 

#Print and output to a CSV
print(result)
result.to_csv('beautifulsoup.csv')
