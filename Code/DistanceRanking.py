# %%
import pandas as pd
import numpy as np
from Ranking import ranking
import string
import random
from Distance import distance

# %%


def DistRank(address):
    zip_code = ['20001', '20002', '20003', '20004', '20005', '20006', '20007', '20008', '20009', '20010', '20011', '20012',
                '20015', '20016', '20017', '20018', '20019', '20020', '20024', '20032', '20036', '20037']
    # three types of isochrone
    types = ["driving", "cycling", "walking"]
    # time of isochrone
    times = [10, 30, 60]
    # add isochrone area to dataframe
    df = pd.DataFrame(zip_code, columns={"Zip Code"})

    from geopy.geocoders import Nominatim

    # create a random name of agent so that the service will not time out
    agent = "distance"+str(random.randint(0, 100))

    geolocator = Nominatim(user_agent=agent)
    location = geolocator.geocode(address)
    # loc is the location of address
    loc = (location.longitude, location.latitude)
    # zi_p is the zip code of address
    zi_p = (str.split(location.address, ",")[-2]).lstrip()

    for i in range(len(types)):
        ty_pe = types[i]
        for j in range(len(times)):
            time = times[j]
            name = 'Ranking of '+str(types[i])+" "+str(times[j])
            li_st = []
            for k in range(len(zip_code)):
                li_st.append(distance(loc, zip_code[k], ty_pe, time))

            df[name] = li_st
            df[name] = ranking(df[name])
            df.loc[df["Zip Code"] == zi_p, name] = 5
        name_col = str(ty_pe.title())+" Area"
        cols = []
        for m in df.columns:
            if ty_pe in str.split(m, " "):
                cols.append(m)

        df[name_col] = df[cols].apply(lambda x: x.sum(), axis=1)

        df[name_col] = ranking(df[name_col])

    return df


# %%
#DistRank("1440 G St NW Washington, DC 20005")


# %%
