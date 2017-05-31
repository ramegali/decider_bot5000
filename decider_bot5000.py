# Raphael Megali copyright 2017
# Version 2.0.1

# gonna have to hide the access token etc

from sys import exit
import requests
import random

app_id = '39FHtcp39Nb-Khyzt6S_fw'
app_secret = 'Gon9cUcLnZnecCwBvWEEP2rCPy5p9VTQabwfW9857k9l0ncLKbieRjw296U3Cia7'
access_token = 'jC7h77ZwjBZfsg90k0JkTs3AWcwU1i2P3jJPtZEnYGlCabGOiG5dJntMml4-bACEunICfkGdK-hYbgL_R8Qn1CdySDgRMIsviLMepTccLe_Kpspi5XLK6zu90pgQWXYx'  # token.json()['access_token']
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % access_token}


# Don't really need this section, at least not for now,
# since we already have the access token

# data = {'grant_type': 'client_credentials',
#        '39FHtcp39Nb-Khyzt6S_fw': app_id,
#        'Gon9cUcLnZnecCwBvWEEP2rCPy5p9VTQabwfW9857k9l0ncLKbieRjw296U3Cia7': app_secret}
# token = requests.post('https://api.yelp.com/oauth2/token', data=data)

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
              # 'sort_by': 'rating'
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
    i = 0
    print "Okay whatever, here they are: \n\n"
    for placesf in results:
        print "%s \n\tRATING: %s \n\tPRICE: %s \n\tADDRESS: %s, %s %s %s \n\tPHONE: %s \n" % (
            results[i]['name'], results[i]['rating'], results[i]['price'],
            results[i]['location']['address1'], results[i]['location']['city'], results[i]['location']['state'],
            results[i]['location']['zip_code'],
            results[i]['display_phone'])
        i += 1


def your_destiny(results):
    destiny = random.randint(0, len(results) - 1)
    print "Alright, here's what I picked for you I hope you're satisfied: %s\n" % (results[destiny]['name'])


if __name__ == "__main__":
    decider_bot()
