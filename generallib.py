from datetime import datetime, timedelta




def getDate(seperator: str, deltaDays: int = 0) -> str:
    """
    @brief 返回指定日期格式的字符串
    @param seperator: 用于分割日期部分的字符，如“-”或“/”
    @param deltaDays: 距离今天的天数偏移，负值表示过去的日期，正值表示未来的日期
    @return 返回格式化的日期字符串，格式为 YYYY[seperator]MM[seperator]DD
    """
    target_date = datetime.now() + timedelta(days=deltaDays)
    return target_date.strftime(f"%Y{seperator}%m{seperator}%d")




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