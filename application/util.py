import time


def timestamp_to_localtime(t):
    # 时间戳转成UTC+8北京时区
    if not t:
        return t
    loc_time = time.localtime(t / 1000 + 8 * 60 * 60)
    return time.strftime('%Y-%m-%d %H:%M:%S', loc_time)


# 如果存在单时间点多条数据，按照如下顺序取值：众数 -> 平均数
def deduplication(list):
    print('开始len：{}, value：{}'.format(len(list), list))
    result = []
    cur_time = 0
    cur_map = {}
    for i in list:
        if cur_time == 0:
            cur_time = i.get('taTimestamp')
            cur_map[i.get('voff_Revised')] = 1
        elif cur_time == i.get('taTimestamp'):
            if cur_map.get(i.get('voff_Revised')):
                cur_map[i.get('voff_Revised')] += 1
            else:
                cur_map[i.get('voff_Revised')] = 1
        else:
            result.append(
                {
                    'taTimestamp': cur_time,
                    'voff_Revised': get_value(cur_map)
                }
            )
            cur_time = i.get('taTimestamp')
            cur_map = {i.get('voff_Revised'): 1}
    if cur_time != 0 and len(cur_map) > 0:
        result.append(
            {
                'taTimestamp': cur_time,
                'voff_Revised': get_value(cur_map)
            }
        )
    print('结束len：{}, value：{}'.format(len(result), result))
    return result


def get_value(m):
    max_value = 0
    result = []
    for key, value in m.items():
        if value > max_value:
            max_value = value
    for key, value in m.items():
        if value == max_value:
            result.append(key)
    return avg(result)


def avg(list):
    l = len(list)
    sum = 0
    for i in list:
        sum += i
    return float(sum) / float(l)
