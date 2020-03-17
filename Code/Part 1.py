# %%
import pandas as pd
import numpy as np
from DistanceRanking import DistRank, DistRank_F
from Ranking import ranking
from Distance import distance
import random

# %%
df = pd.read_csv("data.csv", dtype={"Zip Code": str})

# %%
# creating safety ranking dynamically after users select their preference


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing2(zip_code: str, grades_dict, data):

    grades = grades_dict

    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"] = grades.pop("Public Transportation")
    grades["Driving Area"] = grades.pop("Driving")
    grades["Cycling Area"] = grades.pop("Cycling")
    grades["Walking Area"] = grades.pop("Walking")
    grades["Driving Area of Family"] = grades["Driving Area"]
    grades["Cycling Area of Family"] = grades["Cycling Area"]
    grades["Walking Area of Family"] = grades["Walking Area"]
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

    nan = np.nan
    value_copy = [x for x in zip_score.values() if not np.isnan(x)]

    zip_score["Total"] = sum(value_copy)
    zip_score["Safety"] = zip_score.pop("Ranking of Crime")
    zip_score["Public Transportation"] = zip_score.pop(
        "Availability of Trains")
    zip_score["Driving"] = zip_score.pop("Driving Area")
    zip_score["Cycling"] = zip_score.pop("Cycling Area")
    zip_score["Walking"] = zip_score.pop("Walking Area")
    zip_score["Restaurant Delivery"] = zip_score.pop(
        "Ranking of Delivery Restaurant")
    zip_score["Child Care"] = zip_score.pop("Ranking of Child Care")
    zip_score["Elementary School"] = zip_score.pop(
        "Ranking of Elementary School")
    zip_score["Middle School"] = zip_score.pop("Ranking of Middle School")
    zip_score["High School"] = zip_score.pop("Ranking of High School")
    zip_score["Hospital"] = zip_score.pop("Ranking of Hospital")
    zip_score["Grocery | Freshness"] = zip_score.pop(
        "Ranking of Grocery|Freshness")
    zip_score["Grocery | Bargain"] = zip_score.pop(
        "Ranking of Grocery|Bargain")

    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Driving"] = grades.pop("Driving Area")
    grades["Cycling"] = grades.pop("Cycling Area")
    grades["Walking"] = grades.pop("Walking Area")
    grades["Restaurant Delivery"] = grades.pop(
        "Ranking of Delivery Restaurant")
    grades["Child Care"] = grades.pop("Ranking of Child Care")
    grades["Elementary School"] = grades.pop("Ranking of Elementary School")
    grades["Middle School"] = grades.pop("Ranking of Middle School")
    grades["High School"] = grades.pop("Ranking of High School")
    grades["Hospital"] = grades.pop("Ranking of Hospital")
    grades["Grocery | Freshness"] = grades.pop("Ranking of Grocery|Freshness")
    grades["Grocery | Bargain"] = grades.pop("Ranking of Grocery|Bargain")

    frame = pd.DataFrame(list(zip_score)).rename(columns={0: "Features"})
    frame["Area Score"] = zip_score.values()
    frame = frame[frame["Area Score"] != 0]

    return frame[frame["Features"] == "Total"]["Area Score"].iloc[0]


def select(user_type, age, income, safety, grades_dict, address=None, family_address=None, data=df):

    grades = grades_dict

    data = safety_consideration(safety, data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address != None:
        a = DistRank(address)
        data["Driving Area"] = a["Driving Area"]
        data["Cycling Area"] = a["Cycling Area"]
        data["Walking Area"] = a["Walking Area"]
    if family_address != None:
        data = data.merge(DistRank_F(family_address),
                          on="Zip Code", how="outer")
    else:
        data["Driving Area of Family"] = 0
        data["Cycling Area of Family"] = 0
        data["Walking Area of Family"] = 0

    if age < 55:
        thre = income*0.30
    else:
        thre = income*0.40

    if user_type == "Renter":
        data = data[(data["Rental for Studio"] < thre) | (
            data["Rental for 1 Bed"] < thre) | (data["Rental for 2 Beds"] < thre)].reset_index(drop=True)

        if len(data) > 0:

            for i in range(len(data)):
                grades_sub = grades
                data.loc[i, "Area Score"] = indexing2(
                    data["Zip Code"].loc[i], grades_sub, data)
            data = data.sort_values("Area Score", ascending=False)
    if user_type == "Home Buyer":
        data = data[(data["Price for Sale|Studio"] < thre) | (data["Price for Sale|1 Bed"] < thre) | (
            data["Price for Sale|2 Beds"] < thre)].reset_index(drop=True)

        if len(data) > 0:

            for i in range(len(data)):
                grades_sub = grades
                data.loc[i, "Area Score"] = indexing2(
                    data["Zip Code"].loc[i], grades_sub, data)

            data = data.sort_values("Area Score", ascending=False)

    data = data.drop("Unnamed: 0", axis=1)

    return data


# %%
dic = {}

dic["Availability of Bakery"] = 7
dic["Rating of Bakery"] = 5
dic["Price Level of Bakery"] = 2
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 2
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 3
dic["Rating of Cafe"] = 3
dic["Price Level of Cafe"] = 6
dic["Child Care"] = 4
dic["Elementary School"] = 5
dic["Middle School"] = 3
dic["High School"] = 2
dic["Hospital"] = 3
dic["Availability of Parks"] = 4
dic["Public Transportation"] = 10
dic["Availability of Pharmacy"] = 2
dic["Restaurant Delivery"] = 3
dic["Safety"] = 3
dic["Availability of Sports Facility"] = 8
dic["Driving"] = 10
dic["Walking"] = 6
dic["Cycling"] = 3
dic["Grocery | Freshness"] = 1
dic["Grocery | Bargain"] = 1


safety = ["Property | Theft",
          "Violent | Assault with Dangerous Weapon", "Violent | Homicide"]
# %%

bbb = select("Home Buyer", 45, 1000000, ["Violent | Homicide", "Property | Arson", "Violent | Sex Abuse"], dic,
             address="80 M St SE, Washington, DC 20003", family_address="1440 G st NW, Washington DC 20005", data=df)
print(bbb)
# %%


def select_stu(safety, grades_dict, school=None, data=df):
    data = safety_consideration(safety, data)
    address = school
    grades = grades_dict
    data["Driving Area of Family"] = 0
    data["Cycling Area of Family"] = 0
    data["Walking Area of Family"] = 0
    data = data.merge(DistRank(address), on=[
                      "Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")
    for i in range(len(data)):
        grades_sub = grades
        data.loc[i, "Area Score"] = indexing2(
            data["Zip Code"].loc[i], grades_sub, data)
    data = data.sort_values("Area Score", ascending=False)

    data = data.drop("Unnamed: 0", axis=1)

    return data


# %%

# %%

aa = select_stu(safety, dic, "The Georgetown University", df)
# print(aa)
