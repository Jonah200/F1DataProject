import pandas as pd
import requests

base_url = "https://api.jolpi.ca/ergast/f1/drivers/"

def get_driver_personal_info(driverId):
    url = base_url + f"{driverId}/"
    response = requests.get(url)
    data = response.json()
    return data