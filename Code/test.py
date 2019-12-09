#%%

import pandas as pd
import numpy as np
from DistanceRanking import DistRank
from Ranking import ranking
from Distance import distance
import random
import string
import math

def distance(loc: tuple, zip_code: str, ty_pe: str, time: int):
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

    from geopy import distance

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

df = pd.read_csv("data.csv", dtype={"Zip Code": str})


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing2(zip_code: str, grades_dict, data):
    
    grades=grades_dict

    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"] = grades.pop("Public Transportation")
    grades["Driving Area"] = grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"] = grades.pop(
        "Restaurant Delivery")
    grades["Ranking of Child Care"] = grades.pop("Child Care")
    grades["Ranking of Elementary School"] = grades.pop("Elementary School")
    grades["Ranking of Middle School"] = grades.pop("Middle School")
    grades["Ranking of High School"] = grades.pop("High School")
    grades["Ranking of Hospital"] = grades.pop("Hospital")
    grades["Ranking of Grocery|Freshness"] = grades.pop("Grocery | Freshness")
    grades["Ranking of Grocery|Bargain"] = grades.pop("Grocery | Bargain")
    keys = list(grades)

    zip_data = data[data["Zip Code"] == zip_code]
    grade_sum = sum(grades.values())
    weights = np.array(list(grades.values()))/grade_sum
    zip_ranks = {}
    zip_score = {}
    for i in range(len(keys)):
        zip_ranks[keys[i]] = zip_data[keys[i]].iloc[0]
        zip_score[keys[i]] = weights[i]*zip_ranks[keys[i]]

    zip_score["Total"] = sum(zip_score.values())
    zip_score["Safety"] = zip_score.pop("Ranking of Crime")
    zip_score["Public Transportation"] = zip_score.pop("Availability of Trains")
    zip_score["Traffic Situation"] = zip_score.pop("Driving Area")
    zip_score["Restaurant Delivery"] = zip_score.pop("Ranking of Delivery Restaurant")
    zip_score["Child Care"] = zip_score.pop("Ranking of Child Care")
    zip_score["Elementary School"] = zip_score.pop("Ranking of Elementary School")
    zip_score["Middle School"] = zip_score.pop("Ranking of Middle School")
    zip_score["High School"] = zip_score.pop("Ranking of High School")
    zip_score["Hospital"] = zip_score.pop("Ranking of Hospital")
    zip_score["Grocery | Freshness"] = zip_score.pop("Ranking of Grocery|Freshness")
    zip_score["Grocery | Bargain"] = zip_score.pop("Ranking of Grocery|Bargain")


    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Traffic Situation"] = grades.pop("Driving Area")
    grades["Restaurant Delivery"] = grades.pop("Ranking of Delivery Restaurant")
    grades["Child Care"] = grades.pop("Ranking of Child Care")
    grades["Elementary School"] = grades.pop("Ranking of Elementary School")
    grades["Middle School"] = grades.pop("Ranking of Middle School")
    grades["High School"] = grades.pop("Ranking of High School")
    grades["Hospital"] = grades.pop("Ranking of Hospital")
    grades["Grocery | Freshness"] = grades.pop("Ranking of Grocery|Freshness")
    grades["Grocery | Bargain"] = grades.pop("Ranking of Grocery|Bargain")
    
    frame = pd.DataFrame(list(zip_score)).rename(columns={0: "Features"})
    
    frame["Area Score"]=zip_score.values()
    frame=frame[frame["Area Score"]!=0]



    return frame[frame["Features"]=="Total"]["Area Score"].iloc[0]


def select(user_type, age, income, safety, grades_dict,address=None,data=df):

    grades = grades_dict

    data = safety_consideration(safety, data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address != None:
        data = data.merge(DistRank(address), on=[
                          "Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")

    if age < 55:
        thre = income*0.30
    else:
        thre = income*0.40


    if user_type == "Renter":
        data = data[(data["Rental for Studio"] < thre) | (
            data["Rental for 1 Bed"] < thre) | (data["Rental for 2 Beds"] < thre)].reset_index(drop=True)

        if len(data)>0:

            for i in range(len(data)):
                grades_sub=grades
                data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)
            data=data.sort_values("Area Score",ascending=False)
    if user_type=="Home Buyer":
        
        if len(data)>0:

            for i in range(len(data)):
                grades_sub=grades
                data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)

            data=data.sort_values("Area Score",ascending=False)

    data=data.drop("Unnamed: 0",axis=1)

    return data


dic = {}

dic["Availability of Bakery"] = 3
dic["Rating of Bakery"] = 5
dic["Price Level of Bakery"] = 3
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 5
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 5
dic["Rating of Cafe"] = 5
dic["Price Level of Cafe"] = 0
dic["Child Care"] = 5
dic["Elementary School"] = 5
dic["Middle School"] = 5
dic["High School"] = 5
dic["Hospital"] = 5
dic["Availability of Parks"] = 5
dic["Public Transportation"] = 5
dic["Availability of Pharmacy"] = 5
dic["Restaurant Delivery"] = 5
dic["Safety"] = 5
dic["Availability of Sports Facility"] = 5
dic["Traffic Situation"] = 5
dic["Grocery | Freshness"] = 5
dic["Grocery | Bargain"] = 5



select("Home Buyer",30,200000,["Violent | Robbery","Violent | Assault with Dangerous Weapon","Violent | Homicide"],dic,address="1400 Crystal drive, Arlington, VA, 22202",data=df)

#%%

safety=["Property | Theft","Violent | Assault with Dangerous Weapon", "Violent | Homicide"]

def select_stu(safety,grades_dict,school=None,data=df):
    data=safety_consideration(safety,data)
    address=school
    grades=grades_dict
    data = data.merge(DistRank(address), on=["Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")
    for i in range(len(data)):
        grades_sub=grades
        data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)
    data=data.sort_values("Area Score",ascending=False)

    data=data.drop("Unnamed: 0",axis=1)

    return data
    


select_stu(safety,dic,"The Georgetown University",df)


#%%

df = pd.read_csv("data.csv", dtype={"Zip Code": str})


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing(cur_zip: str, new_zip: str, grades, safety, address=None):

    data = safety_consideration(safety, df)
    if address != None:
        data = data.merge(DistRank(address), on=[
                          "Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")

    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"] = grades.pop("Public Transportation")
    grades["Driving Area"] = grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"] = grades.pop(
        "Restaurant Delivery")
    grades["Ranking of Child Care"] = grades.pop("Child Care")
    grades["Ranking of Elementary School"] = grades.pop("Elementary School")
    grades["Ranking of Middle School"] = grades.pop("Middle School")
    grades["Ranking of High School"] = grades.pop("High School")
    grades["Ranking of Hospital"] = grades.pop("Hospital")
    grades["Ranking of Grocery|Freshness"] = grades.pop("Grocery | Freshness")
    grades["Ranking of Grocery|Bargain"] = grades.pop("Grocery | Bargain")
    keys = list(grades)

    cur_data = data[data["Zip Code"] == cur_zip]
    new_data = data[data["Zip Code"] == new_zip]
    grade_sum = sum(grades.values())
    weights = np.array(list(grades.values()))/grade_sum
    cur_ranks = {}
    new_ranks = {}
    cur_score = {}
    new_score = {}
    index = {}
    for i in range(len(keys)):
        cur_ranks[keys[i]] = cur_data[keys[i]].iloc[0]
        new_ranks[keys[i]] = new_data[keys[i]].iloc[0]
        cur_score[keys[i]] = weights[i]*cur_ranks[keys[i]]
        new_score[keys[i]] = weights[i]*new_ranks[keys[i]]
        index[keys[i]] = (new_score[keys[i]] -
                          cur_score[keys[i]])/cur_score[keys[i]]

    cur_score["Total"] = sum(cur_score.values())
    new_score["Total"] = sum(new_score.values())

    index["Safety"] = index.pop("Ranking of Crime")
    index["Public Transportation"] = index.pop("Availability of Trains")
    index["Traffic Situation"] = index.pop("Driving Area")
    index["Restaurant Delivery"] = index.pop("Ranking of Delivery Restaurant")
    index["Child Care"] = index.pop("Ranking of Child Care")
    index["Elementary School"] = index.pop("Ranking of Elementary School")
    index["Middle School"] = index.pop("Ranking of Middle School")
    index["High School"] = index.pop("Ranking of High School")
    index["Hospital"] = index.pop("Ranking of Hospital")
    index["Grocery | Freshness"] = index.pop("Ranking of Grocery|Freshness")
    index["Grocery | Bargain"] = index.pop("Ranking of Grocery|Bargain")
    index["Total"] = (new_score["Total"]-cur_score["Total"])/cur_score["Total"]

    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Traffic Situation"] = grades.pop("Driving Area")
    grades["Restaurant Delivery"] = grades.pop(
        "Ranking of Delivery Restaurant")
    grades["Child Care"] = grades.pop("Ranking of Child Care")
    grades["Elementary School"] = grades.pop("Ranking of Elementary School")
    grades["Middle School"] = grades.pop("Ranking of Middle School")
    grades["High School"] = grades.pop("Ranking of High School")
    grades["Hospital"] = grades.pop("Ranking of Hospital")
    grades["Grocery | Freshness"] = grades.pop("Ranking of Grocery|Freshness")
    grades["Grocery | Bargain"] = grades.pop("Ranking of Grocery|Bargain")

    frame = pd.DataFrame(list(index)).rename(columns={0: "Features"})
    frame["Current Score"] = cur_score.values()
    frame["New Score"] = new_score.values()
    frame["Change"] = index.values()
    frame=frame[frame["Current Score"]!=0]

    return frame


dic = {}

dic["Availability of Bakery"] = 1
dic["Rating of Bakery"] = 1
dic["Price Level of Bakery"] = 1
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 4
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 5
dic["Rating of Cafe"] = 5
dic["Price Level of Cafe"] = 0
dic["Child Care"] = 5
dic["Elementary School"] = 5
dic["Middle School"] = 5
dic["High School"] = 5
dic["Hospital"] = 4
dic["Availability of Parks"] = 3
dic["Public Transportation"] = 5
dic["Availability of Pharmacy"] = 5
dic["Restaurant Delivery"] = 4
dic["Safety"] = 5
dic["Availability of Sports Facility"] = 1
dic["Traffic Situation"] = 5
dic["Grocery | Freshness"] = 5
dic["Grocery | Bargain"] = 2

safety = ["Property | Burglary","Violent | Assault with Dangerous Weapon","Violent | Homicide"]

indexing("20001", "20016", dic, safety, "1440 G st, NW, Washington DC, 20005")


#%%

df = pd.read_csv("data.csv", dtype={"Zip Code": str})


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing3(cur_zip: str, new_zip: str, grades, data):

    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"] = grades.pop("Public Transportation")
    grades["Driving Area"] = grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"] = grades.pop(
        "Restaurant Delivery")
    grades["Ranking of Child Care"] = grades.pop("Child Care")
    grades["Ranking of Elementary School"] = grades.pop("Elementary School")
    grades["Ranking of Middle School"] = grades.pop("Middle School")
    grades["Ranking of High School"] = grades.pop("High School")
    grades["Ranking of Hospital"] = grades.pop("Hospital")
    grades["Ranking of Grocery|Freshness"] = grades.pop("Grocery | Freshness")
    grades["Ranking of Grocery|Bargain"] = grades.pop("Grocery | Bargain")
    keys = list(grades)

    # add the columns of rentals
    cols = []
    for m in df.columns:
        if "Rental" in str.split(m, " "):
            cols.append(m)

    keys.extend(cols)

    cur_data = data[data["Zip Code"] == cur_zip]
    new_data = data[data["Zip Code"] == new_zip]
    grade_sum = sum(grades.values())
    weights = np.array(list(grades.values()))/grade_sum
    cur_ranks = {}
    new_ranks = {}
    cur_score = {}
    new_score = {}
    index = {}

    sub_keys = [(key) for key in keys if key not in cols]

    for i in range(len(sub_keys)):
        cur_ranks[sub_keys[i]] = cur_data[sub_keys[i]].iloc[0]
        new_ranks[sub_keys[i]] = new_data[sub_keys[i]].iloc[0]
        cur_score[sub_keys[i]] = weights[i]*cur_ranks[sub_keys[i]]
        new_score[sub_keys[i]] = weights[i]*new_ranks[sub_keys[i]]
        index[sub_keys[i]] = (new_score[sub_keys[i]] -
                              cur_score[sub_keys[i]])/cur_score[sub_keys[i]]

    cur_score["Total"] = sum(
        {key: value for key, value in cur_score.items() if key not in cols}.values())
    new_score["Total"] = sum(
        {key: value for key, value in new_score.items() if key not in cols}.values())

    index["Safety"] = index.pop("Ranking of Crime")
    index["Public Transportation"] = index.pop("Availability of Trains")
    index["Traffic Situation"] = index.pop("Driving Area")
    index["Restaurant Delivery"] = index.pop("Ranking of Delivery Restaurant")
    index["Child Care"] = index.pop("Ranking of Child Care")
    index["Elementary School"] = index.pop("Ranking of Elementary School")
    index["Middle School"] = index.pop("Ranking of Middle School")
    index["High School"] = index.pop("Ranking of High School")
    index["Hospital"] = index.pop("Ranking of Hospital")
    index["Grocery | Freshness"] = index.pop("Ranking of Grocery|Freshness")
    index["Grocery | Bargain"] = index.pop("Ranking of Grocery|Bargain")
    index["Total"] = (new_score["Total"]-cur_score["Total"])/cur_score["Total"]

    for col in cols:
        cur_ranks[col] = cur_data[col].iloc[0]
        new_ranks[col] = new_data[col].iloc[0]
        cur_score[col] = cur_ranks[col]
        new_score[col] = new_ranks[col]
        index[col] = (new_score[col] -
                      cur_score[col])/cur_score[col]

    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Traffic Situation"] = grades.pop("Driving Area")
    grades["Restaurant Delivery"] = grades.pop(
        "Ranking of Delivery Restaurant")
    grades["Child Care"] = grades.pop("Ranking of Child Care")
    grades["Elementary School"] = grades.pop("Ranking of Elementary School")
    grades["Middle School"] = grades.pop("Ranking of Middle School")
    grades["High School"] = grades.pop("Ranking of High School")
    grades["Hospital"] = grades.pop("Ranking of Hospital")
    grades["Grocery | Freshness"] = grades.pop("Ranking of Grocery|Freshness")
    grades["Grocery | Bargain"] = grades.pop("Ranking of Grocery|Bargain")

    frame = pd.DataFrame(list(index)).rename(columns={0: "Features"})
    frame["Current Score"] = cur_score.values()
    frame["New Score"] = new_score.values()
    frame["Change"] = index.values()
    frame=frame[frame["Current Score"]!=0]

    return frame


def gov_sti(zip_code: str, needs: dict, afford: float, address=None, data=df):

    thre = afford*0.3

    data = data[(data["Rental for Studio"] < thre) | (
        data["Rental for 1 Bed"] < thre) | (data["Rental for 2 Beds"] < thre)].reset_index(drop=True)

    zip_codes = data["Zip Code"].unique()
    data = safety_consideration(safety, data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address != None:
        data = data.merge(DistRank(address), on=[
                          "Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")

    # changes = pd.DataFrame(zip_codes, columns="Zip Code")
    changes = []
    change = pd.DataFrame(zip_codes, columns=["Zip Code"])
    for i in range(len(zip_codes)):
        needs_sub = needs
        changes.append(indexing3(zip_code, zip_codes[i], needs_sub, data))
    change["Impact"] = changes
    return change



dic = {}

dic["Availability of Bakery"] = 1
dic["Rating of Bakery"] = 1
dic["Price Level of Bakery"] = 1
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 4
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 0
dic["Rating of Cafe"] = 0
dic["Price Level of Cafe"] = 0
dic["Child Care"] = 5
dic["Elementary School"] = 5
dic["Middle School"] = 5
dic["High School"] = 5
dic["Hospital"] = 4
dic["Availability of Parks"] = 3
dic["Public Transportation"] = 5
dic["Availability of Pharmacy"] = 5
dic["Restaurant Delivery"] = 4
dic["Safety"] = 5
dic["Availability of Sports Facility"] = 1
dic["Traffic Situation"] = 5
dic["Grocery | Freshness"] = 5
dic["Grocery | Bargain"] = 2


aa = gov_sti("20002", dic, 30000, None, df)
aa
#aa[aa["Zip Code"] == "20005"]["Impact"].iloc[0]


# %%
aa[aa["Zip Code"] == "20005"]["Impact"].iloc[0]

# %%


# %%
