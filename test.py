from datetime import datetime, timedelta

def is_third_friday_or_surrounding_days():
    # 获取今天的日期
    today = datetime.now()
    # 获取本月的第一天
    first_day_of_month = today.replace(day=1)
    # 获取本月第一天是星期几
    first_day_weekday = first_day_of_month.weekday()

    # 计算本月的第三个周五的日期
    # 计算从第一天到第一个周五的天数
    days_to_first_friday = (4 - first_day_weekday + 7) % 7  # 4是周五，weekday()返回0-6
    first_friday = first_day_of_month + timedelta(days=days_to_first_friday)
    
    # 计算第三个周五的日期
    third_friday = first_friday + timedelta(weeks=2)  # 从第一个周五开始，计算两周后即第三个周五
    
    # 计算前三天和后三天的日期范围
    before_three_days = third_friday - timedelta(days=3)
    after_three_days = third_friday + timedelta(days=3)

    
    # 优化：检查今天是否在前三天到后三天的范围内
    if before_three_days.date() <= today.date() <= after_three_days.date():
        return True
    
    return False


if __name__ == '__main__':
    if is_third_friday_or_surrounding_days():
        print('今天是本月的第三个周五或其前三天或后三天')
    else:
        print('今天不是本月的第三个周五或其前三天或后三天')

