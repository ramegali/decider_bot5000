# JAKE'S PIZZA CRAWLER 
# by Jake Adams copyright 2017 

import requests
from bs4 import BeautifulSoup

def pizza_spider(max_pages, town, state):
    page = 1
    list_of_places = {}

    while page <= max_pages:
        if page is 1:
            url = 'http://www.yellowpages.com/search?search_terms=pizza&geo_location_terms=' + town + '%2C+' + state
        else:
            url = "http://www.yellowpages.com/search?search_terms=pizza&geo_location_terms=" + town +"%2C%20"+ state +"&page=" + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        # in findAll the 'a' flag stand for anchor which indicates where links are in html
        for link in soup.findAll('a', {'class':'business-name'}):
            href = "http://www.yellowpages.com" + link.get('href')
            title = link.string
            if title is None:
                # gets rid of some addresses that don't work
                continue

            local_soup = soup_helper(href)
            website = get_pizzeria_url(local_soup)
            phone_num = get_pizzeria_phone(soup)
            address = get_pizzeria_address(soup)

            info = {}
            info['address'] = address
            info['phone-number'] = phone_num
            info['website'] = website
            # rating
            list_of_places[title] = info


        page += 1
    return list_of_places

def soup_helper(url): # returns a soup obj
    source_code = requests.get(url)
    plain_text = source_code.text
    return BeautifulSoup(plain_text, "html.parser")

def get_pizzeria_url(soup):
    for pizzeria_link in soup.findAll('a', {'class':'secondary-btn website-link'}):
        return pizzeria_link.get('href')


def get_pizzeria_phone(soup):
    for phone in soup.findAll('li', {'class':"phone primary"}):
        return phone.string


def get_pizzeria_address(soup):
    for i in soup.findAll('p', {'class':"adr"}):  # street name and num
        return i.string


print(r'''
    ____  _
   |  _ \(_)__________ _
   | |_) | |_  /_  / _` |
   |  __/| |/ / / / (_| |
   |_|_  |_/___/___\__,_|  _             ____
  / ___|_ __ __ ___      _| | ___ _ __  |___ \
 | |   | '__/ _` \ \ /\ / / |/ _ \ '__|   __) |
 | |___| | | (_| |\ V  V /| |  __/ |     / __/
  \____|_|  \__,_| \_/\_/ |_|\___|_|    |_____|
  ''')
print("\nWelcome")
town = raw_input("What town/city are you looking for pizza in?\n-> ")
state = raw_input("What state are you in?\n-> ")
page_str = raw_input("How many pages do you want to search?\n-> ")
print("\nHere are the pizza places in your surrounding area!")
page = int(page_str)

delicious_pizza = pizza_spider(page, town.title(), state.upper())
# delicious_pizza = pizza_spider(1, 'Lexington', 'MA')
for place in delicious_pizza:
    print(place)
    print("\tAddress:", delicious_pizza[place]['address'])
    print("\tPhone:", delicious_pizza[place]['phone-number'])
    print("\tWebsite:", delicious_pizza[place]['website'])
    print()
