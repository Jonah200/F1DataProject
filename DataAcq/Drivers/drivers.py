import pandas as pd
import requests

base_url = "https://api.jolpi.ca/ergast/f1/"

# return all drivers who participated during a given season
def get_drivers_by_season(year: int):
    url = f"{base_url}{year}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return all drivers who participated in a given round of a given season
def get_drivers_by_round(year: int, race: int):
    url = f"{base_url}{year}/{race}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return all drivers who have driven at a given circuit
def get_drivers_by_circuit(circuit: str):
    url = f"{base_url}circuits/{circuit}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return all drivers who drove at a given circuit during a given season
def get_drivers_by_season_circuit(year: int, circuit: str):
    url = f"{base_url}{year}/circuits/{circuit}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return the driver with a given id
def get_drivers_by_id(driverId: str):
    url = f"{base_url}drivers/{driverId}"
    response = requests.get(url)
    data = response.json()
    return data

# returns drivers who finished a race with the nth fastest lap
def get_drivers_by_nth_lap(n: int):
    url = f"{base_url}fastest/{n}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data


def get_drivers_by_season_nth_lap(year: int, n: int):
    url = f"{base_url}{year}/fastest/{n}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

def get_drivers_by_round_nth_lap(year: int, race: int, n: int):
    url = f"{base_url}{year}/{race}/fastest/{n}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who have had a given grid position
def get_drivers_by_grid(grid: int):
    url = f"{base_url}grid/{grid}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who had a given grid position in a given year
def get_drivers_by_grid_year(grid: int, year: int):
    url = f"{base_url}{year}/grid/{grid}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return the driver with a given grid position in a given round of a given year
def get_drivers_by_grid_round(grid: int, year: int, race: int):
    url = f"{base_url}{year}/{race}/grid/{grid}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who achieved a given race position
def get_drivers_by_pos(pos: int):
    url = f"{base_url}results/{pos}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who achieved a given race position in a given year
def get_drivers_by_pos_year(pos: int, year: int):
    url = f"{base_url}{year}/results/{pos}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return the driver who achieved a given position during a given round of a given year
def get_drivers_by_pos_round(pos: int, year: int, race: int):
    url = f"{base_url}{year}/{race}/results/{pos}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who attained a given status in a race
def get_drivers_by_status(status: int):
    url = f"{base_url}status/{status}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who attained a given status in a given year
def get_drivers_by_status_year(status: int, year: int):
    url = f"{base_url}{year}/status/{status}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who attained a given status in a given round of a given year
def get_drivers_by_status_round(status: int, year: int, race: int):
    url = f"{base_url}{year}/{race}/status/{status}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return all drivers who have driven for a given constructor
def get_drivers_by_constructor(constructor: str):
    url = f"{base_url}constructors/{constructor}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return all drivers who have driven for a given constructor in a given year
def get_drivers_by_constructor_year(constructor: str, year: int):
    url = f"{base_url}{year}/constructors/{constructor}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return drivers who attained a given status during a given round of a given year
def get_drivers_by_status_round(constructor: int, year: int, race: int):
    url = f"{base_url}{year}/{race}/constructors/{constructor}/drivers/"
    response = requests.get(url)
    data = response.json()
    return data

# return info on a driver using their driver id
def get_driver_info(driverId):
    url = f"{base_url}{driverId}/"
    response = requests.get(url)
    data = response.json()
    return data

