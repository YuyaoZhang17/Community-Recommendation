
# %%
import pandas as pd
import numpy as np
from DistanceRanking import DistRank, DistRank_F
from Ranking import ranking
from Distance import distance
import random

# %%
df = pd.read_csv("data.csv", dtype={"Zip Code": str})


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing(cur_zip: str, new_zip: str, grades, safety, address=None, family_address=None):

    data = safety_consideration(safety, df)
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

    nan = np.nan
    cur_copy = [x for x in cur_score.values() if not np.isnan(x)]

    new_copy = [x for x in new_score.values() if not np.isnan(x)]

    cur_score["Total"] = sum(cur_copy)
    new_score["Total"] = sum(new_copy)

    index["Safety"] = index.pop("Ranking of Crime")
    index["Public Transportation"] = index.pop("Availability of Trains")
    index["Driving"] = index.pop("Driving Area")
    index["Cycling"] = index.pop("Cycling Area")
    index["Walking"] = index.pop("Walking Area")
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

    frame = pd.DataFrame(list(index)).rename(columns={0: "Features"})
    frame["Current Score"] = cur_score.values()
    frame["New Score"] = new_score.values()
    frame["Change"] = index.values()
    frame = frame[frame["Current Score"] != 0]

    return frame


# %%
dic = {}

dic["Availability of Bakery"] = 5
dic["Rating of Bakery"] = 5
dic["Price Level of Bakery"] = 3
dic["Availability of Bar"] = 4
dic["Rating of Bar"] = 0
dic["Price Level of Bar"] = 2
dic["Availability of Cafe"] = 5
dic["Rating of Cafe"] = 4
dic["Price Level of Cafe"] = 2
dic["Child Care"] = 3
dic["Elementary School"] = 5
dic["Middle School"] = 3
dic["High School"] = 8
dic["Hospital"] = 3
dic["Availability of Parks"] = 4
dic["Public Transportation"] = 5
dic["Availability of Pharmacy"] = 0
dic["Restaurant Delivery"] = 5
dic["Safety"] = 3
dic["Availability of Sports Facility"] = 10
dic["Driving"] = 10
dic["Cycling"] = 6
dic["Walking"] = 3
dic["Grocery | Freshness"] = 5
dic["Grocery | Bargain"] = 3

safety = ["Property | Theft",
          "Violent | Assault with Dangerous Weapon", "Violent | Homicide"]

# %%
aa = indexing("20032", "20024", dic, safety,
              "80 M St SE, Washington, DC 20003", "1440 G ST NW, Washington DC 20005")
print(aa)

# %%
