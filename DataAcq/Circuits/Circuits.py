import requests
import json

def getCircuitsByYear(year: int):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/circuit.json"
    response = requests.get(url)
    data = response.json()
    return data

def getCircuitByRound(year: int, round: int):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/{round}/circuit.json"
    response = requests.get(url)
    data = response.json()
    return data

def getCircuitByID(year: int, circuitid: str):
    url = f"https://api.jolpi.ca/ergast/f1/{year}/circuits/{circuitid}/circuits.json"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific constructor has participated in
def getCircuitsByConstructor(constructorid: str):
    url = f"https://api.jolpi.ca/ergast/f1/constructors/{constructorid}/circuits.json"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitsByDriver(driverid: str):
    url = f"https://api.jolpi.ca/ergast/f1/drivers/{driverid}/circuits.json"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitByDriver(driverid: str):
    url = f"https://api.jolpi.ca/ergast/f1/drivers/{driverid}/circuits.json"
    response = requests.get(url)
    data = response.json()
    return data

# returns circuits that a specific driver has participated in
def getCircuitsByStatus(statusid: str):
    url = f"https://api.jolpi.ca/ergast/f1/status/{statusid}/circuits.json"
    response = requests.get(url)
    data = response.json()
    return data