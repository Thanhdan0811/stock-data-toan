import pandas as pd
import datetime
import pytz
import math

def get_timestamp(date_string):
    start_bracket = date_string.find("(")
    end_bracket = date_string.find(")")
    # print("date string stamp ", date_string[start_bracket + 1, end_bracket])
    return float(date_string[start_bracket + 1: end_bracket])

def process_excel(data):
    DF_stock = {
                "Ngày lấy dữ liệu": [], 
                "Ngày dữ liệu":[], 
                "VS-Sector": [], 
                "Thay đổi": [], 
                "% thay đổi": [], 
                "Khối lượng": [], 
                "Giá trị": [], 
                "KL NĐTNN Mua": [], 
                "KL NĐTNN Bán": []
            }
    for st in data:
        # "/Date(1704992400000)/"
        time_process = datetime.datetime.fromtimestamp(get_timestamp(st["TradingDate"]) / 1000, pytz.timezone("Asia/Ho_Chi_Minh"))
        time_process = time_process.strftime("%d-%m-%Y")
        DF_stock["Ngày lấy dữ liệu"].append(datetime.datetime.now().strftime("%d-%m-%Y"))
        DF_stock["Ngày dữ liệu"].append(time_process)
        DF_stock["VS-Sector"].append(st["Text"])
        DF_stock["Thay đổi"].append("{:,.2f}".format(st["CloseIndex"]))
        DF_stock["% thay đổi"].append("{:,.2f}%".format(st["ChangeClose"]))
        DF_stock["Khối lượng"].append("{:,}".format(st["Vol"]))
        DF_stock["Giá trị"].append("{:,}".format(st["Val"]))
        DF_stock["KL NĐTNN Mua"].append("{:,}".format(st["ForeignBuyVol"]))
        DF_stock["KL NĐTNN Bán"].append("{:,}".format(st["ForeignSellVol"]))
        # print(type(DF_stock["Khối lượng"][0]))
    
    df = pd.DataFrame(data=DF_stock)

    # print("df", df)

    return df