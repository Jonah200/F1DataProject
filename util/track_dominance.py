import fastf1 as ff1
from fastf1 import plotting
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import os


# Enable the cache by providing the name of the cache folder
# ff1.Cache.enable_cache('Cache')

# Setup plotting
plotting.setup_mpl()

def track_dominance(driver1, driver2, raceId, color1, color2):
    # Initial Parameters
    year= 2025
    
    # Session name abbreviation:
    # The code for the session to load Options are:
    # 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', and 'R'.
    # Default is 'R', which refers to Race.
    # full session name: 'Practice 1', 'Practice 2', 'Practice 3',
    # 'Sprint', 'Sprint Shootout', 'Qualifying', 'Race';
    event = 'Qualifying'

 

    session_event = ff1.get_session(year, raceId, event)
    session_event.load()

    drivers = [driver1, driver2]
    compare_drivers = session_event.laps[session_event.laps['Driver'].isin(drivers)]
    compare_drivers

    fastest_lap_driver01 = session_event.laps.pick_drivers(driver1).pick_fastest()
    fastest_lap_driver02 = session_event.laps.pick_drivers(driver2).pick_fastest()

    telemetry_driver01 = fastest_lap_driver01.get_telemetry().add_distance()
    telemetry_driver02 = fastest_lap_driver02.get_telemetry().add_distance()

    telemetry_driver01['Driver'] = driver1
    telemetry_driver02['Driver'] = driver2
    telemetry_drivers = pd.concat([telemetry_driver01, telemetry_driver02])

    # We want 25 mini-sectors (this can be adjusted up and down)
    num_minisectors = 7*3

    # Grab the maximum value of distance that is known in the telemetry
    total_distance = total_distance = max(telemetry_drivers['Distance'])

    # Generate equally sized mini-sectors
    minisector_length = total_distance / num_minisectors


    # Initiate minisector variable, with 0 (meters) as a starting point.
    minisectors = [0]

    # Add multiples of minisector_length to the minisectors
    for i in range(0, (num_minisectors - 1)):
        minisectors.append(minisector_length * (i + 1))

    telemetry_drivers['Minisector'] = telemetry_drivers['Distance'].apply(
        lambda dist: (
            int((dist // minisector_length) + 1)
        )
    )

    average_speed = telemetry_drivers.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

    average_speed

    # Select the driver with the highest average speed
    fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]

    # Get rid of the speed column and rename the driver column
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

    fastest_driver

    # Join the fastest driver per minisector with the full telemetry
    telemetry_drivers = telemetry_drivers.merge(fastest_driver, on=['Minisector'])

    # Order the data by distance to make matploblib does not get confused
    telemetry_drivers = telemetry_drivers.sort_values(by=['Distance'])

    # Convert driver name to integer
    telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == driver1, 'Fastest_driver_int'] = 1
    telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == driver2, 'Fastest_driver_int'] = 2

    x = np.array(telemetry_drivers['X'].values)
    y = np.array(telemetry_drivers['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fastest_driver_array = telemetry_drivers['Fastest_driver_int'].to_numpy().astype(float)

    
    cmap = ListedColormap([color1, color2])
    lc_comp = LineCollection(
        segments,
        norm=plt.Normalize(1, cmap.N + 1),
        cmap=cmap
    )
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    

    plt.rcParams['figure.figsize'] = [12, 6]

    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    # cbar = plt.colorbar(mappable=lc_comp, label='Driver', boundaries=np.arange(1,4))
    # cbar.set_ticks(np.arange(1.5, 3.5))
    # cbar.set_ticklabels([driver1,driver2])

    title_color = 'black' # '#6441a5'
    # plt.title(f"{year} {raceId} | {event} {driver1} vs {driver2}", color=title_color, fontsize = 16)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    file_path = "app/static/media/track_dominance/track_dominance.png"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    plt.savefig(
        file_path,
        bbox_inches='tight',   # trims extra whitespace
        pad_inches=0,          # no padding
        transparent=True,      # transparent background
        facecolor='none',
        edgecolor='none'
    )