

import os

def remove_existfile(filename):
    if os.path.exists(filename):
        os.remove(filename)


# trade_choice = ["NI225", "SP500m", "XAGUSD"]
# remove_existfile("call{0}.txt".format(x for x in trade_choice))
# remove_existfile("put{0}.txt".format(x for x in trade_choice))
#
# pip install pandas pytz




for  i in trade_dict.keys():
    print(trade_dict[i])