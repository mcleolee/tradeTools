from datetime import datetime, timedelta, date
import pandas as pd
import os
import chardet

def getDate(seperator: str, deltaDays: int = 0) -> str:
    """
    @brief 返回指定日期格式的字符串
    @param seperator: 用于分割日期部分的字符，如“-”或“/”
    @param deltaDays: 距离今天的天数偏移，负值表示过去的日期，正值表示未来的日期
    @return 返回格式化的日期字符串，格式为 YYYY[seperator]MM[seperator]DD
    """
    target_date = datetime.now() + timedelta(days=deltaDays)
    return target_date.strftime(f"%Y{seperator}%m{seperator}%d")

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


class file:
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
                encoding = result['encoding']

            # 读取文件内容
            with open(input_file, 'r', encoding=encoding) as infile:
                content = infile.read()

            # 写入到新的文件
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(content)

            # print(f"Successfully converted {input_file} to UTF-8 and saved as {output_file}.")
        except Exception as e:
            print(f"An error occurred: {e} GDNXCT")

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



def futuresData():
    """
    这个功能帮助导出期货数据，

    遍历产品列表，提示用户当前应该进行到哪个产品。一旦用户将文件导出到目标文件夹，程序就监控到这个文件，
    然后根据文件的表头来判断是什么数据，然后将这个文件重命名为对应的文件名。
    当导出了两个文件后，就生成asset文件，让用户粘贴相应文字进入，保存文件，然后重置count，继续下一个产品。

    :return:
    """
    import time
    def monitor_and_process_products(monitorPath, futuresProducts):
        today = getDate('')
        known_files = set(os.listdir(monitorPath))  # 已知文件列表

        for product in futuresProducts:
            fileCount = 0  # 记录导出的文件数量
            printPurpleMsg(f"-> NOW EXPORT {product} <-")
            printYellowMsg(f'Already exported {fileCount} files')

            while fileCount < 2:
                current_files = set(os.listdir(monitorPath))
                new_files = current_files - known_files
                known_files = current_files

                if not new_files:
                    time.sleep(1)
                    continue

                for file_name in new_files:
                    file_path = os.path.join(monitorPath, file_name)
                    try:
                        # 假设文件是 CSV 格式
                        file.saveAsUft8(file_path)
                        df = pd.read_csv(file_path, encoding='utf-8')


                        # 如果文件表头包含 '成交合约'，则重命名为交易文件
                        if '成交合约' in df.columns:
                            transaction_file = os.path.join(monitorPath, product, f"transaction_{today}.csv")
                            df.to_csv(transaction_file, index=False)
                            printGreenMsg(f"Transaction data exported to {transaction_file}")
                            # 删除源文件
                            os.remove(file_path)
                            fileCount += 1
                        # 如果文件表头包含 '持仓合约'，则重命名为持仓文件
                        elif '持仓合约' in df.columns:
                            holding_file = os.path.join(monitorPath, product, f"holding_{today}.csv")
                            df.to_csv(holding_file, index=False)
                            printGreenMsg(f"Holding data exported to {holding_file}")
                            # 删除源文件
                            os.remove(file_path)
                            fileCount += 1

                        # 当导出两个文件后，跳出循环生成 asset 文件
                        if fileCount == 2:
                            printGreenMsg(f"Exported all {fileCount} files for {product}")
                            assetPath = os.path.join(monitorPath, product)
                            generate_asset_file(assetPath, today)
                            break
                        else:
                            printYellowMsg(f'Already exported {fileCount} files, left {2 - fileCount} files to export')
                    except Exception as e:
                        print(f"Error processing file '{file_name}': {e}")

                # 更新已知文件列表
                known_files = current_files

    def generate_asset_file(path, today):
        asset_file = os.path.join(path, f"asset_{today}.txt")
        printCyanMsg(f'Please copy asset information, end with "q"')

        assetInfo = []
        while True:
            line = input()
            if line.strip().lower() == "q":
                break
            assetInfo.append(line)

        with open(asset_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(assetInfo))
        printGreenMsg(f"Asset file saved to {asset_file}")

    monitorPath = r'D:\TRADE\FuturesData'
    futuresProducts = ['CF15', 'HT02']  # 期货产品列表
    monitor_and_process_products(monitorPath, futuresProducts)

    print("=== End of futures data export ===")
    input("")