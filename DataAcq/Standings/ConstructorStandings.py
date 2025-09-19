import requests
import json

baseUrl = "https://api.jolpi.ca/ergast/f1/"

def getConstructorStandingsByYear(year: int):
    url = baseUrl + f"{year}/constructorstandings"
    response = requests.get(url)
    return response.json()

def getConstructorStandingsByYearConstructor(year: int, constructor: str):
    url = baseUrl + f"{year}/constructors/{constructor}/constructorstandings"
    response = requests.get(url)
    return response.json()

def getConstructorStandingsByYearRound(year: int, round: int):
    url = baseUrl + f"{year}/{round}/constructorstandings"
    response = requests.get(url)
    return response.json()

def getConstructorStandingsByYearPosition(year: int, position: int):
    url = baseUrl + f"{year}/constructorstandings/{position}"
    response = requests.get(url)
    return response.json()

def getConstructorStandingsByYearRoundPosition(year: int, round: int, position: int):
    url = baseUrl + f"{year}/{round}/constructorstandings/{position}"
    response = requests.get(url)
    return response.json()

def getConstructorStandingsByYearRoundConstructor(year: int, round: int, constructor: str):
    url = baseUrl + f"{year}/{round}/constructors/{constructor}/constructorstandings"
    response = requests.get(url)
    return response.json()

print(json.dumps(getConstructorStandingsByYearRoundConstructor(2024,5,"ferrari")))