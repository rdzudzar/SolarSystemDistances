# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 18:40:01 2025

@author: Rob
"""

import streamlit as st
import pandas as pd

from datetime import datetime, date
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body

import astropy

from PIL import Image
import requests
from io import BytesIO

st.set_page_config(layout="wide")
today = Time(datetime.now())

# Set background image
#def set_bg_image(image_url):
#    st.markdown(
#        f"""
#        <style>
#        .stApp {{
#            background-image: url({image_url});
#            background-size: cover;
#            background-position: center;
#            background-repeat: no-repeat;
#        }}
#        </style>
#        """,
#        unsafe_allow_html=True
#    )
#
#set_bg_image("")


dict_ss_objects = {
    "earth": "Earth",
    "sun": "Sun",
    "moon": "Moon",
    "mercury": "Mercury",
    "venus": "Venus",
    "mars": "Mars",
    "jupiter": "Jupiter",
    "saturn": "Saturn",
    "uranus": "Uranus",
    "neptune": "Neptune",
    "pluto": "Pluto"
}

d1, d2, d3 = st.columns([0.25,0.5,0.25])

with d2:
    st.title("Distances in Solar System")

    mini1, mini2 = st.columns([0.7,0.3])
        
    da = st.radio("Date Selection Options", ("Calendar", "Slider with current year"), horizontal=True)
    
    with mini1:
        if da == 'Calendar':
            pick_date = st.date_input("Pick a date", min_value=date(1900, 1, 1), value=datetime.today().date())
    
        if da == "Slider with current year":
    
            start_date = date(year=2025,month=1,day=1)
            end_date = date(year=2025,month=12,day=31)
            max_days = end_date-start_date
            
            pick_date = st.slider('Select date', min_value=start_date, value=datetime.today().date() ,max_value=end_date)
    
    
        # Convert date to datetime and then to Astropy Time
        pick_date = datetime.combine(pick_date, datetime.min.time())
        time_object = Time(pick_date)
    
    #with col2:
        main_ss_object = st.selectbox("Select Reference Body", 
                                      list(dict_ss_objects.values()))
    
selected_reference_object = next(key for key, value in dict_ss_objects.items() if value == main_ss_object)
    

def calculate_distances(selected_reference_object, time_object):
    """

    Parameters
    ----------
    dict_ss_objects_key : Value from dictionary
        Name of the SS object.
    date : Date from the streamlit input
        Initially will be todays date.

    Returns
    -------
    Dataframe with distances.

    """
    data = []
   # time_object = Time(pick_date)
    version = 'de430'
    #version = 'builtin'
    with solar_system_ephemeris.set(version):
        reference_body = get_body(selected_reference_object, time_object)
        
        for body_key, body_name in dict_ss_objects.items():
            
            # Exclude selected object
            if body_key != selected_reference_object: 
                body = get_body(body_key, time_object)
                
                # Distance in AU
                if version == 'de430':
                    distance_au = reference_body.separation_3d(body).value / 1000000 / 149.5978707
                if version == 'builtin':
                    distance_au = reference_body.separation_3d(body).value
                # Distance in million km
                distance_million_km = distance_au * 149.5978707
                
                data.append({
                    "Body": body_name,
                    "Distance [AU]": round(distance_au, 3) if distance_au < 1 else round(distance_au, 1),
                    "Distance [million km]": round(distance_million_km, 3) if distance_million_km < 1 else round(distance_million_km, 0)
                })
    
    df = pd.DataFrame(data)
    return df.sort_values(by="Distance [million km]").reset_index(drop=True)
    

# Calculate distances
df = calculate_distances(selected_reference_object, time_object)

# Images
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/290px-The_Earth_seen_from_Apollo_17.jpg"

planet_images = {
    "Moon": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Moon.png",
    "Sun": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Sun.png",
    "Earth": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Earth.png",
    "Mars": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Mars.png",
    "Venus": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Venus.png",
    "Mercury": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Mercury.png",
    "Jupiter": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Jupiter.png",
    "Saturn": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Saturn.png",
    "Uranus": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Uranus.png",
    "Neptune": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Naptune.png",
    "Pluto": "https://raw.githubusercontent.com/rdzudzar/SolarSystemDistances/refs/heads/main/illustrations/Pluto.png"

}


df['Image'] = df['Body'].map(planet_images)
df = df[['Image', 'Body', 'Distance [AU]', 'Distance [million km]']]



#t1, t2, t3 = st.columns(3)
with d2:
    st.write("Distances From Selected Reference Body to:")
    st.data_editor(
        df,
        column_config={
            "Image": st.column_config.ImageColumn("Image"),
            "Body": st.column_config.Column("Body"),
            "Distance [AU]": st.column_config.Column("[AU]"),
            "Distance [million km]": st.column_config.Column("[million km]"),
        },
        hide_index=True,
    )


df_sorted = df.sort_values(by="Distance [AU]")

with d2:
    orientation = st.radio("Orientation of images:", ("Horizontal", "Vertical"), horizontal=True)

if orientation == "Horizontal":
    
    # Images in one row
    num_columns = len(df_sorted)
    cols = st.columns(num_columns)
    
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        distance_au = str(row['Distance [AU]'])
        distance_km = str(row['Distance [million km]'])
        with cols[i]:
            st.image(row['Image'], caption=f"{row['Body']} - {distance_au} AU", width=150)
            
if orientation == "Vertical":
    i1, i2, i3 = st.columns(3)
    with i2:
        for _, row in df_sorted.iterrows():
            distance_au = str(row['Distance [AU]'])
            st.image(row['Image'], caption=f"{row['Body']} - {distance_au} AU", width=250)

st.subheader("References")
st.markdown(f"This App is using Solar [System Ephemerides](https://docs.astropy.org/en/latest/coordinates/solarsystem.html) from [AstroPy](https://docs.astropy.org/en/latest/index.html) Python Library, Version {astropy.__version__}.")
st.markdown("For calculation, the default JPL ephemerides (DE430) are used, which are roughly valid for years between 1550 and 2650. Here is used function get_body() for reference body and then calculated 3D distance with separation_3d.\
            Until a planetary scientist confirms that this kind of calculation is ok - take the distances with a grain of salt when using reference body that is not Earth :) ")
st.markdown("App made by Dr Robert Dzudzar. Illustrations are my digital drawings, drawn in Procreate. More of my illustrations can be seen on [BlueSky](https://bsky.app/profile/robertdzudzar.bsky.social)")
