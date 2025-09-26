import requests
import json

baseUrl = "https://api.jolpi.ca/ergast/f1/"


# TODO: add functionality for current, last, etc within relevant functions

def getRacesByYear(year: int):
    url = baseUrl + f"{year}/races"
    response = requests.get(url)
    data = response.json()
    return data

def getRacesByRound(year: int, round: str):
    url = baseUrl + f"{year}/{round}/races"
    response = requests.get(url)
    data = response.json()
    return data