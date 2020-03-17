# %%
import pandas as pd
import numpy as np
from Ranking import ranking
from DistanceRanking import DistRank, DistRank_F


# %%

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
    grades["Driving Area"] = grades.pop("Driving")
    grades["Cycling Area"] = grades.pop("Cycling")
    grades["Walking Area"] = grades.pop("Walking")
    grades["Driving Area of Family"] = grades.pop("Driving of Family")
    grades["Cycling Area of Family"] = grades.pop("Cycling of Family")
    grades["Walking Area of Family"] = grades.pop("Walking of Family")
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

    cur_selected = {key: value for key,
                    value in cur_score.items() if key not in cols}

    new_selected = {key: value for key,
                    value in new_score.items() if key not in cols}

    cur_copy = [x for x in cur_selected.values() if not np.isnan(x)]

    new_copy = [x for x in new_selected.values() if not np.isnan(x)]

    cur_score["Total"] = sum(cur_copy)

    new_score["Total"] = sum(new_copy)

    index["Safety"] = index.pop("Ranking of Crime")
    index["Public Transportation"] = index.pop("Availability of Trains")
    index["Driving"] = index.pop("Driving Area")
    index["Cycling"] = index.pop("Cycling Area")
    index["Walking"] = index.pop("Walking Area")
    index["Driving of Family"] = index.pop("Driving Area of Family")
    index["Cycling of Family"] = index.pop("Cycling Area of Family")
    index["Walking of Family"] = index.pop("Walking Area of Family")
    index["Restaurant Delivery"] = index.pop("Ranking of Delivery Restaurant")
    index["Child Care"] = index.pop("Ranking of Child Care")
    index["Elementary School"] = index.pop("Ranking of Elementary School")
    index["Middle School"] = index.pop("Ranking of Middle School")
    index["High School"] = index.pop("Ranking of High School")
    index["Hospital"] = index.pop("Ranking of Hospital")
    index["Grocery | Freshness"] = index.pop("Ranking of Grocery|Freshness")
    index["Grocery | Bargain"] = index.pop("Ranking of Grocery|Bargain")
    index["Total"] = (new_score["Total"] -
                      cur_score["Total"])/cur_score["Total"]

    for col in cols:
        cur_ranks[col] = cur_data[col].iloc[0]
        new_ranks[col] = new_data[col].iloc[0]
        cur_score[col] = cur_ranks[col]
        new_score[col] = new_ranks[col]
        index[col] = (new_score[col] -
                      cur_score[col])/cur_score[col]

    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Driving"] = grades.pop("Driving Area")
    grades["Cycling"] = grades.pop("Cycling Area")
    grades["Walking"] = grades.pop("Walking Area")
    grades["Driving of Family"] = grades.pop("Driving Area of Family")
    grades["Cycling of Family"] = grades.pop("Cycling Area of Family")
    grades["Walking of Family"] = grades.pop("Walking Area of Family")
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


def gov_sti(zip_code: str, needs: dict, afford: float, address=None, family_address=None, data=df):

    thre = afford*0.3

    data = data[(data["Rental for Studio"] < thre) | (
        data["Rental for 1 Bed"] < thre) | (data["Rental for 2 Beds"] < thre)].reset_index(drop=True)

    zip_codes = data["Zip Code"].unique()
    data = safety_consideration(safety, data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address != None:
        a = DistRank(address)
        data["Driving Area"] = a["Driving Area"]
        data["Cycling Area"] = a["Cycling Area"]
        data["Walking Area"] = a["Walking Area"]

    else:
        data = data

    if family_address != None:
        data = data.merge(DistRank_F(family_address)[["Zip Code", "Driving Area of Family", "Cycling Area of Family", "Walking Area of Family"]],
                          on="Zip Code")
    else:
        data["Driving Area of Family"] = 0
        data["Cycling Area of Family"] = 0
        data["Walking Area of Family"] = 0

    # changes = pd.DataFrame(zip_codes, columns="Zip Code")
    changes = []
    change = pd.DataFrame(zip_codes, columns=["Zip Code"])
    for i in range(len(zip_codes)):
        needs_sub = needs
        changes.append(indexing3(zip_code, zip_codes[i], needs_sub, data))
    change["Impact"] = changes
    return change


# %%
dic = {}

dic["Availability of Bakery"] = 0
dic["Rating of Bakery"] = 0
dic["Price Level of Bakery"] = 0
dic["Availability of Bar"] = 0
dic["Rating of Bar"] = 0
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 0
dic["Rating of Cafe"] = 0
dic["Price Level of Cafe"] = 0
dic["Child Care"] = 10
dic["Elementary School"] = 10
dic["Middle School"] = 10
dic["High School"] = 10
dic["Hospital"] = 10
dic["Availability of Parks"] = 10
dic["Public Transportation"] = 10
dic["Availability of Pharmacy"] = 10
dic["Restaurant Delivery"] = 0
dic["Safety"] = 10
dic["Availability of Sports Facility"] = 0
dic["Driving"] = 0
dic["Cycling"] = 0
dic["Walking"] = 10
dic["Driving of Family"] = dic["Driving"]
dic["Cycling of Family"] = dic["Cycling"]
dic["Walking of Family"] = dic["Walking"]
dic["Grocery | Freshness"] = 0
dic["Grocery | Bargain"] = 10


safety = ["Violent | Sex Abuse",
          "Violent | Assault with Dangerous Weapon", "Violent | Homicide"]


df = safety_consideration(safety, df)
# %%

aa = gov_sti("20032", dic, 36400, address="1440 G st NW, Washington DC 20005",
             family_address="1440 G st NW, Washington DC 20005", data=df)

# %%
b = aa[aa["Zip Code"] == "20020"]["Impact"].iloc[0]
print(b)
