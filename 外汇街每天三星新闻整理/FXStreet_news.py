#! -*- utf-8 -*-


import time
from lxml import etree
from selenium.webdriver import PhantomJS



def use_selenium_headless_getdt(url):
    ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe") # windows
    # ch_options = PhantomJS() #linux
    ch_options.get(url)
    time.sleep(3)
    html = ch_options.page_source
    ch_options.close()
    return html











if __name__=="__main__":
    url ="https://www.fxstreet.cn/calendar/"
    html = use_selenium_headless_getdt(url)
    selector = etree.HTML(html)
    rank = selector.xpath('//*[@id="fxst-calendartable"]/tbody/tr/td[6]/span/text()')
    time_ = selector.xpath('//*[@id="fxst-calendartable"]/tbody/tr/td[1]/text()')
    country = selector.xpath('//*[@id="fxst-calendartable"]/tbody/tr/td[4]/text()')
    event = selector.xpath('//*[@id="fxst-calendartable"]/tbody/tr/td[5]/a/text()')
    f_time = [x for x in time_ if "星期" not in time_]
    for i1, i2, i3, i4 in zip(rank, f_time, country, event):
        if i1 == "3":
            print(i1, i2, i3, i4)








# create table ZN_Futures (id int not null primary key auto_increment,ym TEXT,vm TEXT,TAM TEXT,rbm TEXT,pm TEXT,OIM TEXT,mm TEXT,MAM TEXT,lm TEXT,im TEXT,FGM TEXT,bum TEXT,APM TEXT,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;

