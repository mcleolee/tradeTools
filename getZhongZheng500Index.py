from generallib import *

df = pro.index_daily(ts_code='000905.SH', start_date='20200101', end_date='20241031')
df.to_csv(rf'D:\lzy\myCode\tradeTools_github\zz500index.csv', index=False)
print(df)