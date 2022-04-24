# import os
# #
# # from _60m100_affirmS_tradechoice import *
# #
# # trade_dict = {
# #     "NI225": 100
# #     # "SP500m": 60
# #     # "XAGUSD": 0.58
# # }
# def remove_file(filetype):
#     for file in os.listdir("."):
#         file_list = file.split(".")
#         if len(file_list) != 1:
#             if file.split(".")[1] == filetype:
#                 os.remove(file)
#
# remove_txtifile("txt")

import os
def confirm_file_exist_or_not():
    type_list = []

    for file in os.listdir("."):
        file_list = file.split(".")
        if len(file_list) !=1:
            type_list.append(file.split(".")[1])
    if "txt" in type_list:
        return True
    else:
        return False






    #     print(file)
print(confirm_file_exist_or_not())