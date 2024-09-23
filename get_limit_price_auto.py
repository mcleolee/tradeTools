import os
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta
import csv
import re
import time
import pandas as pd
from tqdm import tqdm
import baostock as bs
from WindPy import w


class StreamToLogger:
    def __init__(self, log_func):
        self.log_func = log_func

    def write(self, message):
        if message.strip():  # 忽略空行
            self.log_func(message)

    def flush(self):
        pass


@contextmanager
def redirect_stdout(log_func):
    logger = StreamToLogger(log_func)
    old_stdout = sys.stdout
    sys.stdout = logger
    try:
        yield
    finally:
        sys.stdout = old_stdout

# 获取文档文件夹路径
documents_path = os.path.join(os.environ['USERPROFILE'], 'Documents')

def downloadLimitpriceData_auto():


    # bs.login()
    # from WindPy import w



    def get_code_list_from_csv():
        # 获取当前项目所在目录
        current_dir = os.path.dirname(__file__)

        # CSV文件路径
        csv_file_path = os.path.join(current_dir, 'stock_code_list.csv')

        # 读取CSV文件并转换为列表
        code_list = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                code_list.append(row[0][:6])  # 假设CSV文件只有一列数据
        # print(code_list)
        return code_list

    def get_stock_code_wind():
        """
        获取wind股票代码
        """
        from WindPy import w
        w.start()
        # 当日日期
        m_today = datetime.now().strftime("%Y-%m-%d")

        # 调用wind接口获取全部A股代码
        result = w.wset("sectorconstituent", f"date={m_today};sectorid=a001010100000000")
        stock_code_list = []
        # 判断代码运行是否正常
        if result.ErrorCode == 0:
            # print(result)
            data = result.Data
            # print(data)
            # print(data[1])
            # 判断数据是否为空
            if len(data) > 0:
                for item in data[1]:
                    # print(item)
                    if item.find("SZ") != -1 or item.find("SH") != -1:
                        stock_code_list.append(item)
            else:
                # print("len(result.Data) == 0")
                return []

        else:
            print("get_stock_code_wind result.ErrorCode != 0, exist error")
            return []

        # 若未成功获取数据，则返回空列表
        if len(stock_code_list) > 0:
            return stock_code_list
        else:
            return []

    def get_std_day(day_str: str) -> str:
        """
        day_str: "yyyymmdd"或者"yyyy/mm/dd"或者"yyyy-mm-dd"或者其它形式
        处理过程：用正则筛选字符串中的全部数字，然后拼凑在一起，如果拼凑结果长度等8，则返回拼凑结果，否则返回""
        """
        num_regex = re.compile(r"\d+")
        find_list = num_regex.findall(day_str)
        # print(find_list)
        ret = "".join(find_list)
        # print(ret)
        return ret

    def Generate_Date(tradeDaysPath, today):
        '''
        tradeDaysPath: 记录当年交易日日期的xlsx
        today: 订单日期，格式"yyyymmdd"
        '''
        # 交易日当天
        try:
            today_slope = today[:4] + "/" + today[4:6] + "/" + today[6:8]
            today_line = today[:4] + "-" + today[4:6] + "-" + today[6:8]

            # 前一个交易日
            df_tradeDate = pd.read_excel(tradeDaysPath)
            df_tradeDate["date"] = df_tradeDate.日期.apply(
                lambda x: get_std_day(x) if type(x) == str else x.strftime("%Y%m%d"))

            yesterday = df_tradeDate.date[df_tradeDate[df_tradeDate.date == today].index[0] - 1]
            yes_slope = yesterday[:4] + "/" + yesterday[4:6] + "/" + yesterday[6:8]
            yes_line = yesterday[:4] + "-" + yesterday[4:6] + "-" + yesterday[6:8]

            print(f"Working on yesterday{yesterday} today{today}")

            return today, today_slope, today_line, yesterday, yes_slope, yes_line
        except Exception as e:
            print(rf"Generate_Date Error: {e}\nMove 2024交易日 file to C:\Users\<USER>\Documents")
            return None

    def round_fixed(num, d):
        """
        浮点数的四舍五入
        num: 浮点数
        d: d>0，在小数点后面第几位四舍五入；
           d<0，在整数部位四舍五入，d=-1表示将个位数四舍五入，以此类推
        """
        if num == 0:
            a = 0
        else:
            a = round(num + 0.5 / 10 ** 7, d)  # +0.5/10**7是为了避免丢失的精度造成误差
        return a

    def disappear(*arg):
        # 不对重定向的消息做任何事情
        ...

    def get_day_k_data_wind_inFunc(code, start_date, end_date, price_adjust_type="F"):
        """
        # 获取wind日k线数据
        :param code: 股票代码，比如601688.SH
        :param start_date: 开始日期，比如2015-09-10
        :param end_date: 结束日期，比如2022-12-31
        :param price_adjust_type: 复权类型，"F"前复权，"B"后复权，"NA"不复权
        :return:日数据的dataframe，列名有PRE_CLOSE,OPEN,HIGH,LOW,CLOSE,VOLUME,ADJFACTOR
        """

        if code.startswith("0") or code.startswith("3"):
            code = code + ".SZ"
        elif code.startswith("6"):
            code = code + ".SH"

        with redirect_stdout(disappear):
            w.start()


        result = w.wsd(f"{code}", "pre_close,open,high,low,close,volume,adjfactor",
                       start_date, end_date, f"PriceAdj={price_adjust_type}")

        datatime = [x.strftime('%Y-%m-%d') for x in result.Times]
        data_columns = [x.upper() for x in result.Fields]
        df = pd.DataFrame(result.Data, index=data_columns, columns=datatime)
        data = df.T
        # print(data)
        data["PRE_CLOSE"] = data["PRE_CLOSE"].apply(lambda x: round_fixed(x, 2))
        data["OPEN"] = data["OPEN"].apply(lambda x: round_fixed(x, 2))
        data["HIGH"] = data["HIGH"].apply(lambda x: round_fixed(x, 2))
        data["LOW"] = data["LOW"].apply(lambda x: round_fixed(x, 2))
        data["CLOSE"] = data["CLOSE"].apply(lambda x: round_fixed(x, 2))
        try:
            data["VOLUME"] = data["VOLUME"].apply(lambda x: int(x))
        except ValueError:  # VOLUME的值可能为空，int函数会报错
            pass

        # 等待3秒
        # time.sleep(3)
        return data

    def get_day_k_data_bs(code, start_day, end_day):
        """
        code:"601998.SH"
        start_day: "20220521"
        end_day: "20220628"
        """

        if code.startswith("0") or code.startswith("3"):
            code = "SZ." + code
        elif code.startswith("6"):
            code = "SH." + code

        stock_code = code
        start_date = start_day[:4] + "-" + start_day[4:6] + "-" + start_day[6:8]  # "2022-05-21"
        end_date = end_day[:4] + "-" + end_day[4:6] + "-" + end_day[6:8]  # "2022-05-21"

        data_fields = "date,preclose,open,high,low,close"
        rs = bs.query_history_k_data_plus(stock_code,
                                          data_fields,
                                          start_date=start_date,
                                          end_date=end_date,
                                          frequency='d',
                                          adjustflag="2")

        # 一次性获取全部数据
        # data = rs.get_data() # 获取全部数据 # 注意获取全部数据后，rs就为空了
        # print(data)

        # 一行一行获取数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            # print(type(rs.get_row_data())) # list
            line_list = rs.get_row_data()
            temp_list = []
            for item in line_list:
                if item.find("-") == -1:
                    temp_list.append(round(float(item), 2))
                else:
                    temp_list.append(item)
            data_list.append(temp_list)
        data = pd.DataFrame(data_list, columns=["DATE", "PRE_CLOSE", "OPEN", "HIGH", "LOW", "CLOSE"])
        print(data)
        return data

    # 计算股票的涨跌停价
    def get_rise_down_stop_price(code, last_close_price):
        """
        code:股票代码，形如"601998"或者"601998.SH"
        last_close_price: 昨日收盘价
        """
        if code[:3] == "688" or code[:2] == "30":
            rise_price = round(last_close_price * 1.2, 2)
            down_price = round(last_close_price * 0.8, 2)
        else:
            rise_price = round(last_close_price * 1.1, 2)
            down_price = round(last_close_price * 0.9, 2)
        return rise_price, down_price

    def get_all_stcok_from_wind():
        from WindPy import w
        import pandas as pd
        # 初始化Wind接口
        w.start()

        # 获取全市场A股股票代码
        data = w.wset("SectorConstituent", "sectorId=a001010100000000")

        # 创建DataFrame存储股票代码
        df = pd.DataFrame(data.Data[1])
        df = df[0].str.slice(0, 6)

        # 将DataFrame保存为CSV文件，不包含字段名
        # df.to_csv("stock_code_list.csv", index=False, header=False)

        print(f"已成功获取{len(df)}支股票")

        # 关闭Wind接口
        w.stop()
        return df.to_list()

    def get_next_trade_day(today):
        # 读取 今年的交易日
        df_tradeDate = pd.read_excel(tradeDaysPath)
        # 转换为列表
        tradeDate_list = df_tradeDate.日期.apply(lambda x: get_std_day(x) if type(x) == str else x.strftime("%Y%m%d")).tolist()
        # print(tradeDate_list)
        # 返回今天之后的那个日期
        return tradeDate_list[tradeDate_list.index(today) + 1]

    def printYellowMsg(text):
        print(f"\033[33m{text}\033[0m\n")
        return f"\033[33m{text}\033[0m"


    # 交易日期
    year = str(datetime.now().year)
    tradeDaysPath = rf"{documents_path}/{year}交易日.xlsx"

    today = datetime.now().strftime('%Y%m%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
    next_trade_day = get_next_trade_day(today)
    # 如果是周五，那么下一个交易日是下周一

    notToday = False

    print("This program will use the WIND database, please log in to the WIND account before running the program.")
    # print(fr"Move 2024交易日 file to C:\Users\<USER>\Documents")
    print(f"\n\t         Today -> {today}\n\t      Tomorrow -> {tomorrow}\n\tNext trade day -> {next_trade_day}\n")
    printYellowMsg(f"Auto download {next_trade_day} limit price data, please check if the date is correct")


    print("Starting program")
    # 停留0.5s
    time.sleep(1)

    w.start()
    # date_select = input("是否自动生成当日日期？(y/n):")
    # if date_select == "y":
    #     today = datetime.now().strftime('%Y%m%d')
    # else:
    #     today = input("手动输入日期 yyyymmdd: ")

    today, today_slope, today_line, yesterday, yes_slope, yes_line = Generate_Date(tradeDaysPath, today)
    print("")
    # print(today, today_slope, today_line, yesterday, yes_slope, yes_line)

    # 1.获取所有买单股票代码
    # stock_code_buy_list = get_code_list_from_csv()

    stock_code_buy_list = get_all_stcok_from_wind()

    # stock_code_buy_list = []
    # print("股票个数：", len(stock_code_buy_list))

    # 2.获取前收盘价和计算涨停价
    # 这里的作用是为了保证不管这个文件里有没有东西，都要把交易程序跑起来的保证。特别是YH
    if len(stock_code_buy_list) == 0:
        stock_code_buy_list.append("601669.SH")
    # print("get start")
    start_time = time.time()

    top_limit_price_dict = dict()

    # 3.生成指定格式的文件A
    save_dir = fr"{documents_path}/limit_price"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    limit_price_path = f"{save_dir}/{next_trade_day}_limit_price.csv"

    # 时间循环从这里开始：
    target_time = datetime.now().replace(hour=16, minute=30, second=0, microsecond=0)
    morning_start_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    if datetime.now() < morning_start_time:
        print("Good morning, forgot to run program yesterday?\nDont worry, I will run it for you\n")
        print("havent done this part, just restart and enter yesterday's date")


    if (datetime.now() < target_time) and not notToday:
        while datetime.now() < target_time:
            # printYellowMsg("It's not time yet")
            # wait till target time
            time.sleep(0.1)
            print("\r", end="")
            print(f"Now time: \033[33m{datetime.now()}\033[0m, Waiting for {target_time}...", end="")


    if (datetime.now() > target_time) and not notToday:
        # 检查数据源
        while True:
            # time.sleep(600) # 10分钟
            time.sleep(3)  # 3s DEBUG
            print(f"Now {datetime.now()}, checking data source:", end="")
            try:

                test_df = get_day_k_data_wind_inFunc("000001", today, today)['VOLUME']
                # 如果 VOLUME 列为 NaN，那么就是没有数据
                if test_df.isnull().values.any():
                    print(" \033[33mData is not updated yet\033[0m", end="")
                else:
                    print(" \033[32mData is updated\033[0m", end="")
                    break
                print("\r", end="")
            except Exception as e:
                print(f"\nFAILED checking data source: {e}")
                continue
    elif not notToday:
        print("It's not time yet")
        # wait till target time
        while datetime.now() < target_time:
            time.sleep(1)
            print(f"Waiting for {target_time}...")

    print("")


    # 从 limit_price_path 读取数据，获取第一列，即所有已经下载的股票，转成liswt
    if os.path.exists(limit_price_path):
        try:
            df = pd.read_csv(limit_price_path)
            limit_price_file_already_exist_stock_list = df["证券代码"].tolist()
            # 把每个元素后缀去掉，换句话说，只留前六位
            limit_price_file_already_exist_stock_list = [x[:6] for x in limit_price_file_already_exist_stock_list]
        except Exception as e:
            print(f"FAILED reading {limit_price_path}: {e}\ncheck file plz, delete file if needed")
            limit_price_file_already_exist_stock_list = []

        # print(f"已经下载的股票代码：{stock_code_buy_list}")
    else:
        # 如果文件不存在，那么就。。什么也不做
        limit_price_file_already_exist_stock_list = []
        print(f"{limit_price_path} file is not exist")


    ret_data = []
    print("\n")
    # 检查是否已经下载过了
    if os.path.exists(limit_price_path):
        if len(limit_price_file_already_exist_stock_list) == 0:
            print("No stock code in limit price file, Will download all stock code")
        elif len(limit_price_file_already_exist_stock_list) == len(stock_code_buy_list):
            print("All stock code in limit price file, No need to download")
            input("press enter to return to main menu")
            return
        elif len(limit_price_file_already_exist_stock_list) > 0:
            print("Some stock code in limit price file, Will download the rest of stock code")
            # 对比 limit_price_file_already_exist_stock_list 和 stock_code_buy_list，如果已经下载过了，就不再下载
            stock_code_buy_list = list(set(stock_code_buy_list) - set(limit_price_file_already_exist_stock_list))
            print(f"left {len(stock_code_buy_list)} left stock code to download")
            print(f"already downloaded {len(limit_price_file_already_exist_stock_list)} stock code")
    else:
        print("No limit price file, Will download all stock code")

    print(f'Downloading {today}\'s data')

    subprocess.Popen([
        "powershell",
        "-Command",
        f'Start-Process powershell -ArgumentList \'-NoExit -Command "Get-Content -Path \\"{limit_price_path}\\" -Wait"\''
    ])

    for index, stock_code in tqdm(enumerate(stock_code_buy_list),
                                  desc="DOWNLOADING",
                                  ncols=100,
                                  bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} Stocks [Elapsed: {elapsed} | ETA: {remaining}]",
                                  total=len(stock_code_buy_list)
                                  ):

        pre_close_data = get_day_k_data_wind_inFunc(stock_code, today, today)["CLOSE"]
        if pre_close_data.empty:
            print(index, ":", stock_code, "FAILED DOWNLOADING LIMIT PRICE DATA.")
            continue

        # data=get_day_k_data_bs(stock_code, yesterday, yesterday)["CLOSE"]
        # if len(data)>0:
        #     pre_close = data[0]
        # else:
        #     pre_close = 50
        pre_close = pre_close_data[0]
        top_limit_price, down_limit_price = get_rise_down_stop_price(stock_code, pre_close)

        if stock_code.startswith("0") or stock_code.startswith("3"):
            stock_code = stock_code + ".SZ"
        elif stock_code.startswith("6"):
            stock_code = stock_code + ".SH"
        elif stock_code.startswith("8"):
            continue
        # print(pre_close, top_limit_price, down_limit_price)

        # 每获取一条数据就追加写入 CSV 文件
        data_to_append = [[stock_code, pre_close, top_limit_price, down_limit_price]]
        df_data = pd.DataFrame(data=data_to_append, columns=["证券代码", "昨日收盘价", "今日涨停价", "今日跌停价"])
        df_data.to_csv(limit_price_path, mode='a', header=not os.path.exists(limit_price_path), index=False)

        ret_data.append([stock_code, pre_close, top_limit_price, down_limit_price])
        # if index % 1000 == 0:
        #     print(index, ":", stock_code + ":  涨停价  " + str(top_limit_price) + "   跌停价  " + str(down_limit_price))
    # 最终数据框的保存（可以根据需要保留或删除）
    final_df_data = pd.DataFrame(data=ret_data, columns=["证券代码", "昨日收盘价", "今日涨停价", "今日跌停价"])
    final_df_data.to_csv(limit_price_path, mode='a', header=not os.path.exists(limit_price_path), index=False)


    # df_data = pd.DataFrame(data=ret_data, columns=["证券代码", "昨日收盘价", "今日涨停价", "今日跌停价"])
    # df_data.to_csv(limit_price_path, index=False)

    print("End getting limit price")
    # print("获取前收盘价计算今涨停价和跌停价 结束")

    print(f"file saved to {limit_price_path}")
    end_time = time.time()
    print("It takes: ", int(end_time - start_time) / 60, "min")  # 用时 2093 秒=30分钟

    input("press enter to return to main menu")

downloadLimitpriceData_auto()