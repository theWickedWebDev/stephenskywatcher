
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter

import astropy.units as u
from astropy.coordinates import EarthLocation, solar_system_ephemeris
from timezonefinder import TimezoneFinder

from sunpy.coordinates import sun
import pytz

def eclipse_times(time, lat, lon):
    location = EarthLocation.from_geodetic(lon*u.deg, lat*u.deg)
    # Define an array of observation times centered around the time of interest
    times = time + np.concatenate([np.arange(-120, -5) * u.min,
                                   np.arange(-300, 300) * u.s,
                                   np.arange(5, 121) * u.min])

    # Create an observer coordinate for the time array
    observer = location.get_itrs(times)

    # Calculate the eclipse amounts using a JPL ephemeris
    with solar_system_ephemeris.set('jpl'):
        amount = sun.eclipse_amount(observer)
        amount_minimum = sun.eclipse_amount(observer, moon_radius='minimum')

    tf = TimezoneFinder()  # reuse
    tz = tf.timezone_at(lng=lon, lat=lat)

    utc = dict()
    local = dict()

    # Calculate the start/end points of partial/total solar eclipse
    partial = np.flatnonzero(amount > 0)

    if len(partial) > 0:
        start_partial, end_partial = times[partial[[0, -1]]]
        start_partial_local = pytz.utc.localize(start_partial.datetime).astimezone(pytz.timezone(tz))
        end_partial_local = pytz.utc.localize(end_partial.datetime).astimezone(pytz.timezone(tz))
        utc.update({'start_partial': start_partial})
        utc.update({'end_partial': end_partial})
        local.update({'start_partial_local': start_partial_local})
        local.update({'end_partial_local': end_partial_local})
        total = np.flatnonzero(amount_minimum == 1)

        if len(total) > 0:
            start_total, end_total = times[total[[0, -1]]]
            start_total_local = pytz.utc.localize(start_total.datetime).astimezone(pytz.timezone(tz)) if start_total else None
            end_total_local = pytz.utc.localize(end_total.datetime).astimezone(pytz.timezone(tz)) if end_total else None
            utc.update({'start_total': start_total})
            utc.update({'end_total': end_total})
            local.update({'start_total_local': start_total_local})
            local.update({'end_total_local': end_total_local})
            
    return (utc, local)
