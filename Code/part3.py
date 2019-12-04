# %%
import pandas as pd
import numpy as np


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


# %%
dic = {}

dic["Availability of Bakery"] = 3
dic["Rating of Bakery"] = 4
dic["Price Level of Bakery"] = 2
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 2
dic["Price Level of Bar"] = 3
dic["Availability of Cafe"] = 3
dic["Rating of Cafe"] = 3
dic["Price Level of Cafe"] = 1
dic["Child Care"] = 4
dic["Elementary School"] = 5
dic["Middle School"] = 3
dic["High School"] = 2
dic["Hospital"] = 3
dic["Availability of Parks"] = 4
dic["Public Transportation"] = 3
dic["Availability of Pharmacy"] = 2
dic["Restaurant Delivery"] = 3
dic["Safety"] = 3
dic["Availability of Sports Facility"] = 1
dic["Traffic Situation"] = 5
dic["Grocery | Freshness"] = 1
dic["Grocery | Bargain"] = 1

# %%

aa = gov_sti("20002", dic, 300000, None, df)

# %%
aa[aa["Zip Code"] == "20005"]["Impact"].iloc[0]


# %%
