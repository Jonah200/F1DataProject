import pandas as pd
import requests

base_url = "https://api.jolpi.ca/ergast/f1/"

def get_constructors_by_season(year: int):
    url = f"{base_url}{year}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_round(year: int, race: int):
    url = f"{base_url}{year}/{race}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_circuit(circuit: str):
    url = f"{base_url}circuits/{circuit}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructor_by_id(constructor: str):
    url = f"{base_url}constructors/{constructor}/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_driver(driver: str):
    url = f"{base_url}drivers/{driver}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_grid(grid: int):
    url = f"{base_url}grid/{grid}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_result(result: int):
    url = f"{base_url}results/{result}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data

def get_constructors_by_status(status: int):
    url = f"{base_url}status/{status}/constructors/"
    response = requests.get(url)
    data = response.json()
    return data