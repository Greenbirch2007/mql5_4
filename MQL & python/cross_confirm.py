#! -*- utf-8 -*-

import datetime
from itertools import chain
import pymysql
from queue import Queue
import threading
import time

from lxml import etree

# selenium 3.12.0
from selenium.webdriver import PhantomJS








def test_M_temp():
    url = "http://quote.eastmoney.com/gb/zsN225.html"
    ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe")  # windows
    ch_options.get(url)
    html = ch_options.page_source
    ch_options.close()
    selector = etree.HTML(html)
    last_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[1]/div[1]/span[1]/span/text()')
    yest_close_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[2]/span[2]/span/text()')
    max_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[3]/span[2]/span/text()')
    min_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[4]/span[2]/span/text()')

    max_min = float(max_price[0]) -float(min_price[0])
    max_yest_close_price = float(max_price[0]) -float(yest_close_price[0])
    min_yest_close_price = float(min_price[0]) -float(yest_close_price[0])
    last_yest_close_price = float(last_price[0]) -float(yest_close_price[0])
    print("max_min---->",max_min)
    print("max_yest_close_price---->",max_yest_close_price)
    print("min_yest_close_price---->",min_yest_close_price)
    print("last_yest_close_price---->",last_yest_close_price)
    if abs(last_yest_close_price) >=50:
        print("---->  注意！目前走势是十字星！考虑是否进场 <-----")








if __name__=="__main__":
    test_M_temp()





