import requests
import json
import fastf1
import pandas as pd
import fastf1.plotting
from DataAcq.Drivers import drivers
from DataAcq.Races import Races

fastf1.plotting.setup_mpl(mpl_timedelta_support=True)


'https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315'

def get_telemetry(raceId: str, driver1: str, driver2: str):
    

    raceId = raceId.upper()
    print(raceId)
    session = fastf1.get_session(2025, raceId, "Q")
    session.load(telemetry=True, laps=True, weather=False)

    driver1 = session.laps.pick_drivers(driver1).pick_fastest().get_car_data().add_distance()
    driver2 = session.laps.pick_drivers(driver2).pick_fastest().get_car_data().add_distance()

    driver1["Time"] = pd.to_timedelta(driver1["Time"]).dt.total_seconds()
    driver2["Time"] = pd.to_timedelta(driver2["Time"]).dt.total_seconds()


    # leclerc['Time'] = leclerc['Time'].total_seconds()
    # verstappen['Time'] = verstappen['Time'].total_seconds()
    return driver1, driver2