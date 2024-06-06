import pandas as pd
import tushare as ts
import time

start_time = time.time()

# import yfinance as yf
# import pandas_datareader.data as pddr
#
# stock_list = ['APPL']
# start_date = '2024-6-5'
# end_date = '2024-6-5'
#
# stockData = pddr.DataReader(stock_list[0], 'yahoo', end_date)
#
# closing_prices = stock_list[0]['close']
#
# print(closing_prices)

# stock_list_all = ts.get_stock_basics()
# print(stock_list_all)

#
# df = ts.pro_bar(ts_code='000001.SH', adj='qfq', start_date='20181001', end_date='20181011')
# print(df)

# print(df)
try:
    today = "20240605"
    df = pd.read_csv(r'D:\lzy\myCode\tradeTools_github\stockData\stock_code_list3.csv', header=None)
    all_code_list = df[0].tolist()
    df_total = None
    for index, stock in enumerate(all_code_list, start=1):
        df_single = ts.pro_bar(ts_code=stock, adj='qfq', start_date=today, end_date=today)
        df_total = pd.concat([df_total, df_single], ignore_index=True)  # 合并到这里
        print(f"FETCHING DATA --- \033[33m {index:4} / {len(all_code_list)} \033[0m")
except Exception as e:
    print(f"error:{e}")

print(df_total)
# 记录结束时间
end_time = time.time()

# 计算用时
elapsed_time = end_time - start_time

# 打印股票代码列表和用时
print(f"程序用时: {elapsed_time:.6f} 秒")