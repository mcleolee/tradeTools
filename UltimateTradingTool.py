# TODO
import os
import shutil
from datetime import datetime

DEBUG_MODE = 1

os.system("mode con cols=250 lines=30")

m = "morning"
m2 = "morning2Two"
a = "afternoon"
a2 = "afternoon2Two"

nom_ = "NoSellingMorning_"
nom2_ = "NoSellingMorning2Two_"
noa_ = "NoSellingAfternoon_"
noa2_ = "NoSellingAfternoon2Two_"
underline = "_"

sell = "SellOrderList"
buy = "BuyOrderList"
jrcc = "JinRiChiCang"

divide_SC  = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SC"
divide_SCA = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCA\Sell_Buy_List_FL22SCA"
divide_SCB = r"C:\Users\Administrator\Desktop\divide_order_account\FL22SCB\Sell_Buy_List_FL22SCB"
ori_SC  = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SC\Sell_Buy_List_FL22SC"
ori_SCA = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCA\Sell_Buy_List_FL22SCA"
ori_SCB = r"C:\Users\Administrator\Desktop\兴业证券多账户交易\FL22SCB\Sell_Buy_List_FL22SCB"


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
        ret = shutil.copy(original_path, target_path)
        print(f"文件已从 {original_path} 复制到 {target_path}")
        return ret
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

def printBlueMsg(text):
    print(f"\033[34m{text}\033[0m\n")
    return f"\033[34m{text}\033[0m"

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
    os.system("cls")
    # 先定义一下, 实时信号是直接传到 ori 文件夹的
    today = getToday()
    nom =  rf"{ori_SC}\{nom_}{today}.txt"
    nom2 = rf"{ori_SC}\{nom2_}{today}.txt"
    noa =  rf"{ori_SC}\{noa_}{today}.txt"
    noa2 = rf"{ori_SC}\{noa2_}{today}.txt"

    # FIXME 才意识到可以，选择数字之后，比如说2，就直接 nowTimeNode = m2 就可以很方便了。。。
    # FIXME 没有意识到一个信号拆分后可能是A有信号B是no信号！！
    # FIXME 只要早上有一次 No morning, 那接着的每一次都将要复制一次
    # 选择实时信号
    while True:
        printYellowMsg("\n请确认实时信号节点？(1/2/3/4):\n1：morning; 2：morning2Two; 3：afternoon; 4：afternoon2Two\n")
        choice = input("")
        if choice == "1":
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
            oriBno =   rf"{ori_SCB}\{nom_}{today}.txt"

            break
        elif choice == "2":
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
            oriBno =   rf"{ori_SCB}\{nom2_}{today}.txt"
            break
        elif choice == "3":
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
            oriBno =   rf"{ori_SCB}\{noa_}{today}.txt"

            break
        elif choice == "4":
            rtsSell = ""
            rtsBuy = rf"{ori_SC}\{buy}FL22SC{a2}_{today}.csv"
            rtsJRCC = rf"{ori_SC}\{jrcc}FL22SC{a2}_{today}.csv"
            rtsNoSignal = noa2
            divideAbuy =  rf"{divide_SCA}\{buy}FL22SCA{a2}_{today}.csv"
            divideAjrcc = rf"{divide_SCA}\{jrcc}FL22SCA{a2}_{today}.csv"
            divideBbuy =  rf"{divide_SCB}\{buy}FL22SCB{a2}_{today}.csv"
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
        elif choice == "quit":
            printBlueMsg("returning to main menu...\n")
            input("")
            return
        else:
            printRedMsg("无效的选项，请重新输入！")

    # 检查实时信号到了没有
    printYellowMsg("checking whether the real time signals are arrive...")
    isNoSignal = ifExist(rtsNoSignal)
    isRealTimeSignal = (ifExist(rtsSell) or ifExist(rtsBuy) and ifExist(rtsJRCC))
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
    if choice == "4":
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
    if choice == "4":
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
    if choice == "4":
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
    print("3. 整理数据分析的数据")
    print("0. 退出")
    printYellowMsg("\n功能 1、2 在阿里云 61 上适配")
    printYellowMsg("功能 3 只在数据分析 40 上适配")
    print("----------------------------------------------")


if __name__ == "__main__":
    os.system("cls")
    main()


