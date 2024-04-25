# TODO
import os
import shutil
from datetime import datetime

DEBUG_MODE = 1

testFile = r"C:\Users\progene12\Desktop\A\api key.txt"
testPathA = r"C:\Users\progene12\Desktop\A"
testPathB = r"C:\Users\progene12\Desktop\B"

m = "morning"
m2 = "morning2Two"
a = "afternoon"
a2 = "afternoon2Two"
underline = "_"

sell = "SellOrderList"
buy = "BuyOrderList"
jrcc = "JinRiChiCang"


def init():
    print("starting init")


def getToday():
    currentDatetime = datetime.now()
    today = currentDatetime.strftime("%Y%m%d")
    print(f"today is {today}\n")
    return today


def file_exists(file_path):
    return os.path.exists(file_path)


def copy_file(original_path, target_path):
    try:
        shutil.copy(original_path, target_path)
        print(f"文件已从 {original_path} 复制到 {target_path}")
    except IOError as e:
        print(f"无法复制文件: {e}")


def copy_latest_files(source_folder, destination_folder):
    try:
        # 获取源文件夹中按时间排序的文件列表
        files = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)),
                       reverse=True)

        # 仅复制最新的四个文件
        for file in files[:4]:
            source_file = os.path.join(source_folder, file)
            destination_file = os.path.join(destination_folder, file)

            # 复制文件
            shutil.copy2(source_file, destination_folder)
            print(f"Copied: {source_file} to {destination_file}")
    except Exception as e:
        print(f"Failed to copy files. Error: {e}")


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

def before0920processFL22SC():
    oriFl22 = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SC\Sell_Buy_List_FL22SC"
    os.system("cls")
    today = getToday()

    oriBuy = rf"{oriFl22}\{buy}FL22SC_{today}.csv"
    oriSell = rf"{oriFl22}\{sell}FL22SC_{today}.csv"
    oriJrcc = rf"{oriFl22}\{jrcc}FL22SC_{today}.csv"

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
    # FIXME 这个功能不能正常运行
    # os.system(r"C:\PROGRA~1\Python36\python.exe" r"C:\Users\Administrator\Desktop\divide_order_account\projects\1、盘前订单拆分.py")
    # input("1、盘前订单拆分.py is ending, press any key to continue...")
    printYellowMsg("Plz run the 1、盘前订单拆分.py by hand, press any key to continue after finishing running...")
    input(" ")


    # 检测拆分是否成功
    divide_SCA = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SCA"
    divide_SCB = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\Sell_Buy_List_FL22SCB"
    ori_SCA = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\Sell_Buy_List_FL22SCA"
    ori_SCB = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\Sell_Buy_List_FL22SCB"

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

    if not ( isDivideSCABExist ):
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


def realTimeSignalMoveForFL22SC():
    print("这是功能二！")


def function_three():
    print("这是功能三！")


def main():
    # init()
    while True:
        menu()
        choice = input("请输入选项数字：")

        if choice == "1":
            before0920processFL22SC()
        elif choice == "2":
            realTimeSignalMoveForFL22SC()
        elif choice == "3":
            function_three()
        elif choice == "0":
            os.system("cls")
            print("See you tmr.\n")
            x = input("")
            break
        else:
            print("无效的选项，请重新输入！")


def menu():
    print("----------------------------------------------")
    print("Welcome to the ultimate trading tool ever.")
    print("1. 拆分 FL22SC 并移回源路径")
    print("2. 移动拆分后的 FL22SC 的实时信号到源路径")
    print("3. 功能三")
    print("0. 退出")
    print("----------------------------------------------")


if __name__ == "__main__":
    main()
