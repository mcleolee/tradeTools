
# VERSION 1.4.1

from datetime import datetime, timedelta, date
import pandas as pd
import shutil
import os
import chardet
import time
import csv
import threading
from tqdm import tqdm

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import tushare as ts

TUSHARE_TOKEN = "d5b0e880343ac5de428f0216b29739fd91174ab03a9e96c61e9c737f"
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

signalSyncOn15Path = rf'C:\Users\progene12\Desktop\Start Trading\signal'  # 在我的电脑15上的信号文件夹
debug = 0

def appendToListIfNotExists(list, item):
    if item not in list:
        list.append(item)

def clear_screen():
    """
    @brief 清屏函数，根据操作系统执行相应命令
    """
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux 或 macOS
        os.system('clear')


def get_trade_date(year):
    """
    @brief 获取指定日期范围内的交易日列表
    @param year: 年份
    @return: 交易日列表
    """
    # 获取用户的文档文件夹路径
    try:
        documents_folder = os.path.expanduser("~/Documents")
        # 构造交易日文件名
        trade_dates_file = os.path.join(documents_folder, f"{year}_tradeDates.csv")
        # file.saveAsUft8(trade_dates_file)
        # 读取交易日文件
        if os.path.isfile(trade_dates_file):
            trade_dates_df = pd.read_csv(trade_dates_file)
            # 假设CSV文件中有一列名为'Date'
            return trade_dates_df['date'].tolist()
        else:
            raise FileNotFoundError(f"No file of tradeDates is found: {trade_dates_file}")
    except Exception as e:
        prt.redMsg(f"failed getting the trade date: {e}")


class prt:
    @staticmethod
    def n(nNum=1):
        print("\n" * nNum)

    @staticmethod
    def blackMsg(text):
        print(f"\033[30m{text}\033[0m")
        return f"\033[30m{text}\033[0m"

    @staticmethod
    def redMsg(text):
        print(f"\033[31m{text}\033[0m")
        return f"\033[31m{text}\033[0m"

    @staticmethod
    def greenMsg(text):
        print(f"\033[32m{text}\033[0m")
        return f"\033[32m{text}\033[0m"

    @staticmethod
    def yellowMsg(text):
        print(f"\033[33m{text}\033[0m")
        return f"\033[33m{text}\033[0m"

    @staticmethod
    def blueMsg(text):
        print(f"\033[34m{text}\033[0m")
        return f"\033[34m{text}\033[0m"

    @staticmethod
    def magentaMsg(text):
        print(f"\033[35m{text}\033[0m")
        return f"\033[35m{text}\033[0m"

    @staticmethod
    def cyanMsg(text):
        print(f"\033[36m{text}\033[0m")
        return f"\033[36m{text}\033[0m"

    @staticmethod
    def whiteMsg(text):
        print(f"\033[37m{text}\033[0m")
        return f"\033[37m{text}\033[0m"

    @staticmethod
    def printAllColumns(df):
        prt.yellowMsg(f"Printing all columns in dataframe {df}\n")
        for col in df.columns:
            print(col)

    @staticmethod
    def printDataFrameWithMaxRows(df):
        # 设置显示所有行
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        # 设置显示宽度
        pd.set_option('display.width', 1000)  # 设置为适当的值，以便显示足够的列

        prt.yellowMsg(f"Printing dataframe with max rows")
        print(df)

    @staticmethod
    # @brief Print a message with the specified text or background color.
    # @param text The message to be printed.
    # @param black red green yellow blue magenta cyan white
    # @param isBackground If 1, apply color to background; otherwise, apply to text.
    # @return None
    def colorMsg(text, color, isBackground=0):
        color_codes = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m"
        }
        background_color_codes = {
            "black": "\033[40m",
            "red": "\033[41m",
            "green": "\033[42m",
            "yellow": "\033[43m",
            "blue": "\033[44m",
            "magenta": "\033[45m",
            "cyan": "\033[46m",
            "white": "\033[47m"
        }
        reset = "\033[0m"

        # Select either text color or background color based on isBackground
        if isBackground:
            print(f"{background_color_codes.get(color, background_color_codes['white'])}{text}{reset}")
        else:
            print(f"{color_codes.get(color, color_codes['white'])}{text}{reset}")

    @staticmethod
    def headlineMsg(msg):
        """
        @brief Print a centered message in the console with dynamic border.
        @param msg: The message to be printed.
        """
        try:
            # 获取控制台的宽度
            console_width = shutil.get_terminal_size().columns
        except Exception as e:
            # 如果获取宽度失败，则使用默认值
            console_width = 80
            print(f"Warning: {e}. Using default console width of {console_width}.")

        # 设置边框长度为控制台宽度的一半
        border_length = max(len(msg) + 4, console_width // 2 - 1)  # +4 是为了边框和空格

        # 生成边框
        border = '=' * border_length
        sideLength = (border_length - len(msg) - 2) // 2
        sideBlank = ' ' * sideLength
        # 打印边框和消息
        prt.greenMsg("\n" + sideBlank + border)
        prt.greenMsg(sideBlank + f"={msg.center(border_length - 2)}=")
        prt.greenMsg(sideBlank + border + "\n")

    @staticmethod
    def boldMsg(msg):
        print(f"\033[1m{msg}\033[0m")
        return f"\033[1m{msg}\033[0m"

    @staticmethod
    def fileEncoding(filePath, chunk_size=1024):
        with open(filePath, 'rb') as f:
            raw_data = f.read(chunk_size)  # 只读取前1024字节
            result = chardet.detect(raw_data)
            # print(f'encoding: {result["encoding"]}')
            return f'encoding: {result["encoding"]}'

class file:
    def __init__(self, filePath):
        self.filePath = filePath

    @staticmethod
    def saveAsUft8(input_file: str):
        """
        @brief Converts the input file to UTF-8 encoding and saves it to the output file.
        @param input_file: The path to the input file.
        @return: None
        """
        output_file = input_file
        try:
            # 检测文件编码
            with open(input_file, 'rb') as infile:
                raw_data = infile.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] if result['encoding'] else 'ISO-8859-1'  # 如果检测不到，使用默认编码

            # 读取文件内容
            with open(input_file, 'r', encoding=encoding) as infile:
                content = infile.read()

            # 写入到新的文件
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(content)

            # print(f"Successfully converted {input_file} to UTF-8 and saved as {output_file}.")
        except Exception as e:
            print(f"An error occurred: {e} GDNXCT")
            prt.redMsg(f'detect encoding: {encoding}')

    @staticmethod
    def saveAsGBK(input_file: str):
        """
        @brief Converts the input file to GBK encoding and saves it to the output file.
        @param input_file: The path to the input file.
        @return: None
        """
        output_file = input_file
        try:
            # 检测文件编码
            with open(input_file, 'rb') as infile:
                raw_data = infile.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] if result['encoding'] else 'ISO-8859-1'  # 如果检测不到，使用默认编码

            # 读取文件内容
            with open(input_file, 'r', encoding=encoding) as infile:
                content = infile.read()

            # 写入到新的文件
            with open(output_file, 'w', encoding='gbk') as outfile:
                outfile.write(content)

            # print(f"Successfully converted {input_file} to UTF-8 and saved as {output_file}.")
        except Exception as e:
            print(f"An error occurred: {e} GDNXCG")
            prt.redMsg(f'detect encoding: {encoding}')

    @staticmethod
    def convert_all_files_encoding_in_folder(folder_path, target_encoding='utf-8'):
        """
        Convert all files in a specified folder to the target encoding.

        @param folder_path: Path to the folder containing the files.
        @param target_encoding: Target encoding to save the files (default is UTF-8).
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 只处理文件，跳过文件夹
            if os.path.isfile(file_path):
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # 以目标编码写入文件
                    with open(file_path, 'w', encoding=target_encoding) as f:
                        f.write(content)

                    print(f"Converted '{filename}' to {target_encoding} encoding.")
                except Exception as e:
                    print(f"Error converting '{filename}': {e}")

    @staticmethod
    def merge_csv_files_as_dataframe(input_files: list) -> pd.DataFrame:
        """
        @brief 合并多个CSV文件为一个DataFrame
        @param input_files CSV文件路径的列表
        @return 合并后的pandas DataFrame
        """
        dataframes = []

        # 遍历文件路径列表并读取每个CSV文件
        for file in input_files:
            try:
                df = pd.read_csv(file)
                dataframes.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")

        # 合并所有DataFrame
        if dataframes:
            merged_df = pd.concat(dataframes, ignore_index=True)
        else:
            merged_df = pd.DataFrame()  # 如果没有文件或读取失败则返回空DataFrame

        return merged_df

    @staticmethod
    def merge_dataframe_files_as_dataframe(dataframes: list) -> pd.DataFrame:
        """
        @brief 合并多个DataFrame为一个DataFrame
        @param dataframes DataFrame对象的列表
        @return 合并后的pandas DataFrame
        """
        if not dataframes:
            return pd.DataFrame()  # 如果没有DataFrame则返回空DataFrame

        try:
            # 使用concat合并DataFrame
            merged_df = pd.concat(dataframes, ignore_index=True)
        except Exception as e:
            print(f"Error merging dataframes: {e}")
            return pd.DataFrame()  # 如果发生错误，返回空DataFrame

        return merged_df

    @staticmethod
    def isFileExist(filePath):
        return os.path.exists(filePath)

    @staticmethod
    def sync_folders_incremental(pathSyncFrom, pathSyncTo, gapSec):
        """
        @brief 增量同步文件夹内容，不删除已有内容
        @param pathSyncFrom: 源文件夹路径
        @param pathSyncTo: 目标文件夹路径
        @param gapSec: 同步间隔秒数
        """

        def sync_dir(src_dir, dst_dir):
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            for item in os.listdir(src_dir):
                src_path = os.path.join(src_dir, item)
                dst_path = os.path.join(dst_dir, item)

                if os.path.isdir(src_path):
                    sync_dir(src_path, dst_path)
                else:
                    # 文件不存在或源文件更新时进行复制
                    if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                        shutil.copy2(src_path, dst_path)
                        print(f"Copied file {src_path} to {dst_path}")

        while True:
            sync_dir(pathSyncFrom, pathSyncTo)
            print(f"Synchronized from {pathSyncFrom} to {pathSyncTo}")
            time.sleep(gapSec)

    def sync_folders_incremental_visual(pathSyncFrom, pathSyncTo, gapSec):
        """
        @brief 增量同步文件夹内容，不删除已有内容
        @param pathSyncFrom: 源文件夹路径
        @param pathSyncTo: 目标文件夹路径
        @param gapSec: 同步间隔秒数
        """

        def sync_dir(src_dir, dst_dir):
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            for item in os.listdir(src_dir):
                src_path = os.path.join(src_dir, item)
                dst_path = os.path.join(dst_dir, item)

                if os.path.isdir(src_path):
                    sync_dir(src_path, dst_path)
                else:
                    if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                        shutil.copy2(src_path, dst_path)

        last_sync_time = None

        print("")

        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sync_dir(pathSyncFrom, pathSyncTo)

            # 更新上一次同步成功的时间
            last_sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 在同一行更新输出
            print(f"\rCurrent time: {current_time} | Last sync: {last_sync_time}", end="")

            time.sleep(gapSec)

    # 示例调用
    # sync_folders_incremental("path/to/source", "path/to/destination", 3600)

    # @staticmethod
    # def get_latest_modified_file(dir):
    #     """
    #     @brief 获取指定目录下最新修改的文件
    #     @param dir: 目录路径
    #     @return: 最新修改的文件路径
    #     """
    #     files = os.listdir(dir)
    #     paths = [os.path.join(dir, basename) for basename in files]
    #     return max(paths, key=os.path.getmtime)
    #
    # @staticmethod
    # def get_latest_created_file(dir):
    #     """
    #     @brief 获取指定目录下最新创建的文件
    #     @param dir: 目录路径
    #     @return: 最新创建的文件路径
    #     """
    #     files = os.listdir(dir)
    #     paths = [os.path.join(dir, basename) for basename in files]
    #     return max(paths, key=os.path.getctime)
    #
    # @staticmethod
    # def get_file_size(file_path):
    #     """
    #     @brief 获取指定文件的大小
    #     @param file_path: 文件路径
    #     @return: 文件大小
    #     """
    #     return os.path.getsize(file_path)
    #
    # @staticmethod
    # def get_file_extension(file_path):
    #     """
    #     @brief 获取指定文件的扩展名
    #     @param file_path: 文件路径
    #     @return: 文件扩展名
    #     """
    #     return os.path.splitext(file_path)[1]
    #
    # @staticmethod
    # def get_file_name(file_path):
    #     """
    #     @brief 获取指定文件的文件名
    #     @param file_path: 文件路径
    #     @return: 文件名
    #     """
    #     return os.path.basename(file_path)
    #
    # @staticmethod
    # def get_file_name_without_extension(file_path):
    #     """
    #     @brief 获取指定文件的不带扩展名的文件名
    #     @param file_path: 文件路径
    #     @return: 不带扩展名的文件名
    #     """
    #     return os.path.splitext(os.path.basename(file_path))[0]
    #
    # @staticmethod
    # def get_file_path_without_extension(file_path):
    #     """
    #     @brief 获取指定文件的不带扩展名的文件路径
    #     @param file_path: 文件路径
    #     @return: 不带扩展名的文件路径
    #     """
    #     return os.path.splitext(file_path)[0]
    #
    # @staticmethod
    # def get_file_path(file_path):
    #     """
    #     @brief 获取指定文件的
    #     @param file_path: 文件路径
    #     @return: 不带扩展名的文件路径
    #     """
    #     ...

class ScanTrade:
    '''
    self.signalPath = rf"{self.syncPath}\Sell_Buy_List_{self.product}" 下有今天的信号文件，
    命名规则是：
    SellOrderListCF15_20241031.csv JinRiChiCangCF15_20241031.csv BuyOrderListCF15_20241031.csv
    这是三个原始信号，20241031是今天的日期，为self.today
    然后有4个实时信号，
    SellOrderListCF15morning_20241031.csv
    SellOrderListCF15morning2Two_20241031.csv
    SellOrderListCF15afternoon_20241031.csv
    BuyOrderListCF15afternoon2Two_20241031.csv
    其中每次实时信号都带有一个jrcc文件，如
    JinRiChiCangCF15morning_20241031.csv
    4个实时信号可能有，如果有信号那就是上面四个格式；如果没有，那就会是一个txt文件：
    NoSellingMorning_20241031.txt
    NoSellingMorning2Two_20241031.txt
    NoSellingAfternoon_20241031.txt
    NoBuyingAfternoon2Two_20241031.txt
    '''

    def __init__(self, product, projectPath=None, syncPath=None, insOrderPath=None, today=None):
        self.today = getDate('')
        self.projectPath = rf"C:\Users\Administrator\Desktop\兴业证券多账户交易"  # PARAS
        self.syncPath = rf"E:\BaiduSyncdisk"  # PARAS
        self.insOrderPath = rf"C:/Program Files/SmartTrader-Max/InsOrder"  # PARAS
        self.product = product

        # 如果产品名包含 HT02，FL22，那么就是分帐户的产品
        if 'HT02' in product or 'FL22' in product:
            self.isDividedAccount = True
        else:
            self.isDividedAccount = False


        self.twapPath = rf"{self.projectPath}\{product}\{product}_Orders/{self.today}"
        self.signalPath = rf"{self.syncPath}\Sell_Buy_List_{self.product}"
        self.ordersPath = rf"{self.insOrderPath}\orders.csv"
        self.assetPath = rf"{self.insOrderPath}\asset.csv"
        self.taskPath = rf"{self.insOrderPath}\Task.csv"

        # twap 的分单
        self.twap_1_buy  = self.load_order_data("BuyOrderList1")
        self.twap_2_buy  = self.load_order_data("BuyOrderList2")
        self.twap_3_buy  = self.load_order_data("BuyOrderList3")
        self.twap_4_buy  = self.load_order_data("BuyOrderList4")
        self.twap_5_buy  = self.load_order_data("BuyOrderList5")
        self.twap_6_buy  = self.load_order_data("BuyOrderList6")
        self.twap_1_sell = self.load_order_data("SellOrderList1")
        self.twap_2_sell = self.load_order_data("SellOrderList2")
        self.twap_3_sell = self.load_order_data("SellOrderList3")
        self.twap_4_sell = self.load_order_data("SellOrderList4")
        self.twap_5_sell = self.load_order_data("SellOrderList5")
        self.twap_6_sell = self.load_order_data("SellOrderList6")

        self.twap_list = [self.twap_1_buy, self.twap_2_buy, self.twap_3_buy,
                          self.twap_4_buy, self.twap_5_buy, self.twap_6_buy,
                          self.twap_1_sell, self.twap_2_sell, self.twap_3_sell,
                          self.twap_4_sell, self.twap_5_sell, self.twap_6_sell]

        # self.todaySignalList =

        # 信号数据
        self.signal_list = []
        # 有信号：morning
        # 无信号：Morning
        self.sellOrderList = self.load_signal_data_sell()
        self.buyOrderList = self.load_signal_data_buy()
        self.jrcc = self.load_signal_data("JinRiChiCang")
        self.morning_1 = self.load_signal_data("morning")
        self.morning_2 = self.load_signal_data("morning2Two")
        self.afternoon_1 = self.load_signal_data("afternoon")
        self.afternoon_2 = self.load_signal_data("afternoon2Two")



        self.isTwapDataReady = self.checkDataReady()

    def __str__(self):
        return f"ScanTrade product: {self.product}, Data is ready: {self.isTwapDataReady}, Divided Account: {self.isDividedAccount}"

    def load_signal_data_sell(self):
        filePath = rf"D:\TRADE\RTrade\signal\Sell_Buy_List_{self.product}\SellOrderList{self.product}_{self.today}.csv"
        if os.path.exists(filePath):
            return pd.read_csv(filePath, encoding='utf-8')
        else:
            return pd.DataFrame()

    def load_signal_data_buy(self):
        filePath = rf"D:\TRADE\RTrade\signal\Sell_Buy_List_{self.product}\BuyOrderList{self.product}_{self.today}.csv"
        if os.path.exists(filePath):
            return pd.read_csv(filePath, encoding='utf-8')
        else:
            return pd.DataFrame()




    def load_order_data(self, order_type):
        """
        @brief 读取指定类型的订单数据，若文件不存在或读取失败则返回空DataFrame
        @param order_type: 订单类型名称
        @return DataFrame: 订单数据
        """
        file_path = rf"{self.twapPath}/{order_type}_{self.today}.csv"
        try:
            if os.path.exists(file_path):
                return pd.read_csv(file_path, encoding='utf-8')

            else:
                prt.yellowMsg(f"Warning: {file_path} does not exist.")
                return pd.DataFrame()  # 返回空DataFrame
        except Exception as e:
            prt.redMsg(f"Error reading {file_path}: {e}")
            return pd.DataFrame()  # 返回空DataFrame

    def load_signal_data(self, signal_type):
        """
        @brief 读取信号数据，若文件不存在或读取失败则返回空列表
        @param signal_type: 信号类型（如SellOrderList, BuyOrderList, JinRiChiCang, morning等）
        @return List: 包含每个信号文件路径的列表
        TODO 如果是分帐户的还要单独搞
        """
        patterns = {
            "SellOrderList": [f"SellOrderList{self.product}_{self.today}.csv"],
            "BuyOrderList": [f"BuyOrderList{self.product}_{self.today}.csv"],
            "JinRiChiCang": [f"JinRiChiCang{self.product}_{self.today}.csv"],
            "morning": [f"SellOrderList{self.product}morning_{self.today}.csv",
                        f"JinRiChiCang{self.product}morning_{self.today}.csv"],
            "morning2Two": [f"SellOrderList{self.product}morning2Two_{self.today}.csv",
                            f"JinRiChiCang{self.product}morning2Two_{self.today}.csv"],
            "afternoon": [f"SellOrderList{self.product}afternoon_{self.today}.csv",
                          f"JinRiChiCang{self.product}afternoon_{self.today}.csv"],
            "afternoon2Two": [f"BuyOrderList{self.product}afternoon2Two_{self.today}.csv",
                              f"JinRiChiCang{self.product}afternoon2Two_{self.today}.csv"]
        }

        # 检查信号文件存在性
        for pattern in patterns.get(signal_type, []):
            file_path = os.path.join(self.signalPath, pattern)
            if os.path.exists(file_path):
                self.signal_list.append(file_path)
            else:
                # 检查无信号的txt文件，判断是Selling还是Buying
                no_signal_file = f"No{'Buying' if 'afternoon2Two' in signal_type else 'Selling'}{signal_type.capitalize()}_{self.today}.txt"
                no_signal_path = os.path.join(self.signalPath, no_signal_file)
                if os.path.exists(no_signal_path):
                    print(f"Info: No {signal_type} signal for {self.today}")
                    self.signal_list.append(no_signal_path)
                    break

        # return self.signal_list

    def getOrderNumber(self):
        return len(self.twap_1_buy)

    def checkDataReady(self):
        for twap in self.twap_list:
            if twap.empty:
                return False
        return True

    def update_twap_data(self):
        self.twap_1_buy  = self.load_order_data("BuyOrderList1")
        self.twap_2_buy  = self.load_order_data("BuyOrderList2")
        self.twap_3_buy  = self.load_order_data("BuyOrderList3")
        self.twap_4_buy  = self.load_order_data("BuyOrderList4")
        self.twap_5_buy  = self.load_order_data("BuyOrderList5")
        self.twap_6_buy  = self.load_order_data("BuyOrderList6")
        self.twap_1_sell = self.load_order_data("SellOrderList1")
        self.twap_2_sell = self.load_order_data("SellOrderList2")
        self.twap_3_sell = self.load_order_data("SellOrderList3")
        self.twap_4_sell = self.load_order_data("SellOrderList4")
        self.twap_5_sell = self.load_order_data("SellOrderList5")
        self.twap_6_sell = self.load_order_data("SellOrderList6")

        self.twap_list = [self.twap_1_buy, self.twap_2_buy, self.twap_3_buy,
                          self.twap_4_buy, self.twap_5_buy, self.twap_6_buy,
                          self.twap_1_sell, self.twap_2_sell, self.twap_3_sell,
                          self.twap_4_sell, self.twap_5_sell, self.twap_6_sell]

        self.isTwapDataReady = self.checkDataReady()




def format_to_datetime(value):
    """
    @brief Convert value to a datetime object if it is str, int, or date.
    @param value, Value to be converted, can be str, int, date, or datetime.
    @return datetime object.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, int):
        value_str = str(value)
        if len(value_str) == 10:  # Unix timestamp
            return datetime.fromtimestamp(value)
        elif len(value_str) == 8:  # Assume YYYYMMDD format
            return datetime.strptime(value_str, '%Y%m%d')
        else:
            raise ValueError(f"Integer '{value}' does not match known date formats.")
    if isinstance(value, str):
        formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%H:%M:%S', '%H:%M']
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Value '{value}' does not match any known datetime format.")

    raise TypeError(f"Unsupported type '{type(value)}' for datetime conversion.")


def isDatetimeABeforeB(a, b):
    """
    @brief Check if datetime A is before datetime B.
    @param a Start date or time, can be str, int, or datetime.
    @param b End date or time, can be str, int, or datetime.
    @return True if A is before B, False otherwise.
    """
    a_dt = format_to_datetime(a)
    b_dt = format_to_datetime(b)
    return a_dt < b_dt


def isDatetimeAAfterB(a, b):
    """
    @brief Check if datetime A is after datetime B.
    @param a Start date or time, can be str, int, or datetime.
    @param b End date or time, can be str, int, or datetime.
    @return True if A is after B, False otherwise.
    """
    a_dt = format_to_datetime(a)
    b_dt = format_to_datetime(b)
    return a_dt > b_dt


def getNextTradeDateIfNotTradeDate(trade_dates: list, target_date: date) -> str:
    """
    @brief 如果输入日期不是交易日，找到下一个有效的交易日
    @param trade_dates: 交易日列表，格式为 YYYY-MM-DD
    @param target_date: 输入日期
    @return 下一个交易日 yyyy-mm-dd
    """
    target_str = target_date.strftime('%Y-%m-%d')
    if target_str in trade_dates:
        return target_str  # 是交易日，直接返回
    for trade_date in trade_dates:
        if trade_date > target_str:
            return trade_date  # 找到下一个交易日
    return None


def getNextTradeDate(target_date: str) -> str:
    """
    @brief 找到下一个交易日
    @param target_date: 输入日期，格式为 YYYY-MM-DD
    @return 下一个交易日，格式为 YYYY-MM-DD
    """
    # 转换字符串为日期对象
    target_date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()

    # 获取目标日期的年份
    year = target_date_obj.year

    # 获取指定年份的所有交易日
    trade_dates = get_trade_date(year)

    # 将交易日字符串转换为日期对象
    # TODO 似乎用了太多时间
    trade_dates_obj = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in trade_dates]

    # 找到下一个交易日
    for trade_date in trade_dates_obj:
        if trade_date > target_date_obj:
            return trade_date.strftime('%Y-%m-%d')  # 返回格式化后的交易日

    return None  # 如果没有找到下一个交易日


def get_third_friday(year: int, month: int) -> date:
    """
    @brief 获取指定月份的第三个周五
    @param year: 年份
    @param month: 月份
    @return 该月份的第三个周五的日期
    """
    first_day_of_month = date(year, month, 1)  # 使用date而不是datetime.date
    first_friday_offset = (4 - first_day_of_month.weekday()) % 7  # 找到第一个周五
    third_friday = first_day_of_month + timedelta(days=first_friday_offset + 14)
    return third_friday


def get_third_friday_date(year: int, month: int) -> str:
    """
    @brief 获取指定月份的第三个星期的最后一个交易日
    @param year: 年份
    @param month: 月份
    @return 该月份第三个星期的最后一个交易日
    """
    trade_dates = get_trade_date(year)

    # 第一步：找到该月的第一个周五
    first_day_of_month = date(year, month, 1)  # 当月的第一天
    first_friday_offset = (4 - first_day_of_month.weekday()) % 7  # 找到第一个周五
    third_friday = first_day_of_month + timedelta(days=first_friday_offset + 14)  # 第三个周五

    # 第二步：找到第三个星期的最后一个交易日，如果不是交易日，顺延到下一个交易日
    third_week_last_trade_date = None
    for trade_date in trade_dates:
        trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        # 如果当前交易日在第三个星期内或之后，并且还未找到最后一个交易日
        if trade_date_obj >= third_friday:
            third_week_last_trade_date = trade_date
            break  # 找到第一个有效交易日后就可以停止
        else:
            third_week_last_trade_date = trade_date  # 继续查找

    # 如果找到的最后一个交易日不是交易日，顺延到下一个交易日
    if third_week_last_trade_date is not None:
        last_trade_date_obj = datetime.strptime(third_week_last_trade_date, '%Y-%m-%d').date()
        while third_week_last_trade_date not in trade_dates:
            last_trade_date_obj += timedelta(days=1)
            third_week_last_trade_date = last_trade_date_obj.strftime('%Y-%m-%d')

    return third_week_last_trade_date


def get_first_trade_date_of_week(target_date: date) -> str:
    """
    @brief 找到某个日期所在周的第一个交易日
    @param trade_dates: 交易日列表，格式为 YYYY-MM-DD
    @param target_date: 要查找的日期所在周
    @return 该周的第一个交易日
    # IC2403的当季合约换月这里返回了None
    """
    # 找到target_date所在周的第一个交易日
    trade_dates = get_trade_date(target_date.year)
    start_of_week = target_date - timedelta(days=target_date.weekday())  # 获取该周的周一
    for trade_date in trade_dates:
        trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        if start_of_week <= trade_date_obj <= target_date:
            return trade_date
        # 若没有找到所在周的第一个交易日，则调用 getNextTradeDateIfNotTradeDate 查找下一个交易日
    return getNextTradeDateIfNotTradeDate(trade_dates, start_of_week)



def get_third_week_first_trade_date(year: int, month: int) -> str:
    """
    @brief 获取指定月份的第三个星期的第一个交易日
    @param trade_dates: 交易日列表，格式为 YYYY-MM-DD
    @param year: 年份
    @param month: 月份
    @return 该月份第三个星期的第一个交易日
    """
    # 找到该月的第三个星期的第一天（周一）
    trade_dates = get_trade_date(year)
    first_day_of_month = date(year, month, 1)
    first_monday_offset = (7 - first_day_of_month.weekday()) % 7  # 找到第一个周一
    third_monday = first_day_of_month + timedelta(days=first_monday_offset + 14)  # 第三个周一

    # 找到该周的第一个交易日
    return get_first_trade_date_of_week(third_monday)


def get_first_trade_date_of_month(year: int, month: int) -> str:
    """
    @brief 找到指定月份的第一个交易日
    @param year: 年份
    @param month: 月份
    @return 该月份的第一个交易日
    """
    # 找到指定年份和月份的第一个交易日
    trade_dates = get_trade_date(year)
    for trade_date in trade_dates:
        trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        if trade_date_obj.year == year and trade_date_obj.month == month:
            return trade_date  # 返回该月的第一个交易日
    return None


def get_all_trade_dates_of_month(year: int, month: int) -> list:
    """
    @brief 获取指定月份的所有交易日
    @param year: 年份
    @param month: 月份
    @return 该月份的所有交易日列表
    """
    # 获取指定年份的所有交易日
    trade_dates = get_trade_date(year)
    # 筛选出指定月份的交易日
    return [trade_date for trade_date in trade_dates if datetime.strptime(trade_date, '%Y-%m-%d').date().month == month]


def getContractStartDate(yearMonth: int) -> str:
    """
    @brief 获取主力合约的起始日期，倒推两个月并找到第三个星期的第一个交易日
    @param yearMonth: 年月，例如 2201 表示 2022 年 1 月
    @return 合约的起始日期，格式为 YYYY-MM-DD
    """
    # 将两位数年份转换为四位数年份，假设年份 >= 2000
    year = (yearMonth // 100) + 2000
    month = yearMonth % 100

    # 倒推两个月
    if month == 1:
        # 如果当前月份是1月，倒推两个月到去年的11月
        year -= 1
        month = 11
    elif month == 2:
        # 如果当前月份是2月，倒推两个月到去年的12月
        year -= 1
        month = 12
    else:
        # 如果当前月份大于2，直接减去2个月
        month -= 2

    # 找到倒推后月份的第三个星期的第一个交易日
    contract_start_date = get_third_week_first_trade_date(year, month)

    return contract_start_date


def getContractEndDate(yearMonth: int) -> str:
    """
    @brief 获取主力合约的结束日期，找到合约到期月份的第三个星期的最后一个交易日
    @param yearMonth: 年月，例如 2201 表示 2022 年 1 月
    @return 合约的结束日期，格式为 YYYY-MM-DD
    """
    # 将两位数年份转换为四位数年份，假设年份 >= 2000
    year = (yearMonth // 100) + 2000
    month = yearMonth % 100

    # 找到合约到期月份的第三个星期的最后一个交易日
    contract_end_date = get_third_friday_date(year, month)

    return contract_end_date


def getMainContractRolloverDate(yearMonth: int) -> str:
    """
    @brief 获取主力合约换月日期，是到期日当周第一个交易日
    @param yearMonth: 年月，例如 2201 表示 2022 年 1 月
    @return 主力合约换月日期，格式为 YYYY-MM-DD
    TODo IC2402 会报错，因为很特殊; 已解决
    """

    # 将两位数年份转换为四位数年份，假设年份 >= 2000
    year = (yearMonth // 100) + 2000
    month = yearMonth % 100

    # 获取该年份所有交易日列表
    trade_dates = get_trade_date(year)  # 需要定义 get_trade_date 函数

    # 找到该月份的第三个周五
    third_friday = get_third_friday(year, month)

    # 确保第三个周五是交易日
    third_friday_trade_date = getNextTradeDateIfNotTradeDate(trade_dates, third_friday)

    # 找到第三个周五所在周的第一个交易日
    rollover_date = get_first_trade_date_of_week(third_friday)

    # 确保换月日期是交易日
    if rollover_date is not None:
        rollover_trade_date = getNextTradeDateIfNotTradeDate(trade_dates,
                                                         datetime.strptime(rollover_date, '%Y-%m-%d').date())
    else:  # 如果找不到第三个周五所在周的第一个交易日，就用第三个周五的下一个交易日
        rollover_trade_date = third_friday_trade_date


    if debug:
        print(f"yearMonth: {yearMonth}")
        print(f"year: {year}")
        print(f"month: {month}")
        # print(f"trade_dates: {trade_dates}")
        print(f"third_friday: {third_friday}")
        # print(f"third_friday_trade_date: {third_friday_trade_date}")
        print(f"rollover_date: {rollover_date}")
        print(f"rollover_trade_date: {rollover_trade_date}")

    return rollover_trade_date


def getSubContractRolloverDate(yearMonth: int) -> str:
    '''
    次主力合约的更换，按主力合约到期日的下一个交易日的14点作为换月时间
    主力合约就是次主力合约的上一个合约，注意yearMonth的正确更换
    :param yearMonth:
    :return:
    '''
    # 计算对应的主力合约
    # 如果yearMonth是1月份，那么主力合约就是上一年的12月份
    if yearMonth % 100 == 1:
        yearMonth -= 89
    else:
        yearMonth -= 1

    rolloverDate = getNextTradeDate(getContractEndDate(yearMonth))

    if rolloverDate is None:
        rolloverDate = getNextTradeDateIfNotTradeDate(get_trade_date(yearMonth // 100 + 2000), getContractEndDate(yearMonth))

    if debug:
        print(f"==============================================")
        print(f"= Now is sub contract")
        print(f"= main contract: yearMonth: {yearMonth}")
        print(f"= rolloverDate: {rolloverDate}")
        print(f"==============================================")

    return rolloverDate

def getCurrentAndNextSeasonRolloverDate(yearMonth: int) -> str:
    '''
    @brief 获取当季和次季合约换月日期，是到期日倒推一个月，当周的第一个交易日
            比如IC2106的换月日期是2021 06 18倒推一个月，就是20210518，当周的第一个交易日20210517
    :param yearMonth: 年月，例如 2201 表示 2022 年 1 月
    :return: 换月日期，格式为 YYYY-MM-DD
    '''

    year = yearMonth // 100 + 2000
    month = yearMonth % 100

    # 获取第三个星期的最后一个交易日，假设这是合约的到期日
    expiry_date_str = get_third_friday_date(year, month)
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

    # 倒推一个月
    rollover_month = (expiry_date.month - 1) if expiry_date.month > 1 else 12
    rollover_year = expiry_date.year if expiry_date.month > 1 else expiry_date.year - 1
    rollover_date = date(rollover_year, rollover_month, expiry_date.day)

    # 获取倒推一个月后的第三个星期的第一个交易日
    # IC2403的当季合约换月这里返回了None
    rollover_first_trade_date = get_first_trade_date_of_week(rollover_date)

    if rollover_date is None:
        rollover_date = getNextTradeDateIfNotTradeDate(get_trade_date(rollover_year), rollover_date)

    if debug:
        print(f"yearMonth: {yearMonth}")
        print(f"year: {year}")
        print(f"month: {month}")
        print(f"expiry_date_str: {expiry_date_str}")
        print(f"rollover_first_trade_date: {rollover_first_trade_date}")
        # print(f"trade_dates: {trade_dates}")
        # print(f"third_friday: {third_friday}")
        # print(f"third_friday_trade_date: {third_friday_trade_date}")
        print(f"rollover_date: {rollover_date}")
        # print(f"rollover_trade_date: {rollover_trade_date}")


    return rollover_first_trade_date


def format_dateString_to_YYYYMMDD(date_str):
    """
    @brief Formats a date string to YYYYMMDD format.
    @param date_str: The input date string, which can have various separators.
    @return: A string in the format YYYYMMDD.
    """
    import re
    # 使用正则表达式提取年份、月份和日期
    match = re.match(r'(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})', date_str)
    if match:
        year, month, day = match.groups()
        return f"{year}{month.zfill(2)}{day.zfill(2)}"
    else:
        raise ValueError("Invalid date format")


def format_YYYYMMDD_to_date(date_str) -> date:
    """
    @brief Formats a date string in YYYYMMDD format to a date object.
    @param date_str: The input date string in the format YYYYMMDD.
    @return: A date object.
    """
    return datetime.strptime(date_str, '%Y%m%d').date()


def format_YYYYMMDD_with_separator(date_str, separator=''):
    """ @brief 给YYYYMMDD格式的日期加上分隔符
        @param date_str 传入的日期字符串，如'20240101'
        @return 返回带分隔符的日期，如 '2024-01-01'
    """
    return f"{date_str[:4]}{separator}{date_str[4:6]}{separator}{date_str[6:]}"


def getDate(seperator: str, deltaDays: int = 0) -> str:
    """
    @brief 返回指定日期格式的字符串
    @param seperator: 用于分割日期部分的字符，如“-”或“/”
    @param deltaDays: 距离今天的天数偏移，负值表示过去的日期，正值表示未来的日期
    @return 返回格式化的日期字符串，格式为 YYYY[seperator]MM[seperator]DD
    """
    target_date = datetime.now() + timedelta(days=deltaDays)
    return target_date.strftime(f"%Y{seperator}%m{seperator}%d")

def get_formated_order_XY_single(fund_account, code, direction, quantity, date, s_index, is_init=False, limit_price=None):


    def order_format_st(fund_account, df_divide_order, date, s_index, is_init=False, limit_price=None):
        """
        fund_account: 资金账号
        df_divide_order: 对交易信号分单后的df, 列名有"code", "direction","quantity"，其中code为str类型
        date: 日期, "yyyymmdd"
        s_index: 用来生成外部编号（唯一标识）
        is_init: 兴业smart软件是否初始化的标志
        limit_price: 报单价格，可传入值或者列表
        """
        # 重设索引，以便之后赋值不会出现None值
        df_divide_order = df_divide_order.reset_index(drop=True)
        order_len = len(df_divide_order)

        # 转化为smart格式
        column_list = ["指令编号", "下单指令", "账户类型", "资金账户", "证券代码", "市场", "委托数量", "买卖方向",
                       "委托价格", "委托类别", "委托属性", "委托编号"]
        order = pd.DataFrame(data=None, columns=column_list)
        order_id = [date + str(i) for i in range(s_index, s_index + order_len)]
        order["指令编号"] = order_id
        if not is_init:
            order["下单指令"] = "T"  # 下单
        else:
            order["下单指令"] = "I"  # 初始化
        order["账户类型"] = "0"
        order["资金账户"] = fund_account
        ticker_list = df_divide_order.code.to_list()
        ticker_list = [t[:-3] if len(t) == 9 else t for t in ticker_list]
        order["证券代码"] = ticker_list
        order["市场"] = order.证券代码.apply(lambda x: 1 if x[0] == "6" or x[0] == "9" else 2).astype("int")

        order["委托数量"] = df_divide_order.iloc[:, 2]
        order["买卖方向"] = df_divide_order.direction.astype("int")
        # print(order)

        # "委托价格", "委托类别", "委托属性", "委托编号"
        if len(order) > 0:
            for i in range(len(order)):
                direction = order.loc[i, "买卖方向"]
                # print("direction",direction)
                if limit_price is None:
                    order.loc[i, "委托属性"] = "U"
                    if direction == 1:
                        order.loc[i, "委托价格"] = 500
                    else:
                        order.loc[i, "委托价格"] = 0.1
                else:
                    if isinstance(limit_price, (int, float)):
                        order["委托价格"] = limit_price
                        order["委托属性"] = 0
                    elif isinstance(limit_price, list):
                        if len(limit_price) == order_len:
                            order["委托价格"] = limit_price
                            order["委托属性"] = 0
                        elif len(limit_price) > order_len:
                            order["委托属性"] = 0
                            for j in range(len(limit_price)):
                                order.loc[j, "委托价格"] = limit_price[j]
                                if j == order_len - 1:
                                    break
                        else:
                            for j in range(len(limit_price)):
                                order.loc[j, "委托价格"] = limit_price[j]
                                order.loc[j, "委托属性"] = 0
                            for j in range(len(limit_price), order_len, 1):
                                order.loc[j, "委托属性"] = "U"
                                if direction == 1:
                                    order.loc[j, "委托价格"] = 500
                                else:
                                    order.loc[j, "委托价格"] = 0.1
                    else:
                        print(f"limit_price={limit_price} type={type(limit_price)}")
                        input("type error, change market price order, press Enter to continue:")

                        if direction == 1:
                            order.loc[i, "委托价格"] = 500
                        else:
                            order.loc[i, "委托价格"] = 0.1

                        order.loc[i, "委托属性"] = "U"

        # 初始化报单价格
        if is_init:
            order["委托价格"] = 0.1

        order["委托类别"] = 0

        order["委托编号"] = 0
        # order["本地报单时间"] =  dt.datetime.now().strftime("%H:%M:%S")

        s_index += order_len
        order = order[order["委托数量"] > 0]

        order["委托属性"] = "U"

        # 列名筛选和指定顺序
        order = order[column_list].copy()

        return order, s_index

    df_divide_order = pd.DataFrame(data=[[code, direction, quantity]], columns=["code", "direction", "quantity"])
    order, s_index = order_format_st(fund_account, df_divide_order, date, s_index, is_init, limit_price)

    # 以上都不用


def getTime(seperator: str = ''):
    """
    @brief 获取当前时间
    @return 当前时间字符串
    """
    return datetime.now().strftime(f"%H{seperator}%M{seperator}%S")


###############################################################################################
#                                      OLD FUNCTIONS                                          #
###############################################################################################
# being use but not recommended


def printColorMsg(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m\n")
    return f"\033[{color_code}m{text}\033[0m"
    # 示例用法
    # print(colorize_text("Hello, world!", "31"))  # 红色文本
    # print(colorize_text("Hello, world!", "1;32"))  # 绿色粗体文本


def printRedMsg(text):
    print(f"\033[31m{text}\033[0m\n")
    return f"\033[31m{text}\033[0m"


def printGreenMsg(text):
    print(f"\033[32m{text}\033[0m\n")
    return f"\033[32m{text}\033[0m"


def printYellowMsg(text):
    print(f"\033[33m{text}\033[0m\n")
    return f"\033[33m{text}\033[0m"


def printBlueMsg(text):
    print(f"\033[34m{text}\033[0m\n")
    return f"\033[34m{text}\033[0m"


def printPurpleMsg(text):
    print(f"\033[35m{text}\033[0m\n")
    return f"\033[35m{text}\033[0m"


def printCyanMsg(text):
    print(f"\033[36m{text}\033[0m\n")
    return f"\033[36m{text}\033[0m"


def printWhiteMsg(text):
    print(f"\033[37m{text}\033[0m\n")
    return f"\033[37m{text}\033[0m"


def printBoldMsg(text):
    print(f"\033[1m{text}\033[0m\n")
    return f"\033[1m{text}\033[0m"


###############################################################################################
#                                    DELETED FUNCTIONS                                        #
###############################################################################################
# no longer needed but kept for reference

def getToday():
    # DELETED
    currentDatetime = datetime.now()
    today = currentDatetime.strftime("%Y%m%d")
    print(f"today is {today}\n")
    return today


def getYesterday():
    # DELETED
    currentDatetime = datetime.now()
    yesterday = currentDatetime - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    print(f"yesterday was {yesterday_str}\n")
    return yesterday_str


def get_the_date_before_20_days():
    today = datetime.now()
    the_date_before_20_days = today - timedelta(days=20)
    return the_date_before_20_days.strftime('%Y-%m-%d')



# ==============================TEST================================
# print(getMainContractRolloverDate(2402))