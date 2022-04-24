
# 引入模块


import pandas as pd

l =[1,2,3,4,5,6]

df = pd.DataFrame(l)

# print(df)


def pdd(l):
    df = pd.DataFrame(l)
    return df

print(pdd(l)==df)
# True False