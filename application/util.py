import time


def timestamp_to_localtime(t):
    # 时间戳转成UTC+8北京时区
    if not t:
        return t
    loc_time = time.localtime(t / 1000 + 8 * 60 * 60)
    return time.strftime('%Y-%m-%d %H:%M:%S', loc_time)
