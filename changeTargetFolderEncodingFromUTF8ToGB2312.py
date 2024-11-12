import os
import shutil
import chardet
import tqdm


def is_utf8(file_path):
    """检测文件是否为UTF-8编码"""
    with open(file_path, 'rb') as file:
        raw_data = file.read(1024)
    result = chardet.detect(raw_data)
    return result['encoding'] == 'utf-8'


def backup_file(file_path):
    """将原始文件备份，在文件名后加.backup后缀"""
    backup_path = file_path + ".backup"
    if not os.path.exists(backup_path):
        shutil.copy(file_path, backup_path)
        print(f"备份成功: {file_path} -> {backup_path}")
    else:
        print(f"备份已存在，跳过: {backup_path}")


def convert_to_gb2312_in_place(input_dir):
    """在原目录中将UTF-8文件转换为GB2312编码，备份原文件"""
    for root, _, files in os.walk(input_dir):
        for file_name in tqdm.tqdm(files, desc=f'Processing {input_dir}'):
            input_file_path = os.path.join(root, file_name)

            # 仅转换UTF-8文件
            if not is_utf8(input_file_path):
                print(f"跳过: {input_file_path} 不是UTF-8编码")
                continue

            # 备份原始文件
            # backup_file(input_file_path)

            # 读取UTF-8文件并转换为GB2312
            try:
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                # 用GB2312覆盖原始文件
                with open(input_file_path, 'w', encoding='gb2312', errors='ignore') as file:
                    file.write(content)
                print(f"转换成功: {input_file_path}")
            except Exception as e:
                print(f"转换失败: {input_file_path}, 错误: {e}")


if __name__ == "__main__":

    contractsName = ['IC_202212', 'IC_202301', 'IC_202302', 'IC_202303', 'IC_202304', 'IC_202305', 'IC_202306', 'IC_202307', 'IC_202308', 'IC_202309', 'IC_202310', 'IC_202311', 'IC_202312', 'IC_202401',
                     'IC_202402', 'IC_202403', 'IC_202404', 'IC_202405', 'IC_202406', 'IC_202407', 'IC_202408', 'IC_202409']
    # for contract in contractsName:
    for contract in tqdm.tqdm(contractsName, desc='Processing'):
        input_dir = rf'C:\Users\progene12\share\FUTURES_DATA\{contract}'
        convert_to_gb2312_in_place(input_dir)

