import plotly.express as px
import pandas as pd

def generate_circuit_map(latitude: float, longitude: float, circuit_name: str):

    df = pd.DataFrame({
        "lat": [latitude],
        "lon": [longitude],
        "label": [f"<b>{circuit_name}</b>"]
    })

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        text='label',
        projection="orthographic",
    )

    fig.update_geos(
        projection_rotation=dict(lat=latitude, lon=longitude),
        showland=True,         # show land
        landcolor="rgb(1, 120, 15)",   # dark gray land
        showocean=True,        # show ocean
        oceancolor="rgb(0, 60, 150)",  # deep blue ocean
        showcountries=True,
        countrycolor="black",  # border color
        showlakes=True,
        lakecolor="rgb(0, 80, 160)",
        showframe=False,
        showcoastlines=False,
        coastlinecolor="black"
    )

    fig.update_traces(
        text=df['label'],
        mode='markers+text',
        marker=dict(
            size=20, 
            color="red",
            symbol='star'),
        textposition="top center",
        textfont=dict(size=25, color="white", family='Cambria'))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig.write_image("app/static/media/maps/map.png")
