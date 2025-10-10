import json
import requests

baseUrl = "https://api.jolpi.ca/ergast/f1/"

def getDriverStandingsByYear(year: int):
    url = baseUrl + f"{year}/driverstandings/"
    response = requests.get(url)
    return response.json()

def getDriverStandingsByYearRound(year: int, round: int):
    url = baseUrl + f"{year}/{round}/driverstandings"
    response = requests.get(url)
    return response.json()

def getDriverStandingsCurrent(year: int):
    url = baseUrl + f"{year}/last/driverstandings"
    response = requests.get(url)
    return response.json()

def getCurrentYearSingleDriverStandings(driverId: str):
    url = baseUrl + f"/current/drivers/{driverId}/driverstandings"
    response = requests.get(url)
    print(response.json())
    return response.json()