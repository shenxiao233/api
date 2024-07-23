import json
from collections import deque
def json_process():
    # 读取JSON文件
    file_path = "C:/Users/yang/Desktop/jsondata/14d0a057154f9a4d2c98d9c91137c966/202404_windows-google-chrome-1709530945035.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 按键（日期）排序
    sorted_data = dict(sorted(data.items()))

    # 遍历数据并将毫秒转换为秒
    for date, values in sorted_data.items():
        for key, value in values.items():
            # 如果值是一个列表，且长度为2（假设值的格式是 [数量, 毫秒]）
            if isinstance(value, list) and len(value) == 2:
                # 将毫秒转换为秒并转换为整数
                sorted_data[date][key][1] = int(value[1] // 1000)  # 将毫秒转换为秒并转换为整数

    # 创建一个临时列表来存储需要删除的条目
    to_delete = []

    # 遍历数据并标记需要删除的条目
    for date, values in sorted_data.items():
        for key, value in values.items():
            if 0 in value:
                to_delete.append((date, key))

    # 遍历需要删除的条目并从数据中删除它们
    for date, key in to_delete:
        del sorted_data[date][key]

    # 转换为JSON
    sorted_json = json.dumps(sorted_data, indent=4, ensure_ascii=False)

    # 获取所有日期的网址数据
    all_visits = [visits for date, visits in sorted_data.items()]

    # 创建一个字典，用于统计每个网址的总时长和总访问次数
    statistics = {}

    # 统计每个网址的总时长和总访问次数
    for visits in all_visits:
        for url, (visit_count, visit_duration) in visits.items():
            if url not in statistics:
                statistics[url] = [0, 0]  # 初始化网址的统计信息
            statistics[url][0] += visit_duration
            statistics[url][1] += visit_count

    # 获取浏览时间最长的前五个网址
    top_five = sorted(statistics.items(), key=lambda x: x[1][0], reverse=True)[:5]


    # 统计本月访问总时长和浏览次数
    total_duration_this_month = sum(duration for duration, _ in statistics.values())
    total_visits_this_month = sum(visits for _, visits in statistics.values())



    return sorted_json,top_five, total_duration_this_month, total_visits_this_month

def data_set():
    sorted_json, top_five, total_duration_this_month, total_visits_this_month = json_process()
    return top_five, total_duration_this_month, total_visits_this_month
def data_get():
    sorted_json, top_five, total_duration_this_month, total_visits_this_month = json_process()

    return sorted_json

def website_data_get():
    sorted_json=data_get()
    data = json.loads(sorted_json)
    website_names = set()
    for date_data in data.values():
        for website_name in date_data.keys():
            website_names.add(website_name)

    # 打印去重后的网站名称列表
    return  website_names


def get_processed_data(processed_input):
    # 将输入数据赋值给变量
    ini_data = data_get()
    json_data = json.loads(ini_data)

    # 初始化统计数据
    total_duration = 0
    total_visits = 0
    active_days = 0
    max_duration = 0
    max_visits = 0
    daily_data = {}  # 存储每一天的访问时长和访问次数

    # 遍历json_data，找到所有日期中该网站的数据，并将访问次数和总浏览时长相加
    for date, date_data in json_data.items():
        visits = 0
        duration = 0

        if processed_input in date_data:
            visits, duration = date_data[processed_input]

        total_visits += visits
        total_duration += duration
        active_days += 1

        # 记录每一天的访问时长和访问次数
        daily_data[date] = {'visits': visits, 'duration': duration}

        # 更新最大浏览时长和最大访问次数
        if duration > max_duration:
            max_duration = duration
        if visits > max_visits:
            max_visits = visits

            # 使用deque来存储最后七天的数据
        last_seven_days_data = deque(maxlen=7)

        # 逆序遍历daily_data，将最后七天的数据存储到last_seven_days_data中
        for date in reversed(sorted(daily_data.keys())):
            last_seven_days_data.appendleft((date, daily_data[date]))
            if len(last_seven_days_data) == 7:
                break

        # 将last_seven_days_data转换为字典形式
        last_seven_days_data_dict = dict(last_seven_days_data)

    # 逐个返回处理后的数据
    return processed_input, total_visits, total_duration, active_days, max_duration, max_visits, last_seven_days_data_dict











