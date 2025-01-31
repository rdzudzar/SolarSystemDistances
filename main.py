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

st.set_page_config(layout="wide")
today = Time(datetime.now())

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
    "neptune": "Neptune"
}

d1, d2, d3 = st.columns([0.27,0.4,0.27])

with d2:
    st.title("Distances in Solar System")


    da = st.radio("Date Selection Options", ("Calendar", "Slider with current year"), horizontal=True)
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
    "Moon": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/290px-FullMoon2010.jpg",
    "Sun": "https://t2.gstatic.com/licensed-image?q=tbn:ANd9GcSC-tzajqpca4dchoeTCp8ChzFqdXnSnKtpkbx_5arltgIZQDdV4ALDa2ojaIHmI0GE",
    "Earth": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/290px-The_Earth_seen_from_Apollo_17.jpg",
    "Mars": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo0sfBghhyvJ0mC6ONbnM7wi1o_H484LZ9PA&s",
    "Venus": "https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcT6b03Qr3tnaBzlbznWySao6lYzR84Qw7kF-5DJ6C-3tWD_HB7yHI1dvHB4OwlWX7q-",
    "Mercury": "https://t3.gstatic.com/licensed-image?q=tbn:ANd9GcTFFRKg1XEC7kNu58XVZi9vPh6F9ii0FhevCdEAUKyMEtSdx4HLLLNBMacXXX0Y0gLv",
    "Jupiter": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/290px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg",
    "Saturn": "https://www.opticscentral.com.au/blog/wp-content/uploads/2023/07/main-pic-of-saturn-1024x614.png",
    "Uranus": "https://i.natgeofe.com/n/c1ee2a2c-b6c8-44ad-8e29-413a49732225/42912.jpg",
    "Neptune": "https://github.com/rdzudzar/SolarSystemDistances/blob/main/illustrations/Neptune.png"
}


df['Image'] = df['Body'].map(planet_images)
df = df[['Image', 'Body', 'Distance [AU]', 'Distance [million km]']]



#t1, t2, t3 = st.columns(3)
with d2:
    st.write("Distances From Selected Reference Body to:")
    st.data_editor(
        df,
        column_config={
            "Image": st.column_config.ImageColumn("Image", help="Astronomical object image"),
            "Body": st.column_config.Column("Body"),
            "Distance [AU]": st.column_config.Column("Distance [AU]"),
            "Distance [million km]": st.column_config.Column("Distance [million km]"),
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
st.markdown("Made by Dr Robert Dzudzar")
