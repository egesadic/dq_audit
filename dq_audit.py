from os import listdir, getcwd
from collections import OrderedDict
from os.path import isfile, join
import requests, sys, random, time
from bs4 import BeautifulSoup

def format_query(string):
    q = str(string).replace(" ", "+")
    return q

def kw_loader(kw_file, no_duplicates = False):
    with open(kw_file, 'r') as f:
        tmp = f.readlines()
        f.close()
        keywords = []
        for elem in tmp:
            to_add = elem.replace("\n", "").replace("\ufeff", "")
            keywords.append(to_add)
        if no_duplicates:
            return list(OrderedDict.fromkeys(keywords))
        else:
            return keywords

def audit(kw, to_find):
    url = "https://www.google.com/search?q=" + format_query(kw)
    match = False
    
    print("Now searching: " + kw)
    #Send the query to Google, retrieve HTML
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()
    #Process HTML as an BS object, an easy form to navigate
    html = BeautifulSoup(response.text, "html.parser")
    #Find all "cite" tags inside the HTML with the class "iUh30", this specific tag contains the URL results of our search.
    search_results = html.find_all("cite", class_ = "iUh30")
    #Search for out target site within the cite tags, if match: save it as 1, else save it as 0.
    for elem in search_results:
        if to_find in elem.text:
            match = True
            break
    if match:
        print("Match found! Saving result...\n")
        return "1"    
    else:
        print("No matches. Proceeding...\n")
        return "0"

#User agent information for "Human Mode", also needed for parsing search results from Google.
USER_AGENT = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

#Path for KW.txt files. Program will iterate through files and will treat each .txt file as KW list.
directory  = getcwd() + "yourfolderhere"        
files      = [f for f in listdir(directory) if isfile(join(directory, f))]
results    = []

#Use this if you have a long list of KW's, will throttle the speed of searches so the program won't be banned from google.
humanMode   = False

for f in files:
    #Load keywords from .txt file
    kw = kw_loader(directory+f)
    #Select the target website to google, it should always be in the first line of the .txt file 
    target = kw[0].strip()
    #Remove the target site to avoid mixing it as a keyword
    kw.pop(0)
    for key in kw:
        tmp = audit(key, target)
        results.append(tmp+"\n")
        if humanMode:
            #If human mode is true, it will put an artificial delay between each query.
            slp = random.randint(10,17)
            print("Search completed for keyword: " + key + ". Sleeping for " + str(slp) + " seconds.")
            time.sleep(slp)
    print("Process completed for file: " + "'" + f + "'" + "\n\n")
    res = open(directory + str(f).replace(".txt", "") + "-results.res", 'w', encoding="utf-8")
    res.writelines(results)
    res.close()
    results.clear()
    
print("Process completed for all " + str(len(files)) + "KW files!\nResults are under " + directory)
exit(0)