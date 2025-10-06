import requests


def get_last_session_results():
    url = 'https://api.openf1.org/v1/session_result?session_key=latest'
    response = requests.get(url)
    data = response.json()
    return data

def get_last_session():
    url = 'https://api.openf1.org/v1/sessions?session_key=latest'
    response = requests.get(url)
    data = response.json()
    return data

