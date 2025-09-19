import sys
import requests
import json

def getConstructorStandingsByYear(year: int):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/constructorstandings"
    response = requests.get(url)
    responseData = response.text
    return responseData

json.dump(getConstructorStandingsByYear(2025), sys.stdout)