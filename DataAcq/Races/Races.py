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

def getLastRace():
    url = baseUrl + "current/last/races/"
    response = requests.get(url)
    data = response.json()
    return data

def getCurrentYearRaceNames() -> list:
    url = baseUrl + "current/races/"
    response = requests.get(url)
    data = response.json()
    races = data['MRData']['RaceTable']['Races']
    race_list = [race['raceName'] for race in races]
    return race_list

def getSessionByYearCircuit(circuit: str, year: int):
    url = f"https://api.openf1.org/v1/sessions?year={year}&circuit_short_name={circuit}"
    response = requests.get(url)
    data = response.json()
    return data

def getRaceResultBySessionKey(session_key: int):
    url = f"https://api.openf1.org/v1/session_result?session_key={session_key}"
    response = requests.get(url)
    data = response.json()
    return data

def getRaceResultByYearCircuit(year: int, circuitId: str):
    url = baseUrl + f"{year}/circuits/{circuitId}/results/"
    response = requests.get(url)
    data = response.json()
    return data
