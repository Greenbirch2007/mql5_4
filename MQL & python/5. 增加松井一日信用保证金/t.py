
import re

url = "https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=239311149&int_fd=fund:psearch:search_result"


import requests
res = requests.get(url)
res.encoding = res.apparent_encoding

# # 增加总资产,投资方法,费率的解析

print(res.text)

#
# pattern = re.compile('<p class="tooltip_before floatL md-l-utl-mt4">.*?設定日.*?<td>(.*?)</td>',re.S)
# items = re.findall(pattern,res.text)
#
#
# date_of_established =  items[0].split()
# pattern = re.compile('<th class="alC">設定来</th>.*?<td .*?>(.*?)</td>',re.S)
# items = re.findall(pattern,res.text)
#
# yield_since_established = items[0].split()
#
# print(date_of_established)
# print(yield_since_established)

