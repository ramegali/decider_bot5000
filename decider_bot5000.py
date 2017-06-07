# Raphael Megali copyright 2017
# Version 2.1.1


from sys import exit, path
import requests, random
from client_credentials import access_token 

url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % access_token}

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
        filters = get_filters(food_decision)
    else:
        print "Ok, fine."
        exit()
    get_results(filters)
    print "Thank God that's finally over..."


def what_food():
    food_choices = ['pizza', 'chinese', 'japanese', 'burgers', 'subs', 'italian', 'mexican',
                    'thai', 'greek', 'sushi', 'seafood']
    decision_index = random.randint(0, len(food_choices) - 1)
    food_decision = food_choices[decision_index]
    print "Okay\n\nHere's what I have decided for you:", food_decision
    return food_decision


def get_filters(food_choice):
    filters = {}
    print "Alright. Well, I'm going to need some parameters before we begin..."
    location = raw_input("Please give me the zip code of the city/town where we're searching: ")
    price = raw_input("On a scale of 1 to 4, how pricy do you wanna get? ")
    # OTHER POSSIBILITIES INCLUDE:
    # sort_by <-- parameter to sort by best_match (default), rating, review_count, or distance
    # limit <-- number of businesses to return (default 20, max 50)
    # transactions <-- can the place do delivery, pickup, or restaurant_reservation?

    filters['location'] = location
    filters['price'] = price
    filters['term'] = food_choice
    return filters


def get_results(filters):
    params = {'location': filters['location'],
              'term': filters['term'],
              'pricing_filter': filters['price'],
              'sort_by': 'rating'
              }

    # get the info
    resp = requests.get(url=url, params=params, headers=headers)
    results = resp.json()['businesses']  # gets just the businesses
    print "Would you like to see the results? Or no?"
    ans = raw_input()
    if 'y' in ans:
        display_results(results)

    your_destiny(results)


def display_results(results):
    print "Okay whatever, here they are: \n\n"
    for places in results:
		print places['name']
		print "\tRATING: ", places['rating']
		try:
			print "\tPRICE: ", places['price']
		except:
			print "No pricing info available"
		print "\tADDRESS: ", places['location']['address1'], ", ", places['location']['city'], places['location']['state'], places['location']['zip_code']
		print "\tPHONE: ", places['display_phone'], "\n"

def your_destiny(results):
    destiny = random.randint(0, len(results) - 1)
    print "Alright, here's what I picked for you I hope you're satisfied: %s\n" % (results[destiny]['name'])


if __name__ == "__main__":
    decider_bot()
