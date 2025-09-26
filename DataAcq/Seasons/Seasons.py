import requests
import json

baseUrl = "https://api.jolpi.ca/ergast/f1/"

# TODO: add functionality for current, last, etc within relevant functions

def getSeason(year: int):
    url = baseUrl + f"{year}/seasons"
    response = requests.get(url)
    data = response.json()
    return data

def getSeasonsbyCircuit(circuitid: str):
    url = baseUrl + f"/circuits/{circuitid}/seasons"
    response = requests.get(url)
    data = response.json()
    return data

def getSeasonsbyConstructor(constructorid: str):
    url = baseUrl + f"/constructors/{constructorid}/seasons"
    response = requests.get(url)
    data = response.json()
    return data

def getSeasonsbyDriver(driverid: str):
    url = baseUrl + f"/drivers/{driverid}/seasons"
    response = requests.get(url)
    data = response.json()
    return data

