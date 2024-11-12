from generallib import *



# 设置合约代码
contract_code = 'IC2303'
# 设置日期范围 (2022年10月1日 - 2022年10月31日)
start_date = datetime(2022, 11, 1)
end_date = datetime(2022, 11, 30)

# 目标文件夹路径
folder_path = rf'C:\Users\progene12\share\FUTURES_DATA\IC_202211'







print(f'folder_path: {folder_path}')

# 创建目标文件夹
if not os.path.exists(folder_path):
    os.makedirs(folder_path)



# 定义表头
columns = [
    '交易日', '合约代码', '交易所代码', '合约在交易所的代码', '最新价', '上次结算价', '昨收盘',
    '昨持仓量', '今开盘', '最高价', '最低价', '数量', '成交金额', '持仓量', '今收盘',
    '本次结算价', '涨停板价', '跌停板价', '昨虚实度', '今虚实度', '最后修改时间', '最后修改毫秒',
    '申买价一', '申买量一', '申卖价一', '申卖量一', '申买价二', '申买量二', '申卖价二',
    '申卖量二', '申买价三', '申买量三', '申卖价三', '申卖量三', '申买价四', '申买量四',
    '申卖价四', '申卖量四', '申买价五', '申买量五', '申卖价五', '申卖量五', '当日均价', '业务日期'
]

# 生成每一天的CSV文件
current_date = start_date
while current_date <= end_date:
    # 生成文件名
    date_str = current_date.strftime('%Y%m%d')
    date_str_2 = current_date.strftime('%Y-%m-%d')
    file_name = f'{contract_code}_{date_str}.csv'
    file_path = os.path.join(folder_path, file_name)

    # 读取数据
    wd_df = pd.read_csv(rf'C:\Users\progene12\share\FUTURES_DATA\{contract_code}.csv', encoding='gb2312')
    OPEN = wd_df.loc[wd_df['TIME'] == date_str_2, 'OPEN'].values
    HIGH = wd_df.loc[wd_df['TIME'] == date_str_2, 'HIGH'].values
    LOW = wd_df.loc[wd_df['TIME'] == date_str_2, 'LOW'].values
    CLOSE = wd_df.loc[wd_df['TIME'] == date_str_2, 'CLOSE'].values
    PRE_CLOSE = wd_df.loc[wd_df['TIME'] == date_str_2, 'PRE_CLOSE'].values
    SETTLE = wd_df.loc[wd_df['TIME'] == date_str_2, 'SETTLE'].values
    # print(f'OPEN: {OPEN}, HIGH: {HIGH}, LOW: {LOW}, CLOSE: {CLOSE}, PRE_CLOSE: {PRE_CLOSE}, SETTLE: {SETTLE}')

    # 去除括号并确保浮点数格式
    OPEN = float(OPEN[0]) if OPEN.size > 0 else None
    HIGH = float(HIGH[0]) if HIGH.size > 0 else None
    LOW = float(LOW[0]) if LOW.size > 0 else None
    CLOSE = float(CLOSE[0]) if CLOSE.size > 0 else None
    PRE_CLOSE = float(PRE_CLOSE[0]) if PRE_CLOSE.size > 0 else None
    SETTLE = float(SETTLE[0]) if SETTLE.size > 0 else None

    # 创建空的DataFrame
    df = pd.DataFrame(columns=columns)

    # 添加一行数据
    df.loc[0] = [date_str, contract_code, None, None, None, None, PRE_CLOSE,
                 None, OPEN, HIGH, LOW, None, None, None, CLOSE,
                 None, None, None, None, None, '15:00:00', None,
                 None, 1, None, 1, None, None, None, None,
                 None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None]

    # 保存为CSV文件，确保数值为浮点型格式
    df.to_csv(file_path, index=False, encoding='gb2312', float_format='%.1f')

    print(f'已创建文件: {file_name}')

    # 日期增加一天
    current_date += timedelta(days=1)

print('所有文件已创建完成')
