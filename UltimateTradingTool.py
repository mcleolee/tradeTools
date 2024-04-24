# TODO
import os
import shutil
from datetime import datetime

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
        print(f"The file {path} does not exist.")
        return False


def menu():
    print("Welcome to the ultimate trading tool ever.")
    print("1. 拆分 FL22SC 并移回源路径")
    print("2. 功能二")
    print("3. 功能三")
    print("0. 退出")


def before0920processFL22SC():
    oriFl22 = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SC\Sell_Buy_List_FL22SC"
    os.system("cls")
    today = getToday()

    oriBuy = rf"{oriFl22}\{buy}FL22SC_{today}.csv"
    oriSell = rf"{oriFl22}\{sell}FL22SC_{today}.csv"
    oriJrcc = rf"{oriFl22}\{jrcc}FL22SC_{today}.csv"

    # 检查原始信号在不在，不在直接退
    if ((ifExist(oriBuy) and ifExist(oriSell) and ifExist(oriJrcc)) == False):
        print("There are no original signal!!!\nreturning...")
        input("")
        return
    else:
        print("original signal EXIST.")

    # 然后移动到目标文件夹
    divideFl22 = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SC\Sell_Buy_List_FL22SC"
    copy_file(oriBuy, divideFl22)
    copy_file(oriSell, divideFl22)
    copy_file(oriJrcc, divideFl22)

    # 运行分单脚本
    os.system(r"C:\Users\Administrator\Desktop\divide_order_account\projects\1、盘前订单拆分.py")
    input("1、盘前订单拆分.py is ending, press any key to continue...")

    # 检测拆分是否成功
    divide_SCA = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SCA"
    divide_SCB = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\Sell_Buy_List_FL22SCB"
    ori_SCA = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\Sell_Buy_List_FL22SCA"
    ori_SCB = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\Sell_Buy_List_FL22SCB"

    divideSCAbuy = rf"{divide_SCA}\{buy}FL22SCA_{today}"
    divideSCAsell = rf"{divide_SCA}\{sell}FL22SCA_{today}"
    divideSCBbuy = rf"{divide_SCB}\{buy}FL22SCB_{today}"
    divideSCBsell = rf"{divide_SCB}\{sell}FL22SCB_{today}"

    oriSCAbuy =  rf"{ori_SCA}\{buy}FL22SCA_{today}"
    oriSCAsell = rf"{ori_SCA}\{sell}FL22SCA_{today}"
    oriSCBbuy =  rf"{ori_SCB}\{buy}FL22SCB_{today}"
    oriSCBsell = rf"{ori_SCB}\{sell}FL22SCB_{today}"

    if (ifExist(divideSCAbuy) and ifExist(divideSCAsell) and ifExist(divideSCBbuy) and ifExist(divideSCBsell)) == False:
        print("signal dividing fail!!!\nreturning...")
        input("")
        return
    else:
        print("signal dividing DONE.")

    # 传回文件
    copy_file(divideSCAbuy, oriSCAbuy)
    copy_file(divideSCAsell, oriSCAsell)
    copy_file(divideSCBbuy, oriSCBbuy)
    copy_file(divideSCBsell, oriSCBsell)

    # 检查文件是否复制成功
    if (ifExist(oriSCAbuy) and ifExist(oriSCAsell) and ifExist(oriSCBbuy) and ifExist(oriSCBsell)) == False:
        print("signal dividing fail!!!\nreturning...")
        input("")
        return
    else:
        print("copy file DONE.")

    input("function before0920processFL22SC is ending, press any key to continue...")


def function_two():
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
            function_two()
        elif choice == "3":
            function_three()
        elif choice == "0":
            os.system("cls")
            print("See you tmr.\n")
            x = input("")
            break
        else:
            print("无效的选项，请重新输入！")


if __name__ == "__main__":
    main()
