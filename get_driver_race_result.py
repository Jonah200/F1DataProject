import pandas as pd
import requests

base_url = "https://api.jolpi.ca/ergast/f1/"
def get_driver_race_result(driverId, year, circuitId):
    url = f"{base_url}{year}/drivers/{driverId}/circuits/{circuitId}/results"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data

