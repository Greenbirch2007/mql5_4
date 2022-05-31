


# MT5 默认是东二区时间，  所以MT5的时间加上7 就是 可以处理的时间了



import pandas as pd
import datetime
import csv
# 以需要先⽤pandas的to_datetime()⽅法，转化成时间格式进⾏加减，然后再转换成df格式




def plus_basetime_plus_N_hours(string_datetime, N_hours):
    string_datetime = datetime.datetime.strptime(string_datetime, "%H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
    plus_basetime_plusN = (string_datetime + datetime.timedelta(hours=+N_hours)).strftime("%H:%M:%S")
    return plus_basetime_plusN
def list_time_plus7(list_content):
    f_list =[]
    for item in list_content:
        plus_7_result = plus_basetime_plus_N_hours(item,7)
        f_list.append(plus_7_result)
    return f_list

def difference_set_fromTwo_df(basetime, start_time_string, end_time_string):
    #  df1_time > df2_time
    basetime = datetime.datetime.strptime(basetime, "%H:%M:%S")
    start_time_string = datetime.datetime.strptime(start_time_string, "%H:%M:%S")
    end_time_string = datetime.datetime.strptime(end_time_string, "%H:%M:%S")
    if basetime>=start_time_string and basetime<= end_time_string:
        return True

def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)







def read_csv_file_writeinto_csv(csvfilename_4r,csvfilename_4w,starttimne,endtime):
    COLUMN_NAME = ["DATE", "TIME", "OPEN", "HIGH", "LOW", "CLOSE", "TICKVOL", "VOL", "SPREAD", "plus_7_tokyoTime"]
    writeinto_detail(csvfilename_4w, COLUMN_NAME)
    df = pd.read_csv(csvfilename_4r)
    df_plus_7_newcloumn = pd.DataFrame(list_time_plus7(list(df["<TIME>"])), columns=['plus_7_tokyoTime'])
    df["plus_7_tokyoTime"] =df_plus_7_newcloumn
    for item in df.values.tolist():
        if difference_set_fromTwo_df(item[-1], starttimne, endtime):
            writeinto_detail(csvfilename_4w, item)
            print(item)

    

if __name__ =="__main__":
    start_time_string1 ="19:30:00"
    end_time_string1 = "20:30:00"
    start_time_string2 ="20:30:00"
    end_time_string2 = "21:30:00"
    start_time_string3 ="21:30:00"
    end_time_string3 = "22:30:00"
    start_time_string4 ="22:30:00"
    end_time_string4 = "23:30:00"
    start_time_string5 ="1:00:00"
    end_time_string5 = "2:00:00"
    start_time_string6 ="2:00:00"
    end_time_string6 = "3:00:00"
    start_time_string7 ="3:00:00"
    end_time_string7 = "4:00:00"
    start_time_string8 ="4:00:00"
    end_time_string8 = "5:00:00"
    csvfilename_4r = "NI225_M30_202009231430_202205272230.csv"
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string1.replace(":","-")+"-"+end_time_string1.replace(":","-")+".csv", start_time_string1, end_time_string1)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string2.replace(":","-")+"-"+end_time_string2.replace(":","-")+".csv", start_time_string2, end_time_string2)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string3.replace(":","-")+"-"+end_time_string3.replace(":","-")+".csv", start_time_string3, end_time_string3)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string4.replace(":","-")+"-"+end_time_string4.replace(":","-")+".csv", start_time_string4, end_time_string4)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string5.replace(":","-")+"-"+end_time_string5.replace(":","-")+".csv", start_time_string5, end_time_string5)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string6.replace(":","-")+"-"+end_time_string6.replace(":","-")+".csv", start_time_string6, end_time_string6)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string7.replace(":","-")+"-"+end_time_string7.replace(":","-")+".csv", start_time_string7, end_time_string7)
    read_csv_file_writeinto_csv(csvfilename_4r, start_time_string8.replace(":","-")+"-"+end_time_string8.replace(":","-")+".csv", start_time_string8, end_time_string8)



















