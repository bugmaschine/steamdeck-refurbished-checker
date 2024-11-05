from time import gmtime, strftime
import requests
from discord_webhook import DiscordWebhook
import time
import os

# The country we want check for availability
# List of possibilities here https://github.com/RudeySH/SteamCountries/blob/master/json/countries.json
country_code = 'DE'

# This is the endpoint to check availability
url = 'https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1?origin=https:%2F%2Fstore.steampowered.com&country_code='+country_code+'&packageid=' #64gb


# The webhook we'll send updates to
webhook = None

def superduperscraper (version, urlSuffix) :
    oldvalue = ""
    # previous availability is stored in a file
    # we get the value before checking here
    filename = version + "_" + country_code + ".txt"
    if (os.path.isfile(filename)):
        file_read = open(filename, "r")
        oldvalue = file_read.read()
        file_read.close()
    print("ov: "+ oldvalue)

    # make the request to steam to see if the steam deck is available
    response = requests.get(url+urlSuffix)
    # True / False depending on if it's available or not
    availability = str(response.json()["response"]["inventory_available"])
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " >> "+version+ "-" + country_code + " Result: " + availability + " | raw: " + str(response.text))
    # save the new availability to the same file as above
    file = open(filename, "w")
    file.write(availability)
    file.close()

    # maybe move this somewhere else

    # if the new availability is different form the old one
    if oldvalue != availability and oldvalue != None :
        # and if it's available send a positive message to discord
        if availability == "True" :
            webhook.content = "refurbished "+version+ "-" + country_code + " steam deck available"
            webhook.execute()
        # if not send a negative message
        else:
            webhook.content = "refurbished "+version+ "-" + country_code + " steam deck not available"
            webhook.execute()

if (__name__ == "__main__"):
    # get webhook from env
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    if webhook_url == None:
        print("Webhook url not set")
        os._exit(1)
    # we have to set this here so we can send stuff
    webhook = DiscordWebhook(url=webhook_url, content="error")


    # The numbers are the individual ids for the refurbished steam deck
    # Got these form steamdb, you can probably add normal steam decks as well
    superduperscraper("64", "903905")
    superduperscraper("256", "903906")
    superduperscraper("512", "903907")
