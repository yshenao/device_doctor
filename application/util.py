import time


def timestamp_to_localtime(t):
    # 时间戳转成UTC+8北京时区
    if not t:
        return t
    loc_time = time.localtime(t / 1000 + 8 * 60 * 60)
    return time.strftime('%Y-%m-%d %H:%M:%S', loc_time)


# 如果存在单时间点多条数据，按照如下顺序取值：众数 -> 平均数
def deduplication(list):
    # TODO
    return list
