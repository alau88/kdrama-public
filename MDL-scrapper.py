#More detailed than test.py
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pandas as pd
import re

url = "https://mydramalist.com/search?adv=titles&ty=68&co=3&re=2012,2022&rt=4,10&st=3&so=popular&page="
sub_url = "https://mydramalist.com"
max_pages = 100 #Number of pages to iterate to
url_list = []
for page in range(max_pages):
    popular_page = requests.get(url+str(page+1))
    soup = BeautifulSoup(popular_page.content, "html.parser")
    pop_page = soup.find_all("a", class_="block")
    for link in pop_page:
        sub_link = sub_url + link.get('href') + "/cast" #URL for Cast page of respective title
        url_list.append(sub_link)
    sleep(randint(2,10)) #delay to prevent ip address blacklisting
print(url_list)
title_list, country_list, episode_list, airdate_list, airslot_list, airtime_list, rating_list = [], [], [], [], [], [], []
network_list =[]
genre_list =[]
tag_list =[]
score_list, watchers_list = [], []
voter_list = []
director_list =[]
writer_list =[]
leads_list =[]
leads_likes_avg = []
leads_likes_max = []
""" idol_lead = []
idol_search = ["idol","boy group","girl group", "boygroup","girlgroup"] #These words are listed even if actors are former trainees/idols
pattern = re.compile("|".join(idol_search)) """

#Get Title, MDL ID#, Rating, Year, Genre, Tags, Main Cast, #of watchers, #reviews, screenwriter, director
for url in url_list:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    detail_box = soup.find_all("ul", class_="list m-b-0")[0] #Details box (1st instance of class)
    ##Details
    #Title
    title_list.append(detail_box.find("span", itemprop="name").get_text()) #Title of drama
    #print(title_list)
    #Country, Episodes, Air Date, Air Slot, Airtime, Rating
    if len(detail_box.find_all(text=re.compile("Country:"))) == 0: #check if there is main role box
        country_list.append("n/a")
    else:
        country_list.append(str(detail_box.find('b',string="Country:").next_sibling))
    if len(detail_box.find_all(text=re.compile("Episodes:"))) == 0: #check if there is main role box
        episode_list.append("n/a")
    else:
        episode_list.append(str(detail_box.find('b',string="Episodes:").next_sibling))
    if len(detail_box.find_all(text=re.compile("Aired:"))) == 0: #check if there is main role box
        airdate_list.append("n/a")
    else:
        airdate_list.append(str(detail_box.find('b',string="Aired:").next_sibling))
    if len(detail_box.find_all(text=re.compile("Aired On:"))) == 0: #check if there is main role box
        airslot_list.append("n/a")
    else:
        airslot_list.append(str(detail_box.find('b',string="Aired On:").next_sibling))
    if len(detail_box.find_all(text=re.compile("Duration:"))) == 0: #check if there is main role box
        airtime_list.append("n/a")
    else:
        airtime_list.append(str(detail_box.find('b',string="Duration:").next_sibling)) #Look for string after "Duration:" #can change to integer if needed
    if len(detail_box.find_all(text=re.compile("ontent Rating:"))) == 0: #check if there is main role box
        rating_list.append("n/a")
    else:
        rating_list.append(str(detail_box.find('b',string="Content Rating:").next_sibling))
    #Original Network
    temp = []
    if len(detail_box.find_all(href=re.compile("nt="))) == 0:
        temp = ['n/a']
    else:
        for detail in detail_box.find_all(href=re.compile("nt=")): #Network href tag
            temp.append(detail.get_text())
    network_list.append(', '.join(temp)) #Combine all networks into one string
    #print(network_list)
    #Genres
    temp = []
    for detail in detail_box.find_all(href=re.compile("ge=")): #Genre href tag
        temp.append(detail.get_text())
    genre_list.append(', '.join(temp)) #Combine all genres into one string
    #print(genre_list)
    #Tags
    temp = []
    for detail in detail_box.find_all(href=re.compile("th=")): #Tag href tag
        temp.append(detail.get_text())
    tag_list.append(', '.join(temp)) #Combine all tags into one string
    #print(tag_list)
    ## MDL Stats
    stat_box = soup.find_all("ul", class_="list m-b-0")[1] #MDL Stats box (2nd instance)
    #Score + Watchers
    temp = [] #Score, Rank, Popularity, Watchers, Favourites(0)
    for b_tag in stat_box.find_all('b'): 
        #print(b_tag.text)
        temp.append(b_tag.next_sibling) #Find text after b tags
    score_list.append(float(temp[0])) #Score
    watchers_list.append(int(temp[3].replace(',', ''))) #Watchers: Replace "," and change to int
    #print(score_list, watchers_list)
    #Voters
    temp = stat_box.find("span", class_="hft").get_text() #Number of watchers
    temp = re.findall(r'\d+', temp) #Extract numbers
    voter_list.append(int(''.join(temp))) #Convert to int and append to list
    #print(voter_list)
    ## Cast
    cast_box = soup.find("div", class_="box cast-credits") #Cast Credits box (sole instance)
    #Always Director(s), Screenwriter(s), Main Role, Support Role, etc
    # Director(s)
    cast_index = 0
    temp = []
    if len(cast_box.find_all(text=re.compile("Director"))) == 0: #Check if there is director box
        temp = ["n/a"]
    else:
        director_box = cast_box.find_all("ul", class_="list no-border p-b clear")[cast_index] #First box is director(s)
        for director in director_box.find_all("a", class_="text-primary text-ellipsis"): 
            temp.append(director.get("href")) #Getting the MDL people reference instead of name for unique identification
            #temp.append(director.get_text()) #Change to this line if text version of name is desired
        cast_index += 1
    director_list.append(', '.join(temp)) #Combine all tags into one string
    #print(director_list)
    # Screenwriter(s)
    if len(cast_box.find_all(text="Screenwriter & Director")) != 0: #Screenwriter&Director
        temp = temp #Keep from directors
    elif len(cast_box.find_all(text="Screenwriter")) == 0: #Check if there is screenwriter box
        temp = ["n/a"]
    else:
        temp = []
        writer_box = cast_box.find_all("ul", class_="list no-border p-b clear")[cast_index] #Second box is screenwriter(s)
        for writer in writer_box.find_all("a", class_="text-primary text-ellipsis"): 
            temp.append(writer.get("href")) #Getting the MDL people reference instead of name for unique identification
            #temp.append(writor.get_text()) #Change to this line if text version of name is desired
        cast_index += 1
    writer_list.append(', '.join(temp)) #Combine all tags into one string
    #print(writer_list)
    # Main Role
    temp = []
    likes = []
    #idol = 0
    if len(cast_box.find_all(text="Main Role")) == 0: #check if there is main role box
        temp = ["n/a"]
        likes = [0]
    else:
        leads_box = cast_box.find_all("ul", class_="list no-border p-b clear")[cast_index] #Third box is main lead(s)
        for leads in leads_box.find_all("a", class_="text-primary", href=re.compile("people")): #href: "people" (real life), "character" (in drama)
            temp.append(leads.get("href")) #Getting the MDL people reference instead of name for unique identification
            #temp.append(leads.get_text()) #Change to this line if text version of name is desired
            cast_link = sub_url + leads.get("href")
            cast_page = requests.get(cast_link)
            cast_soup = BeautifulSoup(cast_page.content, "html.parser")
            likes.append(int(str(cast_soup.find("span", class_="like-cntb").text).replace(',','')))
            """ desc = cast_soup.find("div", class_="col-sm-8 col-lg-12 col-md-12")
            if desc.find_all(string=pattern, recursive=True):
                idol += 1 """
    avg_likes = sum(likes)/len(likes)
    leads_list.append(', '.join(temp)) #Combine all tags into one string
    leads_likes_avg.append(avg_likes)
    leads_likes_max.append(max(likes))
    #idol_lead.append(idol)
    #print(leads_list)
    # Too many support roles in cast, likely to have less impact (Exception idols?)
    sleep(randint(2,10))
print(len(url_list),len(title_list),len(country_list),len(airdate_list),len(airslot_list),len(episode_list),len(airtime_list),len(network_list),len(director_list),len(writer_list))
print(len(leads_list),len(score_list),len(voter_list),len(watchers_list),len(genre_list),len(tag_list))

MDLdata = pd.DataFrame(
    {'URL': url_list,
     'Title': title_list,
     'Country': country_list,
     'Air Date': airdate_list,
     'Time Slot': airslot_list,
     'Episodes': episode_list,
     'Runtime': airtime_list,
     'Network': network_list,
     'Director': director_list,
     'Writer': writer_list,
     'Leads': leads_list,
     'Leads_Likes': leads_likes_avg,
     'Leads_Max': leads_likes_max,
     #'Idols': idol_lead,
     'Score': score_list,
     'Voter': voter_list,
     'Watchers': watchers_list,
     'Genre': genre_list,
     'Tag': tag_list
})
MDLdata.index.name='Rank'
MDLdata.to_csv('MDL_Data_2012_2022.csv')