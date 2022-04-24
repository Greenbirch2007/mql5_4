


# https://www.mql5.com/zh/docs/integration/python_metatrader5

# 1. 取mt5数据 m60
# 2. 每10秒测试一次，close-open 大于80 ，就发送信号
# 3. 云服务器向手机微信发送通知
# Greenbirch6007
# NDUEg49ypandas
# 1. 60分钟超80点，通知微信 Nikkei225
# 2. 60分钟超60点，通知微信sp500
# 3. 60分钟超0.58点，通知微信sh_ag
import time
import random
from datetime import datetime
import MetaTrader5 as mt5
import os
import itchat
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
import pandas as pd
import pytz
def today_date():

    today_d = datetime.now().strftime("%Y-%m-%d")
    print(today_d.split("-"))
    year = int(today_d.split("-")[0])
    if len(today_d.split("-")[1]) ==2  and today_d.split("-")[1][0] !=0:
        month = int(today_d.split("-")[1])
    if len(today_d.split("-")[1]) ==2  and today_d.split("-")[1][0] ==0:
        month = int(today_d.split("-")[1][1])

    if len(today_d.split("-")[2]) ==2  and today_d.split("-")[2][0] !=0:
        day = int(today_d.split("-")[2])
    if len(today_d.split("-")[2]) ==2  and today_d.split("-")[2][0] ==0:
        day = int(today_d.split("-")[2][1])
    return year,month,day



class Logger():
    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

        # stdout
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # file
        logfilename = os.path.join(logpath,"{0}.log".format(datetime.now().strftime("%Y-%m-%d")))
        handler = handlers.RotatingFileHandler(filename = logfilename,
                                               maxBytes = 1048576,
                                               backupCount = 3)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# 设置锚文件，如果没有，就写入；如果有了，方向不对再写入，方向
def big_dt_function(tradeone,key_paramter):

    # 显示有关MetaTrader 5程序包的数据
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # 导入'pandas'模块，用于以表格形式显示获得的数据

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 6000)  # max table width to display
    # 导入用于处理时区的pytz模块

    def minum_60m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime60 = (string_datetime + datetime.timedelta(minutes=-60)).strftime("%Y-%m-%d %H:%M:%S")
        return startTime60

    def minum_59m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime59 = (string_datetime + datetime.timedelta(minutes=-59)).strftime("%Y-%m-%d %H:%M:%S")
        return startTime59
    def minum_58m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime58 = (string_datetime + datetime.timedelta(minutes=-58)).strftime("%Y-%m-%d %H:%M:%S")
        return startTime58
    def minum_57m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime57 = (string_datetime + datetime.timedelta(minutes=-57)).strftime("%Y-%m-%d %H:%M:%S")
        return startTime57





    # 建立与MetaTrader 5程序端的连接
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    year, month, day = today_date()
    utc_from = datetime(year, month, day, tzinfo=timezone)
    # request 100 000 EURUSD ticks starting from 10.01.6059 in UTC time zone
    ticks = mt5.copy_ticks_from(tradeone, utc_from, 600000, mt5.COPY_TICKS_ALL)
    print("Ticks received:", len(ticks))

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

    # create DataFrame out of the obtained data
    ticks_frame = pd.DataFrame(ticks)
    # 将时间（以秒为单位）转换为日期时间格式
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    # 整体处理 #直接 1000就好
    # 求一个平均差即可！如果！
    the_last_dt_3000 = ticks_frame.tail(3000)
    the_last_row = the_last_dt_3000.tail(1)
    last_time = str(list(the_last_row["time"])[0])


    _60_time = minum_60m(last_time)
    _59_time = minum_59m(last_time)
    _58_time = minum_58m(last_time)
    _57_time = minum_57m(last_time)
    the_first_row_60 = the_last_dt_3000.loc[the_last_dt_3000['time'] == "{0}".format(_60_time)]
    the_first_row_59 = the_last_dt_3000.loc[the_last_dt_3000['time'] == "{0}".format(_59_time)]
    the_first_row_58 = the_last_dt_3000.loc[the_last_dt_3000['time'] == "{0}".format(_58_time)]
    the_first_row_57 = the_last_dt_3000.loc[the_last_dt_3000['time'] == "{0}".format(_57_time)]

    def get_float_from_dataframe(df_content, attribute, the_last_row):
        if len(df_content.index) != 0:
            if len(df_content.index) == 1:
                dt = [x for x in df_content[attribute]][0]
            else:
                # loc[0] 返回第一行
                dt_1 = df_content.tail(1)
                dt = [x for x in dt_1[attribute]][0]
        else:
            dt = [x for x in the_last_row[attribute]][0]
        return float(dt)

    def choose_not_zero(list_content):
        not_zero_list = []
        for item in list_content:
            if str(item) != "0.0":
                not_zero_list.append(item)
        if not_zero_list != []:
            confirm_dt = random.choice(not_zero_list)
        else:
            confirm_dt = 0.0
        return confirm_dt
    def get_average_dt(bid_price, ask_price):
        average_price = (bid_price + ask_price) / 2
        return average_price

    last_average = get_average_dt(get_float_from_dataframe(the_last_row, "bid", the_last_row),
                                  get_float_from_dataframe(the_last_row, "ask", the_last_row))
    first_average_60 = get_average_dt(get_float_from_dataframe(the_first_row_60, "bid", the_last_row),get_float_from_dataframe(the_first_row_60, "ask", the_last_row))
    first_average_59 = get_average_dt(get_float_from_dataframe(the_first_row_59, "bid", the_last_row),get_float_from_dataframe(the_first_row_59, "ask", the_last_row))
    first_average_58 = get_average_dt(get_float_from_dataframe(the_first_row_58, "bid", the_last_row),get_float_from_dataframe(the_first_row_58, "ask", the_last_row))
    first_average_57 = get_average_dt(get_float_from_dataframe(the_first_row_57, "bid", the_last_row),get_float_from_dataframe(the_first_row_57, "ask", the_last_row))


    confirm_dt_60 = last_average - first_average_60
    confirm_dt_59 = last_average - first_average_59
    confirm_dt_58 = last_average - first_average_58
    confirm_dt_57 = last_average - first_average_57
    confirm_dt= choose_not_zero([confirm_dt_60,confirm_dt_59,confirm_dt_58,confirm_dt_57])


    print("-" * 60,"tradeone is ",tradeone, "data is :",confirm_dt, "-" * 60)
    if abs(confirm_dt) >= key_paramter and confirm_dt > 0 and os.path.exists('call{0}.txt'.format(tradeone)) is False:
        remove_existfile("put{0}.txt".format(tradeone))
        msg = "tradeone is {3} \n mt5 time :{2} \n time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),
                                                                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                      last_time,tradeone)
        # itchat.send("time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S")),'filehelper')
        send_msg_to_sb("敂敂", msg)
        log.debug(msg)

        open('call{0}.txt'.format(tradeone), mode='w')
    if abs(confirm_dt) >= key_paramter and confirm_dt < 0 and os.path.exists('put{0}.txt'.format(tradeone)) is False:
        remove_existfile("call{0}.txt".format(tradeone))
        # itchat.send("time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S")),'filehelper')
        msg = "tradeone is {3} \n mt5 time :{2} \n time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),
                                                                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                      last_time,tradeone)
        send_msg_to_sb("敂敂", msg)
        log.debug(msg)
        open('put{0}.txt'.format(tradeone), mode='w')



def send_msg_to_sb(username,msg):
    users=itchat.search_friends(username)
    userName= users[0]['UserName']
    print(userName)
    itchat.send(msg,toUserName=userName)


def mkdir(path):
    lpath=os.getcwd()
    isExists = os.path.exists(os.path.join(lpath,path))
    if not isExists:
        os.makedirs(path)
def remove_existfile(filename):
    if os.path.exists(filename):
        os.remove(filename)
if __name__=="__main__":
    mkdir("log")
    trade_dict = {
        "NI225": 100
        #"SP500m": 60
        #"XAGUSD": 0.58
    }

    for one_item in trade_dict.keys():
        remove_existfile("call{0}.txt".format(one_item))
        remove_existfile("put{0}.txt".format(one_item))
    logpath= os.path.join(os.getcwd(),"log")
    log= Logger()

    # 登录并获得QR码
    itchat.login()
    # 通过手机扫描QR码登录的微信号给“文件传输助手”发送消息“您好”
    while True:
        for item in trade_dict.keys():
            big_dt_function(item,trade_dict[item])
        # big_dt_function("SP500m",60)
        # big_dt_function("XAGUSD",0.58)
        time.sleep(random.choice((10, 11, 12, 13, 14, 15)))







