import requests
import json

baseUrl = "https://api.jolpi.ca/ergast/f1/"

def getCircuitsByYear(year: int):
    url = baseUrl + f"{year}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

def getCircuitByRound(year: int, round: int):
    url = baseUrl + f"{year}/{round}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

def getCircuitByID(year: int, circuitid: str):
    url = baseUrl + f"{year}/circuits/{circuitid}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific constructor has participated in
def getCircuitsByConstructor(constructorid: str):
    url = baseUrl + f"constructors/{constructorid}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitsByDriver(driverid: str):
    url = baseUrl + f"drivers/{driverid}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitByDriver(driverid: str):
    url = baseUrl + f"drivers/{driverid}/circuits"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitsByStatus(statusid: str):
    url = baseUrl + f"status/{statusid}/circuits"
    response = requests.get(url)
    data = response.json()
    return data