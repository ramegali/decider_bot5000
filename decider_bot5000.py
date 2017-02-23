# Created by Raphael Megali copyright 2017
# VERSION 1.1


# Known issue(s) with this code:
# >> ****FIXED**** Dictionary within dictionary is not working properly. Second dictionary's info
# 		is overriding information in all other dictionary entries so that
#		EVERY location ends up with the same website/address/phone.
# >> Check for invalid city/state

from sys import exit
from bs4 import BeautifulSoup
import random
import requests

def decider_bot():
	print "sigh . . ."
	print "This is Decider Bot..."
	print "I guess it's time to make a decision."
	ready_status = raw_input("Are you ready? ")
	if 'y' in ready_status:
		food_decision = what_food()
	else:
		print "Take your time... I'll be around if you need me...."
		exit()
	print "So... would you like me to search nearby places for", food_decision, "?"	
	ans = raw_input()
	if 'y' in ans:
		here_we_go(food_decision)
	else:
		print "Ok, fine."
		exit()

	print "Thank God that's finally over."

def what_food():
	food_choices = ['pizza', 'chinese', 'japanese', 'burgers', 'subs', 'italian', 'mexican',
					 'thai', 'greek', 'sushi', 'seafood']
	decision_index = random.randint(0, len(food_choices) - 1)
	food_decision = food_choices[decision_index]
	print "Okay\n\nHere's what I have decided for you:", food_decision
	return food_decision

def here_we_go(food_choice):
	print "Alright. I'm going to need the name of your town/city/whatever: "
	city = raw_input()
	state = raw_input("And your state, if you don't mind: ")
	number_of_pages = raw_input("How many pages of results would you like? ")
	number_of_pages = int(number_of_pages)

	print "Alright, I'll let Food Seeker Bot take it from here. . .\n\n"
	list_of_results = food_seeker_bot(city.title(), state.upper(), number_of_pages, food_choice)
	print "Thank you, Food Seeker Bot... Would you like to view Food Seeker Bot's full results (includes address, phone number, and link to webpage)?"
	ans = raw_input()
	if 'y' in ans:
		display_results(list_of_results)
	print "Would you like me to decide which of the above options to take?"
	ans = raw_input()
	if 'y' in ans:
		final_destination(list_of_results)
	else:
		print "Ok have fun making decisions on your own."
		exit()


def food_seeker_bot(city, state, number_of_pages, food_choice):
	list_of_results = {}
	page = 1

	print "HELLO THIS IS FOOD SEEKER BOT"
	print "PLEASE WAIT WHILE I SEEK YOUR FOODS"
	while page <= number_of_pages:
		print "\nPAGE", page
		if page is 1:
			url = 'http://www.yellowpages.com/search?search_terms=' + food_choice + '&geo_location_terms=' + city + '%2C+' + state
		else:
			url = 'http://www.yellowpages.com/search?search_terms=' + food_choice + '&geo_location_terms=' + city +'%2C%20' + state + '&page=' + str(page)
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text, "html.parser")
		# in findAll the 'a' flag stand for anchor which indicates where links are in html
		for link in soup.findAll('a', {'class':'business-name'}):
			href = "http://www.yellowpages.com" + link.get('href')
			title = link.string
			#print title  # <--- could be useful? basically a visual progress indicator
			if title is None:
				# gets rid of some addresses that don't work
				continue

			local_soup = soup_helper(href)
			website = get_url(local_soup)
			phone_num = get_phone(local_soup)
			address = get_address(local_soup)

			info = {} # this makes sure that info's data doesn't override every element in list_of_results
			info['address'] = address
			info['phone-number'] = phone_num
			info['website'] = website
			list_of_results[title] = info

		page += 1
	print "\nOKAY DONE\n\n"
	return list_of_results

def soup_helper(url): # returns a soup obj
    source_code = requests.get(url)
    plain_text = source_code.text
    return BeautifulSoup(plain_text, "html.parser")

def get_url(soup):
    for link in soup.findAll('a', {'class':'secondary-btn website-link'}):
        return link.get('href')

def get_phone(soup):
    for phone in soup.findAll('li', {'class':"phone primary"}):
        return phone.string

def get_address(soup):
    for i in soup.findAll('p', {'class':"adr"}):  # street name and num
        return i.string

def display_results(list_of_results):
	print "Here are the results: "
	for place in list_of_results:
		print place, "\n\tAddress: %s\n\tPhone: %s\n\tWebsite: %s\n" %(list_of_results[place]['address'],list_of_results[place]['phone-number'],list_of_results[place]['website'])
	print "\n\n"

def final_destination(list_of_results):
	final_destination = random.choice(list(list_of_results.items()))
	print "My final decision is ", final_destination, "\n\n"

decider_bot()
	
