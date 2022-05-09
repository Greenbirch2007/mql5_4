
# 引入模块


import pandas as pd

d = [{"a":1,"vlanid":100},{"a":1,"vlanid":101},{"a":1,"vlanid":102},{"a":1,"vlanid":103}]


print([x for x in d if x["vlanid"]!=100])

df = pd.DataFrame(l)

# print(df)


def pdd(l):
    df = pd.DataFrame(l)
    return df

print(pdd(l)==df)
# True False