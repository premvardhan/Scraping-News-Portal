#!/usr/bin/env python
# coding: utf-8

# Import libraries
import json
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient 
from flask_cors import CORS 



# Get the links of interested article 
def get_article(soup):
    all_links = []
    name = "fc-item fc-item--has-image fc-item--pillar-news fc-item--type-feature js-fc-item fc-item--list-mobile fc-item--list-tablet js-snappable"
    articles = soup.find_all("div", {"class": name})
    for article in articles:
        art_link = article.find("a")["href"]
        all_links.append(art_link)
    return all_links
    
# Parse the article links and get the required content
def parse_articles(links):
    all_articles = []
    for art_link in links:
        article_page = requests.get(art_link)
        parse_article = BeautifulSoup(article_page.text, "html.parser")
        data = get_info(parse_article)
        data.update({"article_link":art_link})
        all_articles.append(data)
    
    return all_articles
        
# Extract title, authors and content
def get_info(article_page):
    authors = []
    contents = []
    title = article_page.find("title").text.split("|")[0]
    section = article_page.find('script', type='application/ld+json')
    for auth in section:
        json_data = json.loads(auth)
        authors.append(json_data[0]["author"][0]["name"])
    content = article_page.find_all("p", {"class":"css-38z03z"})
    for para in content:
        contents.append(para.text)
    metadata = {"title": title, "author": authors, "content":"".join(contents), "article_link":[]}
    return metadata

# Connect to mongodb
def connect():
    # Enter your creadentials
    client = MongoClient("mongodb+srv://<YourCredentials>:<YourCredentials>@cluster0.fskuj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    return client

# Insert into mongo
def inset_into_mongo(cluster, content):
    # Database
    db = cluster.nu
    # Table
    table = db["nu_test"]
    for cont in content:
        table.insert_one(cont)
    return {"Data inserted sucessfully"}
        

if __name__ == '__main__': 
    # Url to be parsed
    url = "https://www.theguardian.com/au"
    # Get the response as html
    html = requests.get(url)
    # Parse the response
    soup = BeautifulSoup(html.content, 'html.parser')
    links = get_article(soup)
    content = parse_articles(links)
    print("Data extracted.\n\nInserting into mongodb...\n")
    cluster = connect()
    msg = inset_into_mongo(cluster, content)
    print(msg)


