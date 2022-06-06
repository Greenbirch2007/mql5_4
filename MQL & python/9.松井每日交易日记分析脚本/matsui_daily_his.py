

# 1.总开始时间，结束时间，总交易次数，盈利次数，止损次数 ，盈利总金额，止损总金额
# 2. 每笔交易 开始时间，结束时间，盈亏状况，盈亏金额，买卖方向
# 3
#
#
#
#
import pandas as pd
import datetime
import json

data = pd.read_csv("futoporder_20220606.csv")

start_list = []
end_list = []
for item in data.values.tolist():
    if "-" not in item[16]:
        if "新規" in item[2]:
            start_list.append([item[2],item[4],item[16],item[17]])
        elif "返済" in item[2]:
            end_list.append([item[2],item[4],item[16],item[17]])


# 获取列表的第二个元素
def takeSecond(elem):
    return elem[3]


# 按照时间排序
start_list.sort(key=takeSecond)
end_list.sort(key=takeSecond)
start_time = start_list[0][-1]
end_time = start_list[-1][-1]
print(start_time)
print(end_time)
total_trade_times = len(start_time)


true_trade_money = []
false_trade_money = []
everytime_trade_info  = []

f_list ={}



def compare_two_list(start_list,end_list):
    if  start_list[1] == '買'and int(start_list[2]) > int(end_list[2]):
        trade_result = "止损"
        trade_staus = start_list[1]
        result_money = int(end_list[2]) - int(start_list[2])
        false_trade_money.append(result_money)
    elif '買' in start_list[1] and int(start_list[2]) < int(end_list[2]):
        trade_result = "止盈"
        trade_staus = start_list[1]
        result_money = int(end_list[2]) - int(start_list[2])
        true_trade_money.append(result_money)

    elif '売' in start_list[1] and int(start_list[2]) > int(end_list[2]):
        trade_result = "止盈"
        trade_staus = start_list[1]
        result_money = int(start_list[2]) - int(end_list[2])
        true_trade_money.append(result_money)

    elif '売' in start_list[1] and int(start_list[2]) < int(end_list[2]):
        trade_result = "止损"
        trade_staus = start_list[1]
        result_money = int(start_list[2]) - int(end_list[2])
        false_trade_money.append(result_money)
    one_trade = {}
    one_trade["开始时间"] = start_list[-1]
    one_trade["平仓时间"] =end_list[-1]
    one_trade["开仓价格"] =start_list[2]
    one_trade["平仓价格"] =end_list[2]
    one_trade["单次交易结果"] =trade_result
    one_trade["单次交易方向"] =trade_staus
    one_trade["单次交易结果金额"] =result_money
    everytime_trade_info.append(one_trade)




for i1,i2 in zip(start_list,end_list):
    print(i1,i2)
    compare_two_list(i1,i2)


def writeinto_jsonfile(filename,list_data):
    with open(filename, 'w', encoding='utf-8') as fw:
        json.dump(list_data, fw, indent=4, ensure_ascii=False)


f_list["总开始时间"]=start_time
f_list["总结束时间"]=end_time
f_list["总交易所次数"]= len(true_trade_money)+len(false_trade_money)
f_list["总盈利次数"]= len(true_trade_money)
f_list["总亏损次数"]= len(false_trade_money)
f_list["总盈利金额"]=sum(true_trade_money)
f_list["总亏损金额"]=sum(false_trade_money)
f_list["交易明细"]= everytime_trade_info
filename = datetime.datetime.now().strftime('%Y-%m-%d')
total_trade_money = sum(true_trade_money)+sum(false_trade_money)
writeinto_jsonfile("{1}-t-{0}.json".format(filename,str(total_trade_money)), f_list)