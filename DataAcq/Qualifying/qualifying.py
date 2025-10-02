import pandas as pd
import requests

base_url = "https://api.jolpi.ca/ergast/f1/"

# get all qualifying results from a given season
def get_quali_by_season(year: int):
    url = f"{base_url}{year}/qualifying/"
    response = requests.get(url)
    data = response.json()
    return data

# TODO: add functionality for "current", "last", and "next"
# get qualifying results from a given round in a given season
def get_quali_by_round(year: int, race: int):
    url = f"{base_url}{year}/{race}/qualifying/"
    response = requests.get(url)
    data = response.json()
    return data

# return qualifying results from a given circuit
def get_quali_by_circuit(circuit: str):
    url = f"{base_url}circuits/{circuit}/qualifying/"
    response = requests.get(url)
    data = response.json()
    return data

