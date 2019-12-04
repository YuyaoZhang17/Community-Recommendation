# %%
import numpy as np


def ranking(data):
    data2 = data.drop_duplicates(keep='first', inplace=False).dropna()
    return data.map(lambda x: 5 if x > np.nanpercentile(data2, 80)
                    else (4 if np.nanpercentile(data2, 60) < x <= np.nanpercentile(data2, 80)
                          else (3 if np.nanpercentile(data2, 40) < x <= np.nanpercentile(data2, 60)
                                else (2 if np.nanpercentile(data2, 20) < x <= np.nanpercentile(data2, 40)
                                      else (1)))))


# %%
