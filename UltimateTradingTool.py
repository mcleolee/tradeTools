# TODO 每个函数完了之后clr
# TODO 自动识别IP
# TODO 交易成功之后有没有记录，这个也自动化
# TODO 获取终端的宽度（虽然已经有了）
# TODO 自动显示当时时间和交易阶段，提示应该做怎么操作
# TODO 写一个便捷查询持仓的函数
# TODO 写 def pressAnyKeyToContinue(): 然后替换所有
# TODO 写出 UI

# TODO 在主页打印出实时信号节点和时间！！！
# TODO 把昨日的 ZS 的 format_data 通过 18 复制到浙商的服务器

# TODo 判断今天是不是周一，比如用处在：checkYesterdayDataTo37()，要是周一运行程序就会炸

# TODO 增加功能：Python HTTPS server | use muti thread!

import os
import shutil
from datetime import datetime, timedelta
import zipfile
# import requests                   # 这个不注释，在 61 上跑不了
# from bs4 import BeautifulSoup     # 这个不注释，在 40 上跑不了
import urllib.request
import csv
import tkinter as tk
from tkinter import messagebox
import sv_ttk
import re
import time
# import datetime
import threading
import xlrd
import openpyxl
import prettytable
from prettytable import PrettyTable

DEBUG_MODE = 1
# 1表示启用，但这部分代码未完成
HTTP_SERVER = 0
server40addr = "http://192.168.1.40:8000/"
smart_divide_path = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\projects\smart_data_divide.py"
diff_excel_path = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\projects\持仓差异自动化_v1.2.py"

os.system("mode con cols=200 lines=30")

product_fund_dict = {
    "CF15": "480151137",
    "FL18": "480149909",
    "HT02XY": "480167623",
    "FL18SCA": "480160777",
    "FL22SCB": "3050003937"
}

m = "morning"
m2 = "morning2Two"
a = "afternoon"
a2 = "afternoon2Two"

nom_ = "NoSellingMorning_"
nom2_ = "NoSellingMorning2Two_"
noa_ = "NoSellingAfternoon_"
noa2_ = "NoBuyingAfternoon2Two_"
underline = "_"

sell = "SellOrderList"
buy = "BuyOrderList"
jrcc = "JinRiChiCang"

divide_SC = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SC"
divide_SCA = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SCA"
divide_SCB = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\Sell_Buy_List_FL22SCB"
ori_SC = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SC\Sell_Buy_List_FL22SC"
ori_SCA = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\Sell_Buy_List_FL22SCA"
ori_SCB = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\Sell_Buy_List_FL22SCB"

g_yesterday = None

g_realTimeNode = 0


# ====================================================================================================================
# ================================================ TKINTER ============================================================
# ====================================================================================================================

# def display_message_label():
#     message = "Hello, this is a message using Label."
#     label.config(text=message)
#
# def display_message_text():
#     message = "Hello, this is a message using Text."
#     text.delete(1.0, tk.END)  # 清空Text组件中的内容
#     text.insert(tk.END, message)
#
# def display_message_text():
#     message = "Hello, this is a message using Text."
#     text.delete(1.0, tk.END)  # 清空Text组件中的内容
#     text.insert(tk.END, message)


def iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii():
    ...


# ====================================================================================================================
# ================================================ 工具函数 ============================================================
# ====================================================================================================================

def init():
    print("starting init")


def getToday():
    currentDatetime = datetime.now()
    today = currentDatetime.strftime("%Y%m%d")
    print(f"today is {today}\n")
    return today


def getYesterday():
    currentDatetime = datetime.now()
    yesterday = currentDatetime - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    print(f"yesterday was {yesterday_str}\n")
    return yesterday_str


def file_exists(file_path):
    return os.path.exists(file_path)


def copy_file(original_path, target_path):
    try:
        ret = shutil.copy(original_path, target_path)
        print(f"文件已从 {original_path} 复制到 {target_path}")
        return ret
    except IOError as e:
        print(f"无法复制文件: {e}")


def copy_latest_files(source_folder, destination_folder, fileNumber):
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 仅复制最新的四个文件
        for file in files[:fileNumber]:
            source_file = os.path.join(source_folder, file)
            destination_file = os.path.join(destination_folder, file)

            # 复制文件
            shutil.copy2(source_file, destination_folder)
            print(f"Copied: {source_file} to {destination_file}")
    except Exception as e:
        printRedMsg(f"Failed to copy files. Error: {e}")


def print_latest_files(source_folder, fileNumber):
    # 打印最新的 fileNumber 个文件名
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 获取最新的fileNumber个文件名并打印
        for filename in files[:fileNumber]:
            print(filename)
    except Exception as e:
        printRedMsg(f"Failed to print latest files. Error: {e}")


# 复制按时间顺序排列的，有指定字符的前 fileNumber 个文件
def copy_files_with_string_limited(source_folder, destination_folder, string_to_check, fileNumber):
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 计数器，用于记录已复制的文件数量
        copied_files = 0

        # 遍历文件列表
        for file in files:
            if copied_files >= fileNumber:
                break

            source_file = os.path.join(source_folder, file)

            # 检查文件名是否包含特定字符串
            if string_to_check in file:
                destination_file = os.path.join(destination_folder, file)

                # 复制文件
                shutil.copy2(source_file, destination_folder)
                print(f"Copied: {source_file} to {destination_file}")

                # 增加已复制文件数量
                copied_files += 1

    except Exception as e:
        printRedMsg(f"Failed to copy files. Error: {e}")



# 复制所有含指定字符的文件
def copy_files_with_string_no_limited(source_folder, destination_folder, string_to_check):
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 遍历文件列表
        for file in files:
            source_file = os.path.join(source_folder, file)

            # 检查文件名是否包含特定字符串
            if string_to_check in file:
                destination_file = os.path.join(destination_folder, file)

                # 复制文件 覆盖目标文件夹中的同名文件
                shutil.copy2(source_file, destination_folder)
                print(f"Copied: {source_file} to {destination_file}")

    except Exception as e:
        printRedMsg(f"Failed to copy files. Error: {e}")


# 复制所有含指定字符的文件的测试函数
def test_copy_files_with_string_no_limited(source_folder, destination_folder, string_to_check):
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 遍历文件列表
        for file in files:
            source_file = os.path.join(source_folder, file)

            # 检查文件名是否包含特定字符串
            if string_to_check in file:
                destination_file = os.path.join(destination_folder, file)

                # 复制文件
                shutil.copy2(source_file, destination_folder)
                print(f"Copied: {source_file} to {destination_file}")

    except Exception as e:
        print(f"Failed to copy files. Error: {e}")

def erase_folder_contents(folder_path):
    try:
        # 获取文件夹中的所有文件和文件夹
        items = os.listdir(folder_path)

        # 删除每个文件和清空文件夹
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                # 清空文件夹中的内容
                erase_folder_contents(item_path)
                print(f"Emptied folder: {item_path}")
        return True
    except Exception as e:
        printRedMsg(f"Failed to erase folder contents. Error: {e}")
        return False


def move_files(source_folder, destination_folder):
    try:
        # 移动文件夹中的所有文件到目标文件夹
        shutil.move(source_folder, destination_folder)
        printGreenMsg(f"All files moved from {source_folder} to {destination_folder}")
    except Exception as e:
        printRedMsg(f"Failed to move files. Error: {e}")


def move_all_files_with_string(source_folder, destination_folder, string_to_check):
    try:
        # 确保目标文件夹存在
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # 遍历源文件夹中的所有文件
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)

            # 检查是否是文件且文件名包含特定字符串
            if os.path.isfile(source_file) and string_to_check in filename:
                destination_file = os.path.join(destination_folder, filename)

                # 移动文件，如果目标文件已存在则覆盖
                shutil.move(source_file, destination_file)
                print(f"Moved: {source_file} to {destination_file}")

        printGreenMsg(f"All files containing '{string_to_check}' moved from {source_folder} to {destination_folder}")

    except Exception as e:
        printRedMsg(f"Failed to move files. Error: {e}")

def copy_files_in_folder(source_folder, destination_folder):
    try:
        # 遍历源文件夹中的所有文件
        for filename in os.listdir(source_folder):
            source_file_path = os.path.join(source_folder, filename)
            destination_file_path = os.path.join(destination_folder, filename)
            # 如果是文件则复制
            if os.path.isfile(source_file_path):
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied file: {source_file_path} to {destination_file_path}")
    except Exception as e:
        printRedMsg(f"Failed to copy files. Error: {e}")


def zip_folder(folder_path, zip_path):
    try:
        # 创建一个zip文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历文件夹中的所有文件和子文件夹
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 将文件添加到zip文件中
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

        printGreenMsg(f"Folder {folder_path} successfully zipped to {zip_path}")
    except Exception as e:
        printRedMsg(f"Failed to zip folder. Error: {e}")


def unzip_file(zip_path, extract_to):
    try:
        # 创建一个ZipFile对象
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 解压缩所有文件到指定目标文件夹
            zip_ref.extractall(extract_to)

        printGreenMsg(f"Successfully extracted {zip_path} to {extract_to}")
    except Exception as e:
        printRedMsg(f"Failed to unzip file. Error: {e}")


def create_folder(folder_path):
    try:
        # 创建文件夹
        os.mkdir(folder_path)
        print(f"Folder created at {folder_path}")
    except Exception as e:
        printRedMsg(f"Failed to create folder. Error: {e}")


def ifExist(path):
    # today = getToday()
    if os.path.exists(path):
        print(f"The file {path} exists.")
        return True
    else:
        notExist = "not exist"
        print(f"The file {path} does \033[33m{notExist}\033[0m.")
        return False


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


def ifContain(text, targetText):
    return targetText in text


def count_files_with_target_field(folder_path, target_field):
    try:
        # 初始化计数器
        count = 0
        # 遍历目标文件夹中的所有文件
        for filename in os.listdir(folder_path):
            # 如果目标字段在文件名中，则计数加一
            if target_field in filename:
                count += 1
        return count
    except Exception as e:
        printRedMsg(f"Failed to count files. Error: {e}")


def printName():
    logo1 = """
          _____                    _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\____\                /::\    \                /::\____\        
       /::::\    \              /::::\    \              /:::/    /               /::::\    \              /::::|   |        
      /::::::\    \            /::::::\    \            /:::/    /               /::::::\    \            /:::::|   |        
     /:::/\:::\    \          /:::/\:::\    \          /:::/    /               /:::/\:::\    \          /::::::|   |        
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \        /:::/|::|   |        
   /::::\   \:::\    \      /::::\   \:::\    \       |::|    |               /::::\   \:::\    \      /:::/ |::|   |        
  /::::::\   \:::\    \    /::::::\   \:::\    \      |::|    |     _____    /::::::\   \:::\    \    /:::/  |::|   | _____  
 /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \     |::|    |    /\    \  /:::/\:::\   \:::\    \  /:::/   |::|   |/\    \ 
/:::/  \:::\   \:::|    |/:::/  \:::\   \:::\____\    |::|    |   /::\____\/:::/__\:::\   \:::\____\/:: /    |::|   /::\____\\
\::/   |::::\  /:::|____|\::/    \:::\  /:::/    /    |::|    |  /:::/    /\:::\   \:::\   \::/    /\::/    /|::|  /:::/    /
 \/____|:::::\/:::/    /  \/____/ \:::\/:::/    /     |::|    | /:::/    /  \:::\   \:::\   \/____/  \/____/ |::| /:::/    / 
       |:::::::::/    /            \::::::/    /      |::|____|/:::/    /    \:::\   \:::\    \              |::|/:::/    /  
       |::|\::::/    /              \::::/    /       |:::::::::::/    /      \:::\   \:::\____\             |::::::/    /   
       |::| \::/____/               /:::/    /        \::::::::::/____/        \:::\   \::/    /             |:::::/    /    
       |::|  ~|                    /:::/    /          ~~~~~~~~~~               \:::\   \/____/              |::::/    /     
       |::|   |                   /:::/    /                                     \:::\    \                  /:::/    /      
       \::|   |                  /:::/    /                                       \:::\____\                /:::/    /       
        \:|   |                  \::/    /                                         \::/    /                \::/    /        
         \|___|                   \/____/                                           \/____/                  \/____/         
                                                                                                                             
    """

    logo2 = """
    __________                               
    \______   \_____  ___  __  ____    ____  
     |       _/\__  \ \  \/ /_/ __ \  /    \ 
     |    |   \ / __ \_\   / \  ___/ |   |  \\
     |____|_  /(____  / \_/   \___  >|___|  /
            \/      \/            \/      \/ 

    """
    print(logo2)


if HTTP_SERVER:
    ...
    # def fetchDataFromHttpServer(server_url):
    #     try:
    #         response = requests.get(server_url)
    #         if response.status_code == 200:
    #             printGreenMsg("Data fetched successfully:")
    #             # print(response.text)
    #             return response.text
    #         else:
    #             printRedMsg(f"Failed to fetch data. Status code: {response.status_code}")
    #     except Exception as e:
    #         printRedMsg(f"An error occurred: {e}")
    #
    #
    # def download_files_from_html(html_content, server_url, download_dir):
    #     try:
    #         soup = BeautifulSoup(html_content, 'html.parser')
    #         links = soup.find_all('a')
    #
    #         for link in links:
    #             href = link.get('href')
    #             # 如果链接是相对路径，拼接成绝对路径
    #             if not href.startswith('http'):
    #                 href = server_url + '/' + href
    #
    #             filename = href.split('/')[-1]
    #             file_path = os.path.join(download_dir, filename)
    #
    #             printBlueMsg(f"Downloading {filename}...")
    #             r = requests.get(href, stream=True)
    #             with open(file_path, 'wb') as f:
    #                 for chunk in r.iter_content(chunk_size=8192):
    #                     if chunk:
    #                         f.write(chunk)
    #             printGreenMsg(f"{filename} downloaded successfully.")
    #
    #     except Exception as e:
    #         printRedMsg(f"An error occurred: {e}")


def get_public_ip():
    try:
        ip_data = urllib.request.urlopen('https://api.ipify.org').read().decode('utf-8')
        return ip_data
    except Exception as e:
        return "Error occurred: {}".format(str(e))


def find_stock_data(file_path, stock_code):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 读取表头
        # print("表头:", end=" ")
        printGreenMsg("\n--------------------------------------------------")
        for item in header:
            print(item.ljust(15), end=" ")  # 对齐表头内容
        print()  # 换行

        isFound = False
        for row in reader:
            if any(stock_code in cell for cell in row):
                # print("找到匹配的行：", end=" ")
                for item in row:
                    print(item.ljust(15), end=" ")  # 对齐每一列的内容
                print()  # 换行
        printGreenMsg("\n--------------------------------------------------\n")
        input("press any key to return FIND DATA mode")
        isFound = True

        if not isFound:
            printRedMsg("未找到匹配的股票代码")
            input("press any key to continue...")


# 这个函数接受文件名和产品号与资金账号的字典作为参数。它首先在文件名中查找包含的关键字，然后根据找到的关键字获取对应的产品号。
# 最后，根据产品号在字典中查找对应的资金账号并输出。
def getInfoFromFileName(file_name, product_fund_dict_):
    keywords = ["CF15", "FL18", "HT02XY", "FL18SCA", "FL22SCB"]

    # 查找文件名中包含的关键字
    found_keyword = None
    for keyword in keywords:
        if keyword in file_name:
            found_keyword = keyword
            break

    if found_keyword is None:
        printRedMsg("未找到匹配的关键字")
        input("")
        return

    # 根据关键字获取对应的产品号
    product_number = None
    if found_keyword in product_fund_dict_:
        product_number = product_fund_dict_[found_keyword]

    if product_number is None:
        printRedMsg("未找到对应的产品号")
        input("")
        return

    print(f"\nYou are using \033[33m{found_keyword}\033[0m and the account number is \033[33m{product_number}\033[0m")

    # 根据产品号获取对应的资金账号
    # if product_number in product_fund_dict_:
    #     fund_account = product_fund_dict_[product_number]
    #     printGreenMsg(f"\nYou are using \033[33m{found_keyword}\033[0m and the account number is \033[33m{product_number}\033[0m\n")
    # else:
    #     printRedMsg("未找到对应的产品号")


def printAccountInfo():
    ...


def printAllAccountInfo():
    os.system("cls")
    isCorrect = enterPasswordToContinue()
    if not isCorrect:
        printRedMsg("Wrong password, contact with Admin")
        input("")
        return
    if isCorrect:
        printGreenMsg("password Correct.")
        input("")
    # 五个产品名
    product_names = ["CF15", "FL18", "HT02XY", "FL18SCA", "FL22SCB"]
    # 五个产品号
    product_numbers = ["480151137", "480149909", "480167623", "480160777", "3050003937"]
    # 五个密码
    passwords = ["297725", "230577", "890898", "123321", "123321"]
    printGreenMsg("\n--------------------------------------------------")

    print("产品名\t\t产品账号\t\t密码")
    for name, number, password in zip(product_names, product_numbers, passwords):
        print(f"{name}\t\t{number}\t\t{password}")
    printGreenMsg("\n--------------------------------------------------\n")

    input("press any key to quit")


def enterPasswordToContinue():
    cp = "147258"
    while True:
        p = input("Enter the password to unlock\n")
        if p == cp:
            return True
        else:
            return False


def list_files_with_numbers(path, n):
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(os.path.join(path, f))]  # 过滤出文件
    files.sort()  # 排序文件列表

    for i, file in enumerate(files[:n]):
        print(f"{i + 1}: {file}")

    choice = int(input("请选择文件序号（输入数字 1 到 n）: "))
    if choice < 1 or choice > n:
        print("无效的选择")
        return None

    selected_file = os.path.join(path, files[choice - 1])
    return selected_file


def list_files_with_numbers(path, n):
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(os.path.join(path, f))]  # 过滤出文件
    files.sort()  # 排序文件列表

    for i, file in enumerate(files[:n]):
        print(f"{i + 1}: {file}")

    choice = int(input(f"请选择文件序号（输入数字 1 到 {n}）: "))
    if choice < 1 or choice > n:
        printRedMsg("无效的选择")
        return None

    selected_file = os.path.join(path, files[choice - 1])
    return selected_file


def quickLookUpSellBuyList(product_choice):
    product_names = ["CF15", "FL18", "HT02XY", "FL18SC", "FL18SCA", "FL22SCB"]
    productName = product_names[product_choice - 1]
    rootPath = r"C:\Users\Administrator\Desktop\兴业证券多账户交易"
    BSLpath = rf"{rootPath}\{productName}\Sell_Buy_List_{productName}"

    fullPath = list_files_with_numbers(BSLpath, 15)
    # print(fullPath)
    # TODO 还没写完


# def remove_lines_with_character(file_path, target_character):
#     printGreenMsg("正在处理中...")
#     # 打开文件并逐行读取内容
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#
#     # 过滤掉包含特定字符的行
#     filtered_lines = [line for line in lines if target_character not in line]
#
#     # 将剩余的行重新写入文件
#     with open(file_path, 'w') as file:
#         file.writelines(filtered_lines)
#
#     printGreenMsg("处理完成")
#     input("")


# 如果文件可能很大，我们可以采用逐行读取和写入的方式来处理文件，以避免一次性加载整个文件到内存中
def remove_lines_with_character(file_path, target_character):
    try:
        print(f"正在处理 {target_character} 中...", end=" ")
        # 将目标字符转换为字节对象
        target_byte = target_character.encode()
        temp_file_path = file_path + '.tmp'  # 创建临时文件路径
        # 逐行读取原文件，并过滤掉包含特定字符的行，写入临时文件
        with open(file_path, 'rb') as input_file, open(temp_file_path, 'wb') as output_file:
            for line in input_file:
                if target_byte not in line:
                    output_file.write(line)
        # printGreenMsg("正在逐行读取原文件，并过滤掉包含特定字符的行，写入临时文件中...")
        # 替换原文件

        os.remove(file_path)
        # printGreenMsg("正在替换原文件中...")
        os.rename(temp_file_path, file_path)

        printGreenMsg("处理完成")

    except Exception as e:
        # 如果发生异常，打印错误消息
        printRedMsg(f"处理文件时出现错误：{e}")
        input("")


def rename_all_py_files_and_return_paths(folder_path, new_fund_name):
    file_paths = []

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):  # 确保只处理.py文件
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

                # 读取文件内容
                with open(file_path, "r") as f:
                    content = f.read()

                # 使用正则表达式替换文件中的字符串
                new_content = re.sub(r'fund_name=\w+', 'fund_name=' + new_fund_name, content)

                # 将替换后的内容写回文件
                with open(file_path, "w") as f:
                    f.write(new_content)

                # 生成新的文件名（可选）
                new_file_name = file.replace("old_fund_name", new_fund_name)
                new_file_path = os.path.join(root, new_file_name)

                # 重命名文件
                os.rename(file_path, new_file_path)

    return file_paths


def rename_py_files(directory_path, new_extension=".new"):
    """
    :brief 传入一个路径，遍历这个路径下所有py文件，对每个文件进行重命名操作
    Function to rename all .py files in a given directory.
    :param directory_path: Path to the directory containing .py files.
    :param new_extension: New extension for renamed files (default: ".new").
    """
    today = getToday()
    files = os.listdir(directory_path)
    for filename in files:
        if filename.endswith(".py"):
            old_path = os.path.join(directory_path, filename)
            productName = find_fund_name(old_path)
            if productName:
                new_filename = f"{productName}_{today}{new_extension}"
                new_path = os.path.join(directory_path, new_filename)
                os.rename(old_path, new_path)


def find_fund_name(filepath):
    """
    传入一个文件路径，找到文件里含有fund_name=的一行，返回等号后面的字符串
    Function to find and return the string after "fund_name=" in a specified file.
    :param filepath: Path to the file.
    :return: String after "fund_name=" if found, otherwise None.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'fund_name=(.*)', line)
            if match:
                return match.group(1).strip()


# Example usage:
# 1. Rename all .py files in the directory "my_directory" with extension ".new"
# rename_py_files("my_directory", ".new")

# 2. Find and return the string after "fund_name=" in the file "example_file.txt"
# fund_name_value = find_fund_name("example_file.txt")
# print(fund_name_value)


# 总是删掉错误的行！！！
def remove_lines_time_in_range_for_order_log(file_path):
    printYellowMsg("in func remove_lines_time_in_range_for_order_log")
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 用于匹配时间格式的正则表达式
        import re
        time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')

        # 初始化开始索引和结束索引
        start_index = None
        end_index = None

        # 逐行遍历文件内容
        for i, line in enumerate(lines):
            # 判断是否为时间行且不包含其他字符
            if time_pattern.match(line.strip()) and len(line.strip()) == 8:
                if start_index is None:
                    start_index = i
                else:
                    # 发现一个新的时间行，删除上一个时间段的内容
                    if end_index is not None:
                        del lines[start_index + 1:end_index]
                    start_index = i
                end_index = None
            elif start_index is not None:
                # 找到非时间行，更新结束索引
                end_index = i

        # 如果文件末尾存在时间段，则删除最后一个时间段的内容
        if end_index is not None:
            del lines[start_index + 1:end_index]

        # 将处理后的内容写回文件
        with open(file_path, 'w', encoding='uft-8') as file:
            file.writelines(lines)
    except Exception as e:
        # 如果发生异常，打印错误消息
        printRedMsg(f"删除order文件的一系列时间行错误：{e}")
        input("")


def modifyNamePAtoPAHF(path):
    try:
        # 遍历指定目录中的所有 CSV 文件
        for filename in os.listdir(path):
            if filename.endswith(".csv") and "PA" in filename:
                # 构造旧文件路径
                old_file = os.path.join(path, filename)

                # 替换文件名中的 "PA" 为 "PAHF"
                new_filename = filename.replace("PA", "PAHF")

                # 构造新文件路径
                new_file = os.path.join(path, new_filename)

                # 重命名文件
                os.rename(old_file, new_file)
                print(f"Renamed: {old_file} to {new_file}")

        printGreenMsg("Files renamed successfully.")

    except Exception as e:
        printRedMsg(f"Failed to rename files. Error: {e}")


def run_python_file(path):
    os.system(fr"D:\software\python3.6.6\python.exe {path}")


# 如果表头中有重复的字段名称，PrettyTable 会抛出 Field names must be unique 错误。
# 为了解决这个问题，可以在读取表头时检查并处理重复字段名称。例如，可以在字段名称后面添加编号使其唯一。
# 以下是一个改进后的示例
def make_unique(field_names):
    """
    确保字段名称唯一。
    """
    seen = {}
    unique_field_names = []
    for name in field_names:
        if name in seen:
            seen[name] += 1
            unique_field_names.append(f"{name}_{seen[name]}")
        else:
            seen[name] = 0
            unique_field_names.append(name)
    return unique_field_names

def replace_none_with_empty_string(row):
    """
    将行中的 None 替换为空字符串。
    """
    return ['' if cell is None else cell for cell in row]


def read_and_print_xlsx(file_path):
    """
    读取并打印 .xlsx 文件的内容

    参数:
    file_path (str): .xlsx 文件的路径
    """
    printYellowMsg(f"now printing excel: {file_path}")
    try:
        # 尝试加载工作簿
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # 创建 PrettyTable 对象
        table = PrettyTable()

        # 获取表头
        headers = [cell.value for cell in sheet[1]]
        unique_headers = make_unique(headers)
        table.field_names = replace_none_with_empty_string(unique_headers)

        # 添加表格行
        for row in sheet.iter_rows(min_row=2, values_only=True):
            table.add_row(replace_none_with_empty_string(row))

        # 打印表格内容
        print(table)
    except FileNotFoundError:
        printRedMsg(f"File not found: {file_path}. Please check the file path.")
    except Exception as e:
        printRedMsg(f"An error occurred while reading the file: {e}")



def iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii():
    ...


# ====================================================================================================================
# ============================================   主要函数   ===========================================================
# ====================================================================================================================

def before0920processFL22SC():
    oriFl22 = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SC\Sell_Buy_List_FL22SC"
    os.system("cls")
    today = getToday()

    oriBuy = rf"{oriFl22}\{buy}FL22SC_{today}.csv"
    oriSell = rf"{oriFl22}\{sell}FL22SC_{today}.csv"
    oriJrcc = rf"{oriFl22}\{jrcc}FL22SC_{today}.csv"

    # 20240524 百度网盘同步空间移动到了 37，分单程序都自动运行了
    while False:
        # 检查原始信号在不在，不在直接退
        print("checking if the original signals are exist...")
        if ((ifExist(oriBuy) and ifExist(oriSell) and ifExist(oriJrcc)) == False):
            printRedMsg("There are no original signal!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("original signal EXIST")
            input("press any key to continue...")

        # 然后移动到目标文件夹
        printYellowMsg("\nMoving original signals to the divide_order_account path...")
        divideFl22 = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SC\Sell_Buy_List_FL22SC"
        # TODO testing
        copy_file(oriBuy, divideFl22)
        copy_file(oriSell, divideFl22)
        copy_file(oriJrcc, divideFl22)
        printYellowMsg("Move done, now checking if moving is complete...")
        if not (ifExist(rf"{divideFl22}\{buy}FL22SC_{today}.csv") and ifExist(
                rf"{divideFl22}\{sell}FL22SC_{today}.csv") and ifExist(rf"{divideFl22}\{jrcc}FL22SC_{today}.csv")):
            printRedMsg("Moving is not complete!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("Moving is complete, press any key to run the 1、盘前订单拆分.py...")
            input(" ")

        # 运行分单脚本
        # FIXME 这个功能不能正常运行 用多线程
        # os.system(r"C:\PROGRA~1\Python36\python.exe" r"C:\Users\Administrator\Desktop\divide_order_account\projects\1、盘前订单拆分.py")
        # input("1、盘前订单拆分.py is ending, press any key to continue...")
        printYellowMsg("Plz run the 1、盘前订单拆分.py by hand, press any key to continue after finishing running...")
        input(" ")

    # 检测拆分是否成功

    # divide 文件夹下的三个文件
    # A
    divideSCAbuy = rf"{divide_SCA}\{buy}FL22SCA_{today}.csv"
    divideSCAsell = rf"{divide_SCA}\{sell}FL22SCA_{today}.csv"
    divideSCAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA_{today}.csv"
    # B
    divideSCBbuy = rf"{divide_SCB}\{buy}FL22SCB_{today}.csv"
    divideSCBsell = rf"{divide_SCB}\{sell}FL22SCB_{today}.csv"
    divideSCBjrcc = rf"{divide_SCB}\{jrcc}FL22SCB_{today}.csv"
    isDivideSCAExist = ifExist(divideSCAbuy) and ifExist(divideSCAsell) and ifExist(divideSCAjrcc)
    isDivideSCBExist = ifExist(divideSCBbuy) and ifExist(divideSCBsell) and ifExist(divideSCBjrcc)
    isDivideSCABExist = isDivideSCAExist and isDivideSCBExist

    if not (isDivideSCABExist):
        printRedMsg("signal dividing fail!!!\nreturning...")
        input("")
        return
    else:
        printGreenMsg("signal dividing is DONE.")
        input(" ")

    printYellowMsg("Copying files, 6 in total...")
    # 传回文件
    # TODO 这里直接
    # TODO testing
    # SCA
    copy_file(divideSCAbuy, ori_SCA)
    copy_file(divideSCAsell, ori_SCA)
    copy_file(divideSCAjrcc, ori_SCA)
    # SCB
    copy_file(divideSCBbuy, ori_SCB)
    copy_file(divideSCBsell, ori_SCB)
    copy_file(divideSCBjrcc, ori_SCB)
    printYellowMsg("Copying finished, examine required...")

    # 检查文件是否复制成功
    # 原始信号文件夹的三个文件
    # A
    oriSCAbuy = rf"{ori_SCA}\{buy}FL22SCA_{today}.csv"
    oriSCAsell = rf"{ori_SCA}\{sell}FL22SCA_{today}.csv"
    oriSCAjrcc = rf"{ori_SCA}\{jrcc}FL22SCA_{today}.csv"
    # B
    oriSCBbuy = rf"{ori_SCB}\{buy}FL22SCB_{today}.csv"
    oriSCBsell = rf"{ori_SCB}\{sell}FL22SCB_{today}.csv"
    oriSCBjrcc = rf"{ori_SCB}\{jrcc}FL22SCB_{today}.csv"
    isOriSCAExist = ifExist(oriSCAbuy) and ifExist(oriSCAsell) and ifExist(oriSCAjrcc)
    isOriSCBExist = ifExist(oriSCBbuy) and ifExist(oriSCBsell) and ifExist(oriSCBjrcc)
    isOriSCABExist = isOriSCAExist and isOriSCBExist

    if not (isOriSCABExist):
        printRedMsg("divided signals copy fail!!!\nreturning...")
        input("")
        return
    else:
        printGreenMsg("divided signals copy DONE.")
        input(" ")

    printGreenMsg("function before0920processFL22SC is ending, press any key to continue...")
    input("")


def realTimeSignalMoveForFL22SC():
    os.system("cls")
    # 先定义一下, 实时信号是直接传到 ori 文件夹的
    today = getToday()
    nom = rf"{ori_SC}\{nom_}{today}.txt"
    nom2 = rf"{ori_SC}\{nom2_}{today}.txt"
    noa = rf"{ori_SC}\{noa_}{today}.txt"
    noa2 = rf"{ori_SC}\{noa2_}{today}.txt"

    # FIXME 才意识到可以，选择数字之后，比如说2，就直接 nowTimeNode = m2 就可以很方便了。。。
    # FIXME 没有意识到一个信号拆分后可能是A有信号B是no信号！！ 20240430 出现了这个问题，直接爆红，只能手动复制
    # FIXMED 只要早上有一次 No morning, 那接着的每一次都将要复制一次
    # 选择实时信号
    while True:
        printYellowMsg("\n请确认实时信号节点？(1/2/3/4):\n1：morning; 2：morning2Two; 3：afternoon; 4：afternoon2Two\n")
        global g_realTimeNode
        g_realTimeNode = input("")
        if g_realTimeNode == "1":
            rtsBuy = ""
            rtsSell = rf"{ori_SC}\{sell}FL22SC{m}_{today}.csv"
            rtsJRCC = rf"{ori_SC}\{jrcc}FL22SC{m}_{today}.csv"
            rtsNoSignal = nom
            divideAsell = rf"{divide_SCA}\{sell}FL22SCA{m}_{today}.csv"
            divideAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA{m}_{today}.csv"
            divideBsell = rf"{divide_SCB}\{sell}FL22SCB{m}_{today}.csv"
            divideBjrcc = rf"{divide_SCB}\{jrcc}FL22SCB{m}_{today}.csv"
            divideAno = rf"{divide_SCA}\{nom_}{today}.txt"
            divideBno = rf"{divide_SCB}\{nom_}{today}.txt"

            oriAbuy = rf" "
            oriAsell = rf"{ori_SCA}\{sell}FL22SCA{m}_{today}.csv"
            oriAjrcc = rf"{ori_SCA}\{jrcc}FL22SCA{m}_{today}.csv"
            oriAno = rf"{ori_SCA}\{nom_}{today}.txt"

            oriBsell = rf"{ori_SCB}\{sell}FL22SCB{m}_{today}.csv"
            oriBjrcc = rf"{ori_SCB}\{jrcc}FL22SCB{m}_{today}.csv"
            oriBno = rf"{ori_SCB}\{nom_}{today}.txt"

            break
        elif g_realTimeNode == "2":
            rtsBuy = ""
            rtsSell = rf"{ori_SC}\{sell}FL22SC{m2}_{today}.csv"
            rtsJRCC = rf"{ori_SC}\{jrcc}FL22SC{m2}_{today}.csv"
            rtsNoSignal = nom2
            divideAsell = rf"{divide_SCA}\{sell}FL22SCA{m2}_{today}.csv"
            divideAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA{m2}_{today}.csv"
            divideBsell = rf"{divide_SCB}\{sell}FL22SCB{m2}_{today}.csv"
            divideBjrcc = rf"{divide_SCB}\{jrcc}FL22SCB{m2}_{today}.csv"
            divideAno = rf"{divide_SCA}\{nom2_}{today}.txt"
            divideBno = rf"{divide_SCB}\{nom2_}{today}.txt"

            oriAbuy = rf" "
            oriAsell = rf"{ori_SCA}\{sell}FL22SCA{m2}_{today}.csv"
            oriAjrcc = rf"{ori_SCA}\{jrcc}FL22SCA{m2}_{today}.csv"
            oriAno = rf"{ori_SCA}\{nom2_}{today}.txt"

            oriBsell = rf"{ori_SCB}\{sell}FL22SCB{m2}_{today}.csv"
            oriBjrcc = rf"{ori_SCB}\{jrcc}FL22SCB{m2}_{today}.csv"
            oriBno = rf"{ori_SCB}\{nom2_}{today}.txt"
            break
        elif g_realTimeNode == "3":
            rtsBuy = ""
            rtsSell = rf"{ori_SC}\{sell}FL22SC{a}_{today}.csv"
            rtsJRCC = rf"{ori_SC}\{jrcc}FL22SC{a}_{today}.csv"
            rtsNoSignal = noa
            divideAsell = rf"{divide_SCA}\{sell}FL22SCA{a}_{today}.csv"
            divideAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA{a}_{today}.csv"
            divideBsell = rf"{divide_SCB}\{sell}FL22SCB{a}_{today}.csv"
            divideBjrcc = rf"{divide_SCB}\{jrcc}FL22SCB{a}_{today}.csv"
            divideAno = rf"{divide_SCA}\{noa_}{today}.txt"
            divideBno = rf"{divide_SCB}\{noa_}{today}.txt"

            oriAbuy = rf" "
            oriAsell = rf"{ori_SCA}\{sell}FL22SCA{a}_{today}.csv"
            oriAjrcc = rf"{ori_SCA}\{jrcc}FL22SCA{a}_{today}.csv"
            oriAno = rf"{ori_SCA}\{noa_}{today}.txt"

            oriBsell = rf"{ori_SCB}\{sell}FL22SCB{a}_{today}.csv"
            oriBjrcc = rf"{ori_SCB}\{jrcc}FL22SCB{a}_{today}.csv"
            oriBno = rf"{ori_SCB}\{noa_}{today}.txt"

            break
        elif g_realTimeNode == "4":
            rtsSell = ""
            rtsBuy = rf"{ori_SC}\{buy}FL22SC{a2}_{today}.csv"
            rtsJRCC = rf"{ori_SC}\{jrcc}FL22SC{a2}_{today}.csv"
            rtsNoSignal = noa2
            divideAbuy = rf"{divide_SCA}\{buy}FL22SCA{a2}_{today}.csv"
            divideAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA{a2}_{today}.csv"
            divideBbuy = rf"{divide_SCB}\{buy}FL22SCB{a2}_{today}.csv"
            divideBjrcc = rf"{divide_SCB}\{jrcc}FL22SCB{a2}_{today}.csv"
            divideAno = rf"{divide_SCA}\{noa2_}{today}.txt"
            divideBno = rf"{divide_SCB}\{noa2_}{today}.txt"

            oriAbuy = rf"{ori_SCA}\{buy}FL22SCA{a2}_{today}.csv"
            oriAsell = rf" "
            oriAjrcc = rf"{ori_SCA}\{jrcc}FL22SCA{a2}_{today}.csv"
            oriAno = rf"{ori_SCA}\{noa2_}{today}.txt"

            oriBbuy = rf"{ori_SCB}\{buy}FL22SCB{a2}_{today}.csv"
            oriBjrcc = rf"{ori_SCB}\{jrcc}FL22SCB{a2}_{today}.csv"
            oriBno = rf"{ori_SCB}\{noa2_}{today}.txt"
            break
        elif g_realTimeNode == "quit":
            printBlueMsg("returning to main menu...\n")
            input("")
            return
        else:
            printRedMsg("无效的选项，请重新输入！")

    # 检查实时信号到了没有
    printYellowMsg("checking whether the real time signals are arrive...")
    isNoSignal = ifExist(rtsNoSignal)
    isRealTimeSignal = ((ifExist(rtsSell) or ifExist(rtsBuy)) and ifExist(rtsJRCC))
    isRealTimeSignalExist = isNoSignal or isRealTimeSignal
    if not isRealTimeSignalExist:
        printRedMsg("real time signals are NOT arrive!!!\nreturning...")
        input("")
        return
    else:
        printGreenMsg("real time signals ARE arrive.")
        input(" ")

    # # 复制文件进入 divide 文件
    # if isNoSignal:
    #     # 如果是no信号
    #     copy_file(rtsNoSignal, ori_SC)
    # elif isRealTimeSignal:
    #     if choice == "4":
    #         copy_file(rtsBuy, ori_SC)
    #         copy_file(rtsJRCC, ori_SC)
    #     copy_file(rtsSell, ori_SC)
    #     copy_file(rtsJRCC, ori_SC)

    # TODO 等待 30s 让程序拆分文件
    # TODO 检测信号是否复制成功

    # 检测信号是否拆分成功
    if g_realTimeNode == "4":
        isNoDivide = ifExist(divideAno) and ifExist(divideBno)
        isSignalDivide = ifExist(divideAbuy) and ifExist(divideAjrcc) and ifExist(divideBbuy) and ifExist(divideBjrcc)
        isDivide = (isNoDivide) or (isSignalDivide)
        if not isDivide:
            printRedMsg("afternoon2Two signal is not divided!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("signal is divided.")
            input(" ")

    else:
        # choice == 1 2 3
        isNoDivide = ifExist(divideAno) and ifExist(divideBno)
        isSignalDivide = ifExist(divideAsell) and ifExist(divideAjrcc) and ifExist(divideBsell) and ifExist(divideBjrcc)
        isDivide = (isNoDivide) or (isSignalDivide)
        if not isDivide:
            printRedMsg("signal is not divided!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("signal is divided.")
            input(" ")

    # 把拆分好的信号复制回来
    if g_realTimeNode == "4":
        copy_file(divideAno, ori_SCA)
        copy_file(divideAbuy, ori_SCA)
        copy_file(divideAjrcc, ori_SCA)
        copy_file(divideBbuy, ori_SCB)
        copy_file(divideBjrcc, ori_SCB)
        copy_file(divideBno, ori_SCB)
    else:
        copy_file(divideAsell, ori_SCA)
        copy_file(divideAno, ori_SCA)
        copy_file(divideAjrcc, ori_SCA)
        copy_file(divideBsell, ori_SCB)
        copy_file(divideBjrcc, ori_SCB)
        copy_file(divideBno, ori_SCB)

    # 验证复制回来的信号
    # A
    if g_realTimeNode == "4":
        isNoOri = ifExist(oriAno) and ifExist(oriBno)
        isSignalOri = ifExist(oriAbuy) and ifExist(oriAjrcc) and ifExist(oriBbuy) and ifExist(oriBjrcc)
        isOri = (isNoOri) or (isSignalOri)
        if not isOri:
            printRedMsg("divided afternoon2Two signal is not copy well!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("signal is copied")
            input(" ")

    else:
        # choice == 1 2 3
        isNoOri = ifExist(oriAno) and ifExist(oriBno)
        isSignalOri = ifExist(oriAsell) and ifExist(oriAjrcc) and ifExist(oriBsell) and ifExist(oriBjrcc)
        isOri = (isNoOri) or (isSignalOri)
        if not isOri:
            printRedMsg(f"divided signal is not copy well!!!\nreturning...")
            input("")
            return
        else:
            printGreenMsg("signal is copied")
            input(" ")

        # 完成
        printGreenMsg("Action done, returning to main menu...")
        input(" ")



def realTimeSignalMoveForHT02():
    # 包含原始信号和实时信号
    os.system("cls")
    input("Now processing HT02XY")
    today = getToday()
    divide_HT = r"C:\Users\Administrator\Desktop\divide_order_account\HT02XY\Sell_Buy_List_HT02XY"
    ori_HT = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\HT02XY\Sell_Buy_List_HT02XY"

    nom =  rf"{divide_HT}\{nom_}{today}.txt"
    nom2 = rf"{divide_HT}\{nom2_}{today}.txt"
    noa =  rf"{divide_HT}\{noa_}{today}.txt"
    noa2 = rf"{divide_HT}\{noa2_}{today}.txt"
    # HT02XYsell,HT02XYjrcc,HT02XYbuy,HT02XYno = None
    # 原始信号
    originalSignalBuy = rf"{divide_HT}\{buy}HT02XY_{today}.csv"
    originalSignalSell = rf"{divide_HT}\{sell}HT02XY_{today}.csv"
    originalSignalJrcc = rf"{divide_HT}\{jrcc}HT02XY_{today}.csv"

    print(g_realTimeNode)
    input("")

    while True:
        # printYellowMsg("\n请确认实时信号节点？(1/2/3/4):\n1：morning; 2：morning2Two; 3：afternoon; 4：afternoon2Two\n")
        # g_realTimeNode = input("")
        if g_realTimeNode == "1":
            HT02XYsell = rf"{divide_HT}\{sell}HT02XY{m}_{today}.csv"
            HT02XYjrcc = rf"{divide_HT}\{jrcc}HT02XY{m}_{today}.csv"
            HT02XYbuy = ""
            HT02XYno = nom
            break
        elif g_realTimeNode == "2":
            HT02XYsell = rf"{divide_HT}\{sell}HT02XY{m2}_{today}.csv"
            HT02XYjrcc = rf"{divide_HT}\{jrcc}HT02XY{m2}_{today}.csv"
            HT02XYbuy = ""
            HT02XYno = nom2
            break
        elif g_realTimeNode == "3":
            HT02XYsell = rf"{divide_HT}\{sell}HT02XY{a}_{today}.csv"
            HT02XYjrcc = rf"{divide_HT}\{jrcc}HT02XY{a}_{today}.csv"
            HT02XYbuy = ""
            HT02XYno = noa
            break
        elif g_realTimeNode == "4":
            HT02XYjrcc = rf"{divide_HT}\{jrcc}HT02XY{a2}_{today}.csv"
            HT02XYsell = ""
            HT02XYbuy = rf"{divide_HT}\{buy}HT02XY{a2}_{today}.csv"
            HT02XYno = noa2
            break
        elif g_realTimeNode == "quit":
            printBlueMsg("returning to main menu...\n")
            input("")
            return
        else:
            printRedMsg("无效的选项，请重新输入！")

    # 检查 HT02XY 拆分了没有
    printYellowMsg("checking whether the real time signals are arrive...")
    isNoSignal = ifExist(HT02XYno)
    isRealTimeSignal = ((ifExist(HT02XYsell) or ifExist(HT02XYbuy)) and ifExist(HT02XYjrcc))
    isHT02XYsignalExist = isNoSignal or isRealTimeSignal
    if not isHT02XYsignalExist:
        printRedMsg("HT02XY signal is not exist!\nreturning...")
        input("")
        return
    else:
        printGreenMsg("HT02XY signals ARE arrive.")
        input("")

    # 复制到扫单文件夹
    if g_realTimeNode == "4":
        copy_file(HT02XYbuy, ori_HT)
        copy_file(HT02XYjrcc, ori_HT)
        copy_file(HT02XYno, ori_HT)
    else:
        copy_file(HT02XYsell, ori_HT)
        copy_file(HT02XYjrcc, ori_HT)
        copy_file(HT02XYno, ori_HT)

    # 验证复制回来的信号
    printYellowMsg("省略验证，请自行检查\n")
    printGreenMsg("Action done, returning to main menu...")
    input(" ")


def dataCollectorOn40():
    today = getToday()
    global g_yesterday
    if g_yesterday == None:
        g_yesterday = input("请输入上一个交易日的日期")
    printYellowMsg("PLZ CHECK THIS FUNCTION IS ONLY WORKING ON 40")
    printYellowMsg("Deleting data in folder toLZY")
    destinationPath = r"C:\Users\progene014\Desktop\toLZY\data"

    # os.chmod(destinationPath, 0o777)
    if erase_folder_contents(destinationPath):
        printGreenMsg("Data has been deleted.")
        input("")
    else:
        printRedMsg("Data has NOT been deleted, returning to main menu...")
        input(" ")
        return

    # limit_price_file
    limitPricePath = r"D:\limit_price_projects\limit_price_file"
    copy_latest_files(limitPricePath, destinationPath, 1)

    # data
    oriDataSCA = r"D:\hutao\projects\数据分析\FL22SC\data_FL22SCA"
    oriDataSCB = r"D:\hutao\projects\数据分析\FL22SC\data_FL22SCB"
    desDataSCA = r"C:\Users\progene014\Desktop\toLZY\data\A_data"
    desDataSCB = r"C:\Users\progene014\Desktop\toLZY\data\B_data"
    copy_latest_files(oriDataSCA, desDataSCA, 3)
    copy_latest_files(oriDataSCB, desDataSCB, 3)

    # fl22sc 的 format data
    oriDataSC_format = r"D:\hutao\projects\数据分析\FL22SC\format_data"
    desDataA_format = r"C:\Users\progene014\Desktop\toLZY\data\A_format_data"
    desDataB_format = r"C:\Users\progene014\Desktop\toLZY\data\B_format_data"
    copy_files_with_string_limited(oriDataSC_format, desDataA_format, "SCA", 3)
    copy_files_with_string_limited(oriDataSC_format, desDataB_format, "SCB", 3)

    # ht02zs 的 format data
    oriDataHT02_format = r"D:\hutao\projects\数据分析\HT02\format_data"
    desDataHT02ZS_format = r"C:\Users\progene014\Desktop\toLZY\data\HT02ZS_format_data"
    desDataHT02XY_format = r"C:\Users\progene014\Desktop\toLZY\data\HT02XY_format_data"
    copy_files_with_string_limited(oriDataHT02_format, desDataHT02ZS_format, "HT02ZS", 3)
    copy_files_with_string_limited(oriDataHT02_format, desDataHT02XY_format, "HT02XY", 3)

    printYellowMsg("check if files are lastest, making ZIP file now")
    # NQ 修改这个参数以把 zip 文件放到你想要的位置
    whereToZip = rf"C:\Users\progene014\Desktop\toLZY\data{g_yesterday}.zip"
    zip_folder(destinationPath, whereToZip)
    ifExist(whereToZip)
    printGreenMsg("function ending, returning to main menu...")
    input(" ")


# 收盘拆分的导出数据的检查
def checkExportData():
    ...
    today = getToday()
    # 检查有没有导出数据
    printYellowMsg("now checking if smt_data exist...")
    input("")
    smtData = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\smt_data"
    asset = rf"{smtData}\asset_{today}.csv"
    trans = rf"{smtData}\transaction_{today}.csv"
    order = rf"{smtData}\order_{today}.csv"
    holdin = rf"{smtData}\holding_{today}.csv"
    smtDataExist = ifExist(asset) and ifExist(trans) and ifExist(order) and ifExist(holdin)
    if not smtDataExist:
        printRedMsg("smtData is NOT exist, returning to main menu...")
        input("")
        return
    else:
        printGreenMsg("smtData is exist.")
        input("")

    printYellowMsg(f"NOW RUNNING {smart_divide_path}...")


    thread = threading.Thread(target=run_python_file, args=(smart_divide_path,))
    thread.start()
    # 等待线程结束
    thread.join()
    printGreenMsg("Data divide program is finished.")


    input("")

    # 检查是否拆分完毕
    cf15 = count_files_with_target_field(r"C:\Users\Administrator\Desktop\兴业证券多账户交易\CF15\data", today)
    fl18 = count_files_with_target_field(r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL18\data", today)
    ht02zs = count_files_with_target_field(r"C:\Users\Administrator\Desktop\兴业证券多账户交易\HT02XY\data", today)
    fl22sc = count_files_with_target_field(r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\data", today)
    fl22xz = count_files_with_target_field(r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\data", today)
    print(cf15, fl18, ht02zs, fl22sc, fl22xz)

    # 完成
    printGreenMsg("process done, returning to main menu")
    input("")


def downloadDataFromServer40():
    ...
    # TODO 未完成，又找不到本地文件夹的错误，而且会下载分享的所有文件。
    # download_dir = r"C:\Users\progene12\Desktop\Start Trading\FL22SC数据分析"
    # html_content = fetchDataFromHttpServer(server40addr)
    # if html_content:
    #     if not os.path.exists(download_dir):
    #         os.makedirs(download_dir)
    #
    #     # 下载文件
    #     download_files_from_html(html_content, server40addr, download_dir)


# TODO 转移到37上之后需要改一切! 疯狂！
def copYesterdayData():
    printYellowMsg("接下来将依次进行：\n\tFL22SC -> format_data\n\tFL22SC -> data\n\tHT02 -> format_data")
    # 解压zip文件夹
    startTradePath = r"C:\Users\Administrator\Desktop\startTrade"
    temp = rf"{startTradePath}\data\temp"
    today = getToday()
    global g_yesterday
    if g_yesterday == None:
        g_yesterday = input("enter yesterday's date")
    zipPath = rf"{startTradePath}\data{g_yesterday}.zip"
    if not ifExist(zipPath):
        printRedMsg(f"data{g_yesterday}.zip is NOT here, do you want to enter a valid date? y/n")
        wantTo = input("")
        if wantTo == "y" or "Y":
            manualDate = input("Enter the date that is last trade day or the date you want for the zip file.")

        elif wantTo == "n":
            printRedMsg(f"data{g_yesterday}.zip is NOT here, returning to main menu...")
            return

    input("")
    # create_folder(temp)
    unzip_file(zipPath, temp)

    printBlueMsg("FL22SCA -> format_data")
    # ! 移动 FL22SC 文件到 divide 文件夹
    # test = rf"{temp}\test"
    des_A_data = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\data"
    des_A_FormatData = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\format_data"
    des_B_data = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\data"
    des_B_FormatData = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\format_data"
    des_limit_price = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\limit_price"
    copy_files_in_folder(rf"{temp}\A_data", des_A_data)
    copy_files_in_folder(rf"{temp}\A_format_data", des_A_FormatData)
    copy_files_in_folder(rf"{temp}\B_data", des_B_data)
    copy_files_in_folder(rf"{temp}\B_format_data", des_B_FormatData)
    copy_file(rf"{temp}\{today}_limit_price.csv", des_limit_price)

    # TODoo yesterday 不是上一个交易日就没法运行了啊啊啊

    # 检验文件是否传输
    #FIXME 220240527 先注释，判断昨日有问题，下面也是

    # if count_files_with_target_field(des_A_data, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_A_data}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des_A_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_A_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des_B_data, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_B_data}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des_B_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_B_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return

    if not ifExist(des_limit_price):
        printRedMsg("limit price file is NOT copied")
    else:
        ...

    printBlueMsg("FL22SCB -> format_data")
    # 移动文件夹到 兴业扫单文件夹 C:\Users\Administrator\Desktop\兴业证券多账户交易
    des2_A_data = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\data"
    des2_A_FormatData = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\format_data"
    des2_B_data = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\data"
    des2_B_FormatData = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\format_data"
    copy_files_in_folder(rf"{temp}\A_data", des2_A_data)
    copy_files_in_folder(rf"{temp}\A_format_data", des2_A_FormatData)
    copy_files_in_folder(rf"{temp}\B_data", des2_B_data)
    copy_files_in_folder(rf"{temp}\B_format_data", des2_B_FormatData)

    # 检验文件是否传输
    # if count_files_with_target_field(des2_A_data, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des2_A_data}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des2_A_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des2_A_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des2_B_data, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des2_B_data}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des2_B_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des2_B_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return

    printBlueMsg("HT02XY -> format_data\nHT02ZS -> format_data")
    # 移动 ht02 的 format_data 到兴业扫单文件夹 C:\Users\Administrator\Desktop\divide
    des_ht02xy_FormatData = r"C:\Users\Administrator\Desktop\divide_order_account\HT02XY\format_data"
    des_ht02zs_FormatData = r"C:\Users\Administrator\Desktop\divide_order_account\HT02ZS\format_data"
    copy_files_in_folder(rf"{temp}\HT02XY_format_data", des_ht02xy_FormatData)
    copy_files_in_folder(rf"{temp}\HT02ZS_format_data", des_ht02zs_FormatData)

    # 检验文件是否传输
    # if count_files_with_target_field(des_ht02xy_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_ht02xy_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return
    #
    # if count_files_with_target_field(des_ht02zs_FormatData, g_yesterday) == 3:
    #     printGreenMsg(f"yesterday's data copied to {des_ht02zs_FormatData}")
    # else:
    #     printRedMsg("Data corrupt! returning to main menu...")
    #     input("")
    #     return




    # 操作完之后清空temp文件夹
    printYellowMsg("Deleting temp path and archiving zip file...")
    input("")
    erase_folder_contents(temp)
    move_files(zipPath, r"C:\Users\Administrator\Desktop\startTrade\data")

    printGreenMsg("process done, returning to main menu...")
    input("")


def findData():
    # TODO 搞format data好像会炸
    while True:
        os.system("cls")
        print(f"\n\t\t  \033[1\033[42;3;31m FIND DATA MODE \033[0m\n")
        # print("请选择功能：")
        print("\n\t1. 查询单个文件")
        print("\t2. 快速查询 Sell_Buy_List")
        # print("quit. 退出")

        choice = input("\n\n\n\n\nEnter the function you want:\n")

        if choice == '1':
            os.system("cls")

            file_path = input("请拖入 CSV 文件：")
            if file_path.lower() == 'quit':
                print("返回主界面")
                return

            stock_code = input("请输入股票代码：")
            getInfoFromFileName(file_path, product_fund_dict)
            find_stock_data(file_path, stock_code)
        elif choice == "2":
            # TODO finish!

            print("1. CF15")
            print("2. FL18")
            print("3. HT02XY")
            print("4. FL18SC")
            print("5. FL18SCA")
            print("6. FL22SCB")
            productChoice = input("input the product you want.")
            if productChoice == "1":
                quickLookUpSellBuyList(1)
            elif productChoice == "2":
                ...
            elif productChoice == "3":
                ...
            elif productChoice == "4":
                ...
            elif productChoice == "5":
                ...
            elif productChoice == "6":
                ...





        elif choice == "test":
            printYellowMsg("testing for def getInfoFromFileName(file_name, product_fund_dict):")
            x = input()
            getInfoFromFileName(x, product_fund_dict)

            input("press any key to quit testing")
        elif choice.lower() == 'quit':
            print("返回主界面")
            return
        else:
            input("无效选项，请重新输入")


def simpleRiseTopTxt():
    os.system("cls")
    printYellowMsg("\n这个程序不会备份源文件，修改是不可逆的\n")

    file_path = input("请拖入要分析的文件：\n")
    if file_path.lower() == 'quit':
        print("返回主界面")
        return

    print("1. Risestop ----- 监控涨跌停")
    print("2. Unusual ------ 订单异常监控")
    print("3. Order -------- 程序文件")
    print("0. 自定义模式")
    # print("4. ")

    choice = input("\n输入要进行的操作的文件类型: \n")

    if choice == "1":
        printYellowMsg("Auto set the filename with date and file type, \nif not intend to do so, type no.\n")
        isSetName = input("")
        if not isSetName == "no":
            try:
                today = getToday()
                directory = os.path.dirname(file_path)
                new_path = os.path.join(directory, today + "_risestop.log")
                os.rename(file_path, new_path)
                # printYellowMsg(rf"set the filename to {today}")
                file_path = new_path
            except Exception as e:
                # 如果发生异常，打印错误消息
                printRedMsg(f"重命名错误：{e}")
                input("")
            # print(file_path)
            # input("")
        if not file_path:
            printRedMsg("file_path is bad, return to main menu...")
            input("")
            return

        printGreenMsg("backup the log file...")
        originalLogPath = rf"{file_path}\..\originalLog"
        if not os.path.exists(originalLogPath):
            os.makedirs(originalLogPath)
            printGreenMsg(f"路径 {originalLogPath} 创建成功")
        else:
            print(f"路径 {originalLogPath} 已存在，跳过")
        # C:\Users\Administrator\Desktop\startTrade\Log\Risestop\originalLog
        # shutil.move(file_path, originalLogPath, copy_function=shutil.copy2)
        shutil.copy(file_path, originalLogPath)

        remove_lines_with_character(file_path, "Python")
        remove_lines_with_character(file_path, "for more information")
        remove_lines_with_character(file_path, "now_time")
        remove_lines_with_character(file_path, "nowtime")
        remove_lines_with_character(file_path, "没有一字涨停")
        remove_lines_with_character(file_path, "*******************")
        remove_lines_with_character(file_path, "还未到达")
        remove_lines_with_character(file_path, "已到达")
        remove_lines_with_character(file_path, "cb_error <class 'int'>")
        remove_lines_with_character(file_path, "                        ")

        input("return to main menu...")
        input("")
    elif choice == "2":
        printYellowMsg("Auto set the filename with date and file type, \nif not intend to do so, type no.\n")
        isSetName = input("")
        if not isSetName == "no":
            try:
                today = getToday()
                directory = os.path.dirname(file_path)
                new_path = os.path.join(directory, today + "_unusual.log")
                os.rename(file_path, new_path)
                printYellowMsg(rf"set the filename to {today}")
                file_path = new_path
            except Exception as e:
                # 如果发生异常，打印错误消息
                printRedMsg(f"重命名错误：{e}")
                input("")
            # print(file_path)
            # input("")
        if not file_path:
            printRedMsg("file_path is bad, return to main menu...")
            input("")
            return

        printGreenMsg("backup the log file...")
        # originalLogPath = r"C:\Users\Administrator\Desktop\startTrade\Log\Unusual\originalLog"
        originalLogPath = rf"{file_path}\..\originalLog"
        if not os.path.exists(originalLogPath):
            os.makedirs(originalLogPath)
            printGreenMsg(f"路径 {originalLogPath} 创建成功")
        else:
            print(f"路径 {originalLogPath} 已存在，跳过")
        # shutil.move(file_path, originalLogPath, copy_function=shutil.copy2)
        shutil.copy(file_path, originalLogPath)

        remove_lines_with_character(file_path, "无异常订单情况")
        remove_lines_with_character(file_path, "现在在")
        remove_lines_with_character(file_path, "now time")
        remove_lines_with_character(file_path, "Python")
        remove_lines_with_character(file_path, "for more information")

        input("return to main menu...")
        input("")
    elif choice == "3":
        # order
        printYellowMsg("!在这个模式下，拖入文件的同文件夹下所有文件将会被处理!\n")
        printYellowMsg("Auto set the filename with date and file type, \nif not intend to do so, type no.\n")

        # 重命名
        isSetName = input("")
        if not isSetName == "no":
            try:
                printBlueMsg("rename now")
                # 重命名
                rename_py_files(file_path + r"\..", ".log")
                printBlueMsg("rename done")
            except Exception as e:
                # 如果发生异常，打印错误消息
                printRedMsg(f"重命名错误：{e}")
                input("")
            # print(file_path)
            # input("")
        # 如果 file_path是空的，就返回
        if not file_path:
            printRedMsg("file_path is bad, return to main menu...")
            input("")
            return

        # 对这个文件夹下的所有 py 文件进行操作
        files = os.listdir(file_path + r"\..")
        today = getToday()
        for filename in files:
            if today in filename:
                # print(filename)
                orderPath = rf"C:\Users\Administrator\Desktop\startTrade\Log\Order\{filename}"
                printGreenMsg(f"backup the log file {filename}...")
                # originalLogPath = r"C:\Users\Administrator\Desktop\startTrade\Log\Unusual\originalLog"
                originalLogPath = rf"{orderPath}\..\originalLog"
                if not os.path.exists(originalLogPath):
                    os.makedirs(originalLogPath)
                    printGreenMsg(f"路径 {originalLogPath} 创建成功")
                else:
                    print(f"路径 {originalLogPath} 已存在，跳过")
                # print(originalLogPath)
                # print(orderPath)
                # shutil.move(file_path, originalLogPath, copy_function=shutil.copy2)
                try:
                    shutil.copy(orderPath, originalLogPath)
                except Exception as e:
                    # 如果发生异常，打印错误消息
                    printRedMsg(f"移动错误：{e}")
                    input("")

                remove_lines_with_character(orderPath, "交易信号还未到达")
                remove_lines_with_character(orderPath, "Not Trading Time")

        input("return to main menu...")
        input("")

    elif choice == "0":
        printYellowMsg("!在这个模式下，源文件将会被处理!请备份好文件\n")
        printYellowMsg("自定义模式\n")
        input("")

        if not file_path:
            printRedMsg("file_path is bad, return to main menu...")
            input("")
            return
        flag = False
        while not flag:
            x = input("输入要删除的行")
            if x == "quit":
                printYellowMsg("returning to main menu...")
                input("")
                return
            else:
                remove_lines_with_character(file_path, x)

        input("return to main menu...")
        input("")


def baiduToScan():
    today = getToday()
    baiduSyncdiskPath = r"E:\BaiduSyncdisk"
    scanPath = rf"C:\Users\Administrator\Desktop\兴业证券多账户交易"


    fundListInBaidu = ['FL18', 'CF15', 'FL', 'PA', 'HT02', 'FL22SC']
    fundListInScan = ['FL18', 'CF15', 'FL', 'PA', 'HT02', 'FL22SC', 'HT02XY', 'FL22SCA', 'FL22SCB']
    fundListInDivide = ['HT02XY', 'FL22SCA', 'FL22SCB']
    fundListInBaiduAvaliable = ['FL18', 'CF15', 'FL', 'PA']

    # 先把所有信号复制到扫单文件夹
    for fund in fundListInBaiduAvaliable:
        origin = rf"{baiduSyncdiskPath}/Sell_Buy_List_{fund}"
        if fund == "PA":
            target = r"D:\Trade\scan_trade_xt\PAHF"
            # testTarget = r"C:\Users\Administrator\Desktop\startTrade\test_delete_later\pa"
        else:
            target = rf"{scanPath}/{fund}/Sell_Buy_List_{fund}"
            # testTarget = rf"C:\Users\Administrator\Desktop\startTrade\test_delete_later\{fund}/Sell_Buy_List_{fund}"
        copy_files_with_string_no_limited(origin, target, today)
        # 只有在处理 PA 时才会改名
        if fund == "PA":
            modifyNamePAtoPAHF(target)
            move_all_files_with_string(target, r"D:\Trade\scan_trade_xt\PAHF\Sell_Buy_List_PAHF", today)
            # move_all_files_with_string(testTarget, r"C:\Users\Administrator\Desktop\startTrade\test_delete_later\pa\q", "PAHF")



    input("press enter to exit")


def paToPahf():
    today = getToday()
    baiduSyncdiskPath = r"E:\BaiduSyncdisk"

    fundPA = 'PA'

    # 先把所有信号复制到扫单文件夹
    origin = rf"{baiduSyncdiskPath}/Sell_Buy_List_{fundPA}"
    target = r"D:\Trade\scan_trade_xt\PAHF"

    copy_files_with_string_no_limited(origin, target, today)
    modifyNamePAtoPAHF(target)
    move_all_files_with_string(target, r"D:\Trade\scan_trade_xt\PAHF\Sell_Buy_List_PAHF", today)
    # move_all_files_with_string(testTarget, r"C:\Users\Administrator\Desktop\startTrade\test_delete_later\pa\q", "PAHF")

    input("press enter to exit")


def checkYesterdayDataTo37():
    today = getToday()
    print(rf"yesterday was {g_yesterday}")
    checkDataList = []
    checkFormatDataList = ['FL22SCA', 'FL22SCB', "HT02XY", 'HT02ZS']
    limitPricePath = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\limit_price"

    for fundname in checkFormatDataList:
        path = rf"C:\Users\Administrator\Desktop\divide_order_account\{fundname}\format_data"
        count = count_files_with_target_field(path, g_yesterday)
        if count == 3:
            printGreenMsg(f"{fundname}'s format data is prepared.")
        else:
            printRedMsg(f"{fundname}'s format data is NOT prepared, the count is {count}")

    if count_files_with_target_field(limitPricePath, today) == 1:
        printGreenMsg(f"{today}'s limit price data is prepared.")
    else:
        printRedMsg(f"{today}'s limit price data is NOT prepared.")

    format_today = f"{today[:4]}-{today[4:6]}-{today[6:]}"
    if count_files_with_target_field(r"E:\BaiduSyncdisk\Sell_Buy_List_PA", format_today):
        printGreenMsg(f"{today}'s DataCorrect file is generated.")
    else:
        printRedMsg(f"{today}'s DataCorrect file is NOT generated!")

    input("press enter to return to main menu")

def diffGenerateAndCheck():
    today = getToday()
    printYellowMsg(f"NOW RUNNING {diff_excel_path}")
    input("Press enter to continue...")

    thread = threading.Thread(target=run_python_file, args=(diff_excel_path,))
    thread.start()

    thread.join()
    printGreenMsg("diff excel done generating.")

    # 查看表格
    todayTotalDiffPath = rf"C:\Users\Administrator\Desktop\兴业证券多账户交易\totalDiff\持仓差异整合_{today}.xlsx"
    read_and_print_xlsx(todayTotalDiffPath)

    input("press enter to exit")

# def display_current_time():
#     # os.system("cls")
#     os.system('cls' if os.name == 'nt' else 'clear')
#     try:
#         # Define the specific time ranges and their corresponding messages
#         special_time_ranges = [
#             ("00:00", "00:01", "Midnight check!"),
#             ("08:40", "09:20", "Good morning! Time to start your day!"),
#             ("09:20", "09:30", "Real time Signal arrived"),
#             ("09:30", "09:50", "TWAP 1"),
#             ("09:50", "10:10", " - "),
#             ("10:10", "10:30", "TWAP 2 & Morning 1"),
#             ("10:30", "10:50", " - "),
#             ("10:50", "11:00", " - "),
#             ("11:00", "11:20", "TWAP 3 & Morning 2"),
#             ("11:20", "13:30", "Noon break"),
#             ("13:30", "13:40", "TWAP 4"),
#             ("13:40", "14:00", " - "),
#             ("14:00", "14:20", "TWAP 5 & Afternoon 1"),
#             ("14:20", "14:30", " - "),
#             ("14:30", "15:00", "TWAP 6 & Afternoon 2"),
#             ("15:00", "15:30", "Reverse repo"),
#             ("15:30", "17:40", "Wrap up the day!")
#         ]
#
#         while True:
#             now = datetime.now()
#             current_time = now.strftime("%H:%M:%S")
#             current_time_short = now.strftime("%H:%M")
#
#             # Clear the console
#             os.system('cls' if os.name == 'nt' else 'clear')
#
#             # Print the current time
#             print("Current Time:", current_time)
#
#             # Check if current time (HH:MM) is within any of the special time ranges
#             for start, end, message in special_time_ranges:
#                 if start <= current_time_short <= end:
#                     print(f"Special Time Range {start} - {end}: {message}")
#
#             # Wait for 1 second before updating
#             time.sleep(1)
#     except KeyboardInterrupt:
#         ...
#         # 捕捉到键盘中断 (Ctrl+C)，退出循环
#         # print("\n程序已退出")


def afterMain():
    while True:
        os.system("cls")
        menu()
        choice = input("请输入选项数字：")

        if choice == "9":
            before0920processFL22SC()
        elif choice == "1":
            checkYesterdayDataTo37()
        elif choice == "10":
            realTimeSignalMoveForFL22SC()
            realTimeSignalMoveForHT02()
        elif choice == "13":
            dataCollectorOn40()
        elif choice == "3":
            checkExportData()
        elif choice == "6":
            findData()
        elif choice == "7":
            printAllAccountInfo()
        elif choice == "5":
            simpleRiseTopTxt()
        elif choice == "8":
            ...
            # display_current_time()
        elif choice == "99":
            ...
            # downloadDataFromServer40()
        elif choice == "12":
            copYesterdayData()
        elif choice == "2":
            paToPahf()
        elif choice == "11":
            baiduToScan()
        elif choice == "4":
            diffGenerateAndCheck()
        elif choice == "0":
            os.system("cls")
            print("See you tmr.\n")
            print("\n")
            printName()
            x = input("")
            break
        elif choice == "test":
            x = input("file")
            remove_lines_time_in_range_for_order_log(x)
            input("")
        else:
            printRedMsg("无效的选项，请重新输入！")
            input("\n")
            os.system("cls")


def main():
    # global root
    # root = tk.Tk()
    # root.title("Ultimate Trading Tool")
    #
    # # 创建菜单按钮
    # menu_btn = tk.Button(root, text="打开主菜单", command=afterMain)
    # menu_btn.pack(pady=20)
    #
    # output_text = tk.Text(root, height=10, width=50)
    # output_text.pack(padx=10, pady=10)
    #
    # root.mainloop()
    global g_yesterday
    temp = getYesterday()
    while 0:
        x = input("Wrong or Right? y/n \n")
        if x == "y" or "":
            g_yesterday = temp
            break
        elif x == "n":
            g_yesterday = input("enter yesterday's date (format: YYYYMMDD):")
            break
        else:
            print("enter the right choice")
    afterMain()


def menu():
    # TODOed 写一个可以便捷查询真实持仓的小程序
    # ipAddr = get_public_ip()

    print("----------------------------------------------")
    print(f"\t\t  \033[1\033[42;3;31m MAIN MENU \033[0m")

    print("1. 检查 昨日数据分析的数据 & 云盘是否正常工作")
    print("2. PA -> PAHF -> Move")
    print("3. 收盘拆分导出数据的拆分和检查 ")
    print("4. Diff 持仓差异分析并查看")
    print("5. 存档并简化 LOG 记录")
    print("6. 查询数据")
    print("7. 查看各个账号密码")
    print("8. 时钟")
    print("0. 退出")
    print("")
    print(f"\033[33m已停用功能: \033[0m")
    print("9.  拆分 FL22SC, HT02 的原始信号并移回源路径 *已停用*")
    print("10. 移动拆分后的 FL22SC, HT02 的实时信号 *已停用*")
    print("11. 百度网盘同步空间 -> 扫单文件夹 *已停用*")
    print("12. 昨日数据分析的数据 -> 分单文件夹 *已停用* ")
    print("13. 自动整理数据分析的数据 *已停用*")

    # print("10. 从另一台机器上的 HTTP 服务器上 fetch 文件(已删除)         ")

    # printGreenMsg(f"\n这台机器的 IP 地址是： {ipAddr}")
    # printYellowMsg("\n适用于 61 的功能: 1, 2, 3, 4")
    # printYellowMsg("适用于 40 的功能: 5")
    # printYellowMsg("适用于本机的功能: 9")
    print("----------------------------------------------")


if __name__ == "__main__":
    os.system("cls")
    main()
