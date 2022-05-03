import itertools
import sys
import html
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
import csv
import os
import time
import copy
import re
import datetime
from itertools import chain
import pymysql
from queue import Queue
import threading

from lxml import etree

# selenium 3.12.0
from selenium.webdriver import PhantomJS


def remove_dot_fromlist(list_content):
    big_list =[]
    for item in list_content:
        item_int= int("".join(item.split(",")))
        big_list.append(item_int)
    return big_list

def run_forever(func):
    def wrapper(obj):
        while True:
            func(obj)
    return wrapper


class ZG_Futures(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        self.url_pattern = '{0}'
        # url 队列
        self.url_queue = Queue()


    def add_url_to_queue(self):
        for i in url_list:
            print(i)

            self.url_queue.put(self.url_pattern.format(i))


    @run_forever
    def add_page_to_queue(self):
        ''' 发送请求获取数据 '''
        url = self.url_queue.get()

        html= use_selenium_headless_getdt(url)

        patter_= re.compile('<div class="chart_table01_col_02"><div class="chart_table01_price01"><p>(.*?)</p></div>',re.S)
        items= re.findall(patter_,html)
        if items !=[]:
            result = remove_dot_fromlist(items)
# Nikki225,DowJ

        dt_dict = {}
        dt_dict["Nikki225"] = result[0]
        dt_dict["DowJ"] = result[1]
        final_dt.append(dt_dict)
        print(items)




        # 完成当前URL任务
        self.url_queue.task_done()

# <div class="chart_box" data-id="N225RM02/TFX"><div class="chart_table01 clearfix"><div class="chart_table01_col_01"><div class="chart_table01_name"><p>(.*?)</p></div>'+'<div class="chart_table01_col_02"><div class="chart_table01_price01"><p>(.*?)</p></div>'

    #

    # <img src="img/chart_flag_N225_TFX.png" alt=""></div></div><div class="chart_table01_col_02"><div class="chart_table01_price01"><p>(.*?)</p></div><div class="chart_table01_price02"><p>.*?<span>.*?</span></p></div><!-- / .chart_table01_col_02 --></div><div class="chart_table01_col_03"><div class="chart_table01_ask"><p><span class="chart_table01_ask_txt01">ASK</span><span class="chart_table01_ask_txt02">.*?</span><span class="chart_table01_ask_txt03">（40）</span></p></div><div class="chart_table01_bid"><p><span class="chart_table01_bid_txt01">BID</span><span class="chart_table01_bid_txt02">26,798</span><span class="chart_table01_bid_txt03">（100）</span></p></div></div><!-- / .chart_table01 clearfix --></div><!-- / .chart_box --></div>


    def run_use_more_task(self,func,count=1):
        for i in range(0,count):
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()
    def run(self):
        url_t = threading.Thread(target=self.add_url_to_queue)
        url_t.setDaemon(True)
        url_t.start()

        self.run_use_more_task(self.add_page_to_queue,4)
         # 使用队列join方法,等待队列任务都完成了才结束
        self.url_queue.join()









def use_selenium_headless_getdt(url):
    #ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe") # windows
    ch_options = PhantomJS() #linux
    ch_options.get(url)
    html = ch_options.page_source
    ch_options.close()
    return html



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Futures',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        f_ls = "%s," * (2)
        print(len(f_ls[:-1].split(",")))
        cursor.executemany('insert into click_CFD (Nikki225,DowJ) values ({0})'.format(f_ls[:-1]),content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass
#合并list的字典
def list_dict(list_data):
    dict_data = {}
    for i in list_data:
        key, = i
        value, = i.values()
        dict_data[key] = value
    return dict_data


def collection_func():
    sst = ZG_Futures()
    sst.run()
    e = datetime.datetime.now()
    f = e - s
    print(final_dt)
    # [{'rbm': '4960'}, {'TAM': '6182'}, {'im': '875.5'}, {'ppm': '8697'}, {'jmm': '3003.0'}, {'pm': '11470'}, {'mm': '4062'}, {'jm': '3799.5'}]

    # 异步之后还要排序
    f_tuple = (final_dt[0]["Nikki225"],final_dt[0]["DowJ"])
    print(f_tuple)
    # 每10秒插入一次
    insertDB([f_tuple])
    print(final_dt)
    print(f)
    sys.exit(0)
#
#
if __name__=="__main__":
    # in Japan
    s = datetime.datetime.now()

    final_dt = []
    # 制只锁定在 10个左右 # 内存太小了，所以这次先缩减在6-7
    forSort_futurescode = ["Nikki225", "DowJ"]
    url_list = ["https://www.clickkabu365.jp/"]
    collection_func()








# create table click_CFD (id int not null primary key auto_increment,Nikki225 TEXT,DowJ TEXT,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;



# drop table click_CFD;