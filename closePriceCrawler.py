import pandas as pd
import tushare as ts
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


df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')

print(df)

