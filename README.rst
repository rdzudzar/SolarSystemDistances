Solar System Distances
=====================

|Streamlit|

Solar System Distances is a Web App that shows you how far are bodies in our Solar System away from each other.


Illustrations
-------------
Illustrations are my digital drawings, drawn in Procreate.



How to use
----------
Select a reference body - from which you want to measure distance to the other bodies in our Solar System.
At the start, date is always set to Today, but you can pick other day.



**Requirements:**
-----------------
Code is written in Python 3.11.7, below are the packages which are used in the code:
- ``streamlit >= 1.37.1``
- ``pandas >= 2.1.4``
- ``astropy >= 5.3.4``
- ``jplephem >= 2.22``


References
----------

This App is using Solar System Ephemerides (https://docs.astropy.org/en/latest/coordinates/solarsystem.html) from AstroPy (https://docs.astropy.org/en/latest/index.html) Python Library. For calculation, the default JPL ephemerides (DE430) are used, which are roughly valid for years between 1550 and 2650. Here is used function get_body() for reference body and then calculated 3D distance with separation_3d. Until a planetary scientist confirms that this kind of calculation is ok - take the distances with a grain of salt when using reference body that is not Earth :)



.. |Streamlit| image:: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
   :target: https://solar-system-distances.streamlit.app
   :alt: Streamlit App