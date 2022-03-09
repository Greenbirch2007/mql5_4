


# import os
#
# base_file=''
#
# import itchat
#
# itchat.auto_login()
# def send_msg_to_sb(username,msg):
#     users=itchat.search_friends(username)
#     userName= users[0]['UserName']
#     print(userName)
#     itchat.send(msg,toUserName=userName)
#
# send_msg_to_sb("敂敂",msg)
# import os
# from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
# from datetime import datetime
# def mkdir(path):
#     lpath=os.getcwd()
#     isExists = os.path.exists(os.path.join(lpath,path))
#     if not isExists:
#         os.makedirs(path)
#
# mkdir("log")
# logpath= os.path.join(os.getcwd(),"log")
# class Logger:
#     def __init__(self, name=__name__):
#         self.logger = getLogger(name)
#         self.logger.setLevel(DEBUG)
#         formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")
#
#         # stdout
#         handler = StreamHandler()
#         handler.setLevel(DEBUG)
#         handler.setFormatter(formatter)
#         self.logger.addHandler(handler)
#
#         # file
#         logfilename = os.path.join(logpath,"{0}.log".format(datetime.now().strftime("%Y-%m-%d")))
#         handler = handlers.RotatingFileHandler(filename = logfilename,
#                                                maxBytes = 1048576,
#                                                backupCount = 3)
#         handler.setLevel(DEBUG)
#         handler.setFormatter(formatter)
#         self.logger.addHandler(handler)
#
#     def debug(self, msg):
#         self.logger.debug(msg)
#
#     def info(self, msg):
#         self.logger.info(msg)
#
#     def warn(self, msg):
#         self.logger.warning(msg)
#
#     def error(self, msg):
#         self.logger.error(msg)
#
#     def critical(self, msg):
#         self.logger.critical(msg)
# logfilename = os.path.join(logpath,"{0}.log".format(datetime.now().strftime("%Y-%m-%d")))
# log = Logger()
# log.debug("asdf")
# import datetime
# def today_date():
#
#     today_d = datetime.datetime.now().strftime("%Y-%m-%d")
#     print(today_d.split("-"))
#     year = int(today_d.split("-")[0])
#     if len(today_d.split("-")[1]) ==2  and today_d.split("-")[1][0] !=0:
#         month = int(today_d.split("-")[1])
#     if len(today_d.split("-")[1]) ==2  and today_d.split("-")[1][0] ==0:
#         month = int(today_d.split("-")[1][1])
#
#     if len(today_d.split("-")[2]) ==2  and today_d.split("-")[2][0] !=0:
#         day = int(today_d.split("-")[2])
#     if len(today_d.split("-")[2]) ==2  and today_d.split("-")[2][0] ==0:
#         day = int(today_d.split("-")[2][1])
#     return year,month,day
#
# year,month,day = today_date()

import random


print()

def choose_not_zero(list_content):
    not_zero_list =[]
    for item in list_content:
        if str(item) != "0.0":
            not_zero_list.append(item)
    if not_zero_list !=[]:
        confirm_dt = random.choice(not_zero_list)
    else:
        confirm_dt = 0.0
    return confirm_dt

