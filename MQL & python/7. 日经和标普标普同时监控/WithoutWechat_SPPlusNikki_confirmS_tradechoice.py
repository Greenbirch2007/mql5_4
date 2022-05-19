


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
import os,csv
import itchat
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
import pandas as pd
import pytz
import requests
from lxml import etree


def confirm_reponsetext(response, encodings):
    if encodings != []:
        response_text = response.content.decode("{0}".format(encodings[0]))
    else:
        response_text = response.text
    return response_text



def get_sj_dailymargin_info():
    url = "https://www.matsui.co.jp/service/fop/d-futures/margin/"
    res = requests.get(url)
    encodings = requests.utils.get_encodings_from_content(res.text)
    response_text = confirm_reponsetext(res, encodings)
    selector = etree.HTML(response_text)
    margin_ = selector.xpath('/html/body/div[1]/main/div[2]/article/div/div[2]/div/table/tbody/tr[3]/td[3]/text()')
    return margin_[0]

def today_date():

    today_d = datetime.now().strftime("%Y-%m-%d")

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
def big_dt_function(tradeone,basetime):


    # 导入'pandas'模块，用于以表格形式显示获得的数据

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 6000)  # max table width to display
    # 导入用于处理时区的pytz模块

    def minum_basetime(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime = (string_datetime + datetime.timedelta(minutes=-basetime)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime

    def minum_basetime_minus1(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus1 = (string_datetime + datetime.timedelta(minutes=-basetime+1)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus1
    def minum_basetime_minus2(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus2 = (string_datetime + datetime.timedelta(minutes=-basetime+2)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus2
    def minum_basetime_minus3(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus3 = (string_datetime + datetime.timedelta(minutes=-basetime+3)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus3





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

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

    # create DataFrame out of the obtained data
    ticks_frame = pd.DataFrame(ticks)
    # 将时间（以秒为单位）转换为日期时间格式
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    # 整体处理 #直接 1000就好
    # 求一个平均差即可！如果！
    the_last_dt_188888 = ticks_frame.tail(188888)
    the_last_row = the_last_dt_188888.tail(1)
    last_time = str(list(the_last_row["time"])[0])


    _base_time = minum_basetime(last_time)
    _base_time_minus1 = minum_basetime_minus1(last_time)
    _base_time_minus2 = minum_basetime_minus2(last_time)
    _base_time_minus3 = minum_basetime_minus3(last_time)
    the_first_row_basetime = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time)]
    the_first_row_basetime_minus1 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus1)]
    the_first_row_basetime_minus2 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus2)]
    the_first_row_basetime_minus3 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus3)]

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
    first_average_basetime = get_average_dt(get_float_from_dataframe(the_first_row_basetime, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime, "ask", the_last_row))
    first_average_basetime_minus1 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus1, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus1, "ask", the_last_row))
    first_average_basetime_minus2 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus2, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus2, "ask", the_last_row))
    first_average_basetime_minus3 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus3, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus3, "ask", the_last_row))


    confirm_dt_basetime = last_average - first_average_basetime
    confirm_dt_basetime_minus1 = last_average - first_average_basetime_minus1
    confirm_dt_basetime_minus2  = last_average - first_average_basetime_minus2
    confirm_dt_basetime_minus3 = last_average - first_average_basetime_minus3

    confirm_dt= choose_not_zero([confirm_dt_basetime,confirm_dt_basetime_minus1,confirm_dt_basetime_minus2,confirm_dt_basetime_minus3])


    return last_average,confirm_dt



def send_msg_to_sb(username,msg):
    users=itchat.search_friends(username)
    itchat.send(msg,toUserName=users[0]['UserName'])


def print_and_sendmsg(username, msg):
    send_msg_to_sb(username, msg)
    log.debug(msg)
def mkdir(path):
    lpath=os.getcwd()
    isExists = os.path.exists(os.path.join(lpath,path))
    if not isExists:
        os.makedirs(path)
def remove_existfile(filename):
    if os.path.exists(filename):
        os.remove(filename)
def remove_file(filetype):
    for file in os.listdir("."):
        file_list = file.split(".")
        if len(file_list) != 1:
            if file.split(".")[1] == filetype:
                os.remove(file)


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

def affirm_Signal(tradeone):

    # 导入'pandas'模块，用于以表格形式显示获得的数据

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 6000)  # max table width to display
    # 导入用于处理时区的pytz模块

    def minum_basetime(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime = (string_datetime + datetime.timedelta(minutes=-0.1)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime

    def minum_basetime_minus1(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus1 = (string_datetime + datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus1
    def minum_basetime_minus2(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus2 = (string_datetime + datetime.timedelta(minutes=-2)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus2
    def minum_basetime_minus3(string_datetime):
        import datetime
        string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
        minum_basetime_minus3 = (string_datetime + datetime.timedelta(minutes=-3)).strftime("%Y-%m-%d %H:%M:%S")
        return minum_basetime_minus3





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


    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

    # create DataFrame out of the obtained data
    ticks_frame = pd.DataFrame(ticks)
    # 将时间（以秒为单位）转换为日期时间格式
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    # 整体处理 #直接 1000就好
    # 求一个平均差即可！如果！
    the_last_dt_188888 = ticks_frame.tail(188888)
    the_last_row = the_last_dt_188888.tail(1)
    last_time = str(list(the_last_row["time"])[0])


    _base_time = minum_basetime(last_time)
    _base_time_minus1 = minum_basetime_minus1(last_time)
    _base_time_minus2 = minum_basetime_minus2(last_time)
    _base_time_minus3 = minum_basetime_minus3(last_time)
    the_first_row_basetime = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time)]
    the_first_row_basetime_minus1 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus1)]
    the_first_row_basetime_minus2 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus2)]
    the_first_row_basetime_minus3 = the_last_dt_188888.loc[the_last_dt_188888['time'] == "{0}".format(_base_time_minus3)]

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
    first_average_basetime = get_average_dt(get_float_from_dataframe(the_first_row_basetime, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime, "ask", the_last_row))
    first_average_basetime_minus1 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus1, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus1, "ask", the_last_row))
    first_average_basetime_minus2 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus2, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus2, "ask", the_last_row))
    first_average_basetime_minus3 = get_average_dt(get_float_from_dataframe(the_first_row_basetime_minus3, "bid", the_last_row),get_float_from_dataframe(the_first_row_basetime_minus3, "ask", the_last_row))


    confirm_dt_basetime = last_average - first_average_basetime
    confirm_dt_basetime_minus1 = last_average - first_average_basetime_minus1
    confirm_dt_basetime_minus2  = last_average - first_average_basetime_minus2
    confirm_dt_basetime_minus3 = last_average - first_average_basetime_minus3
    confirm_dt= choose_not_zero([confirm_dt_basetime,confirm_dt_basetime_minus1,confirm_dt_basetime_minus2,confirm_dt_basetime_minus3])
    return confirm_dt
def writeintotxt_file(filename,data):
    with open(filename,'a', newline='\n', encoding="utf-8") as f_output:
        tsv_output = csv.writer(f_output, delimiter=',')
        tsv_output.writerow(data)

def readDatafile(filename):
    line_list = []
    call_list = []
    put_list = []
    with open(filename,"r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list.append(line)
    for item in line_list:
        if "put" in item:
            put_list.append(float(item.split(",")[1]))
        elif "call" in item:
            call_list.append(float(item.split(",")[1]))
    total_list = sum(call_list)+sum(put_list)

    return sum(call_list),sum(put_list),total_list




def find_and_confirm_signal(tradeone,base_dt_minus3,base_dt_minus30,trade_dict,find_param,confirm_param):


    # 识别信号
    if os.path.exists('call{0}.txt'.format(tradeone)) is False and os.path.exists('put{0}.txt'.format(tradeone)) is False:
        # 无文件,进行信号甄别;有文件,就验证信号
        find_signal_dt = base_dt_minus30
        find_signal_msg = "tradeone is {2} \n time: {1} \n 市场为 {0} ，发现信号！".format(str(find_signal_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),tradeone)
        if find_signal_dt> 0 and find_signal_dt>trade_dict[tradeone]*find_param:
            print(find_signal_msg)

            open('call{0}.txt'.format(tradeone), mode='w')
        elif find_signal_dt <0 and  find_signal_dt<-trade_dict[tradeone]*find_param:
            print(find_signal_msg)

            open('put{0}.txt'.format(tradeone), mode='w')
        else:
            pass

    else: #验证信号
        if os.path.exists('call{0}.txt'.format(tradeone)) is True:
            confirm_signal_dt = base_dt_minus3
            if confirm_signal_dt>0 :
                # 写入文件
                writeintotxt_file("call{0}.txt".format(tradeone), ["call",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("call{0}.txt".format(tradeone))
                print("----------------信号是--call------{0}-----------------------------------".format(tradeone))

                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(call_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(put_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)

                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "{0}--------------做多的信号彻底失败！赶紧离场！".format(tradeone)
                    print(msg5)

                    remove_existfile("call{0}.txt".format(tradeone))
            elif confirm_signal_dt<0:
                # 写入文件
                writeintotxt_file("call{0}.txt".format(tradeone), ["put",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("call{0}.txt".format(tradeone))
                # 1. 本次判定的信号的结果 ，和
                # 2. 累积判定正确的信号的结果 ，和
                # 3. 累积判定错误的信号的结果 ，和
                # 4. 累积判定的信号的结果 ，和
                # 5. 合计的 加上40点 还是为负说明信号彻底失效！ 删除txt文件
                print("---------------信号是--call-------{0}-----------------------------------".format(tradeone))
                msg1 = "本次判定信号是错误的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(call_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(put_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)

                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "{0}--------------做多的信号彻底失败！赶紧离场！".format(tradeone)
                    print(msg5)

                    remove_existfile("call{0}.txt".format(tradeone))



        # 读取文件信息,结合当次数据发送信号确认的情况。
        elif os.path.exists('put{0}.txt'.format(tradeone)) is True:
            confirm_signal_dt = base_dt_minus3
            if confirm_signal_dt<0:
                # 写入文件
                writeintotxt_file("put{0}.txt".format(tradeone), ["call",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("put{0}.txt".format(tradeone))
                print("---------------信号是--put-------{0}-----------------------------------".format(tradeone))

                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(put_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(call_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)

                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "{0}-------做空的信号彻底失败！赶紧离场！".format(tradeone)
                    print(msg5)

                    remove_existfile("put{0}.txt".format(tradeone))
            elif confirm_signal_dt>0:
                # 写入文件
                writeintotxt_file("put{0}.txt".format(tradeone), ["put",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("put{0}.txt".format(tradeone))
                print("---------------信号是--put-------{0}-----------------------------------".format(tradeone))
                msg1 = "本次判定信号是错误的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(put_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(call_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)

                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "{0}-------做空的信号彻底失败！赶紧离场！".format(tradeone)
                    print(msg5)

                    remove_existfile("put{0}.txt".format(tradeone))



def final_(tradeone):
    last_average, confirm_dt_60 = big_dt_function(tradeone, 60)
    confirm_dt_5 = affirm_Signal(tradeone)
    print(tradeone, float(confirm_dt_5), float(confirm_dt_60))
    find_and_confirm_signal(tradeone, float(confirm_dt_5), float(confirm_dt_60), FX_trade_dict, 0.17, 0.1)

if __name__=="__main__":
    # 开始时, 删除所有文本
    remove_file("txt")
    time.sleep(2)
    FX_trade_dict = {'SP500m': 41,"NI225":363}
    mkdir("log")
    true_list = []
    false_list = []

    logpath= os.path.join(os.getcwd(),"log")
    log= Logger()


    # 通过手机扫描QR码登录的微信号给“文件传输助手”发送消息“您好”
    while True:
        final_("SP500m")
        final_("NI225")

        time.sleep(180)
        print("-"*99)












