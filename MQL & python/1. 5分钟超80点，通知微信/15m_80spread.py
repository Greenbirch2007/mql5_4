


# https://www.mql5.com/zh/docs/integration/python_metatrader5

# 1. 取mt5数据 m15
# 2. 每10秒测试一次，close-open 大于80 ，就发送信号
# 3. 云服务器向手机微信发送通知
# Greenbirch2007
# NDUEg49y
import time
from datetime import datetime
import MetaTrader5 as mt5
import os



# 设置锚文件，如果没有，就写入；如果有了，方向不对再写入，方向
def big_dt_function():
    # 显示有关MetaTrader 5程序包的数据
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # 导入'pandas'模块，用于以表格形式显示获得的数据
    import pandas as pd

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 1500)  # max table width to display
    # 导入用于处理时区的pytz模块
    import pytz

    def minum_15m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime2 = (string_datetime + datetime.timedelta(minutes=-15)).strftime("%Y-%m-%d %H:%M")
        return startTime2

    # 建立与MetaTrader 5程序端的连接
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2022, 3, 8, tzinfo=timezone)
    # request 100 000 EURUSD ticks starting from 10.01.2019 in UTC time zone
    ticks = mt5.copy_ticks_from("NI225", utc_from, 100000, mt5.COPY_TICKS_ALL)
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

    def minum_15m(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        startTime2 = (string_datetime + datetime.timedelta(minutes=-15)).strftime("%Y-%m-%d %H:%M:%S")
        return startTime2

    _15_time = minum_15m(last_time)
    the_first_row = the_last_dt_3000.loc[the_last_dt_3000['time'] == "{0}".format(_15_time)]

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

    def get_average_dt(bid_price, ask_price):
        average_price = (bid_price + ask_price) / 2
        return average_price

    last_average = get_average_dt(get_float_from_dataframe(the_last_row, "bid", the_last_row),
                                  get_float_from_dataframe(the_last_row, "ask", the_last_row))
    first_average = get_average_dt(get_float_from_dataframe(the_first_row, "bid", the_last_row),
                                   get_float_from_dataframe(the_first_row, "ask", the_last_row))

    confirm_dt = last_average - first_average

    return confirm_dt


if __name__:="__main__":
    import itchat
    # 登录并获得QR码
    itchat.login()
    # 通过手机扫描QR码登录的微信号给“文件传输助手”发送消息“您好”

    while True:
        confirm_dt = big_dt_function()
        time.sleep(15)
        print("-"*50,confirm_dt,"-"*50)
        if abs(confirm_dt) >= 80 and confirm_dt>0 and os.path.exists("call.txt") is False:
            if os.path.exists("put.txt"):
                os.remove('put.txt')
            itchat.send("time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S")),'filehelper')
            file_handle = open('call.txt', mode='w')
        if  abs(confirm_dt) >= 80 and confirm_dt<0 and os.path.exists("put.txt") is False:
            if os.path.exists("call.txt"):
                os.remove('call.txt')
            itchat.send("time: {1} \n 市场为 {0} ，考虑是否进场！".format(str(confirm_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S")),'filehelper')
            file_handle = open('put.txt', mode='w')






