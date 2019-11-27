
# %%
import pandas as pd
import math
import numpy as np


def distance(address: str, zip_code: str, ty_pe: str, time: int):
    # the function of calculating angles
    def angle(v1, v2):
        dx1 = v1[0]
        dy1 = v1[1]
        dx2 = v2[0]
        dy2 = v2[1]
        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180/math.pi)

        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180/math.pi)

        if angle1*angle2 >= 0:
            included_angle = abs(angle1-angle2)
        else:
            included_angle = abs(angle1) + abs(angle2)
            if included_angle > 180:
                included_angle = 360 - included_angle
        return included_angle

    cores = pd.read_csv("cores.csv")

    cores = cores.rename(columns={"Unnamed: 0": "Zip Code"})
    cores["Zip Code"] = cores["Zip Code"].astype(str)

    cores["Core"] = cores["Core"].map(lambda x: eval(x))

    from geopy.geocoders import Nominatim
    from geopy import distance

    geolocator = Nominatim(user_agent="distance")
    location = geolocator.geocode(address)
    # loc is the location of address
    loc = (location.longitude, location.latitude)

    core = cores[cores["Zip Code"] ==
                 zip_code]["Core"].iloc[0]  # the start point
    new = np.array(loc)-np.array(core)
    new = tuple(new)

    # import the coordinates of isochrone

    name = ty_pe.title()+" Area.csv"
    data = pd.read_csv(name, dtype={"Zip Code": str})
    data = data[data["Zip Code"] == zip_code]
    col = "Coors of "+str(time)+" mins"
    coors = data[col].iloc[0]
    coors = eval(coors)

    # the dot that in the direction of target wil have the smallest angle
    dots = []
    angles = []
    for i in range(len(coors)):
        a = np.array(coors[i])-np.array(core)
        dots.append(a)
        angles.append(angle(new, a))
    core_dist = distance.distance(loc, core).miles
    min_ind = angles.index(min(angles))
    that_dot = coors[min_ind]
    that_dist = distance.distance(that_dot, core).miles
    if core_dist < that_dist:
        that_dist = float("inf")

    return that_dist

# %%


print(distance("1440 G St NW Washington, DC 20005", "20005", "driving", 60))


# %%
print(distance("1440 G St NW Washington, DC 20005", "20001", "driving", 30))


# %%
