import os
import shutil
import subprocess


def erase_folder_contents(folder_path):
    try:
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)

        # 删除每个文件
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Failed to erase folder contents. Error: {e}")



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

    # try:
    #     # 清空目标文件夹
    #     for file in os.listdir(destination_folder):
    #         destination_file = os.path.join(destination_folder, file)
    #         os.remove(destination_file)
    #         print(f"Deleted: {destination_file}")
    # except Exception as e:
    #     print(f"Failed to delete files. Error: {e}")


if __name__ == "__main__":
    folder1 = r"C:\Users\progene12\share\dataCollector\GRID"
    folder2 = r"C:\Users\progene12\share\dataCollector\PAHF"
    folder3 = r"C:\Users\progene12\share\dataCollector\YL17"
    erase_folder_contents(folder1)
    erase_folder_contents(folder2)
    erase_folder_contents(folder3)

    # 示例用法
    source_folder_1 = r"D:\TRADE\grid_trade\trade_data"
    source_folder_2 = r"D:\TRADE\scan_trade_xt\PAHF\data"
    source_folder_3 = r"D:\TRADE\scan_trade_xt\YL17YH\data"

    destination_folder_1 = r"C:\Users\progene12\share\dataCollector\GRID"
    destination_folder_2 = r"C:\Users\progene12\share\dataCollector\PAHF"
    destination_folder_3 = r"C:\Users\progene12\share\dataCollector\YL17"

    copy_latest_files(source_folder_1, destination_folder_1 )
    copy_latest_files(source_folder_2, destination_folder_2 )
    copy_latest_files(source_folder_3, destination_folder_3 )

    print("\n")
    # os.system(".\\C:\\Users\\progene12\\share\\httpServer.bat")

    # # 指定.bat文件的完整路径
    bat_file_path = "C:\\Users\\progene12\\share\\httpServer.bat"
    #
    # # 构建命令列表，使用Popen运行.bat文件
    # try:
    #     # 启动进程
    #     process = subprocess.Popen(bat_file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     # 等待进程执行完成并获取输出结果
    #     stdout, stderr = process.communicate()
    #     # 打印输出结果
    #     if stdout:
    #         print("Output from the bat file:")
    #         print(stdout.decode())
    #         print("\nThe server is ONLINE\n")
    #     # 如果有错误信息，打印错误信息
    #     if stderr:
    #         print("Error from the bat file:")
    #         print(stderr.decode())
    # except Exception as e:
    #     print(f"An error occurred while trying to run the bat file: {e}")
    print("\nThe server is ONLINE\n")
    os.system(bat_file_path)


    input("Press Enter to exit...")