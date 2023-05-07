# importing requests and json
import requests, json
import sys

# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = sys.argv[1]
API_KEY = "c90c9d642fccafced22c32c07db76133"
# upadting the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
# HTTP request
response = requests.get(URL)
# checking the status code of the request
if response.status_code == 200:
    # getting data in the json format
    data = response.json()
    # getting the main dict block
    main = data["main"]
    # getting temperature
    temperature = main["temp"]
    # getting the humidity
    humidity = main["humidity"]
    # getting the pressure
    pressure = main["pressure"]
    # weather report
    report = data["weather"]
    s = ""
    s += f"{temperature/10}" + "|"
    s += f"{humidity}" + "|"
    s += f"{pressure}" + "|"
    s += f"{report[0]['description']}" + "|"
    print(s)
else:
    # showing the error message
    print("Error in the HTTP request")
