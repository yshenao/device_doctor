from application.apps.testpoint.rule import Rule
from application.apps.testpoint.db.mongodb import MongoDBClient
from application.util import deduplication, timestamp_to_localtime


class Analyze(Rule):
    def __init__(self):
        super(Rule, self).__init__()
        self.total_cnt = 0
        self.abnormal_cnt = 0
        self.disturbed_cnt = 0

    def process(self, cronjob_id):
        testpoint_map = self.preload()
        self.analyze(testpoint_map, cronjob_id)

    def preload(self):
        # 数据预加载
        # 从DB加载数据到内存中
        testpoint_list = MongoDBClient().get_all_testpoint_info()
        # 构造map，id到info的映射
        testpoint_map = {}
        for t in testpoint_list:
            if not testpoint_map.get(t.bsMeasureControlPointId):
                testpoint_map[t.bsMeasureControlPointId] = [
                    {
                        'taTimestamp': t.taTimestamp,
                        'voff_Revised': t.voff_Revised
                    }
                ]
                continue
            testpoint_map[t.bsMeasureControlPointId] += {
                'taTimestamp': t.taTimestamp,
                'voff_Revised': t.voff_Revised
            }
        # 如果存在单时间点多条数据，按照如下顺序取值：众数 -> 平均数
        for id, info in testpoint_map.items():
            testpoint_map[id] = deduplication(info)
        # # 时间戳转成日期
        # for id, info in testpoint_map.items():
        #     testpoint_map[id] = {
        #         'taTimestamp': timestamp_to_localtime(info.get('taTimestamp')),
        #         'voff_Revised': info.voff_Revised
        #     }
        self.total_cnt = len(testpoint_map)
        return testpoint_map

    def analyze(self, testpoint_map, cronjob_id):
        for id, info in testpoint_map.items():
            is_data_lost, start_time, end_time = self.cal_is_data_lost(info)
            abnormal_time, disturbed_time = self.cal_abnormal_data(info)
            if len(abnormal_time) > 0:
                self.abnormal_cnt += 1
            if len(disturbed_time) > 0:
                self.disturbed_cnt += 1
            self.MysqlClient.add_testpoint_abnormal_analysis(
                id=id,
                is_data_lost=is_data_lost,
                start_time=start_time,
                end_time=end_time,
                abnormal_time=abnormal_time,
                disturbed_time=abnormal_time,
                cronjob_id=cronjob_id
            )

    def cal_is_data_lost(self, info):
        # 计算测试桩数据是否丢失
        start_time = info[0].taTimestamp
        end_time = info[len(info) - 1].taTimestamp
        # 按照10分钟采集一次数据计算
        expect_cnt = (end_time - start_time) / 1000 / 60 / 10
        actual_cnt = len(info)

        if actual_cnt * 100 / expect_cnt > 90:
            return False, start_time, end_time
        return True, start_time, end_time

    def cal_abnormal_data(self, info):
        # 计算异常数据
        abnormal_time, disturbed_time = [], []

        is_abnormal, abnormal_start_time, abnormal_end_time = False, None, None
        for f in info:
            if f.voff_Revised < -1.2 or f.voff_Revised > -0.85:
                is_abnormal = True
                abnormal_end_time = timestamp_to_localtime(f.taTimestamp)
                if not abnormal_start_time:
                    abnormal_start_time = timestamp_to_localtime(f.taTimestamp)
                continue
            if abnormal_start_time:
                abnormal_end_time = timestamp_to_localtime(f.taTimestamp)
            if abnormal_start_time and abnormal_end_time:
                disturbed_time += {
                    'start_time': abnormal_start_time,
                    'end_time': abnormal_end_time
                }
                is_abnormal, abnormal_start_time, abnormal_end_time = False, None, None

        if is_abnormal:
            abnormal_time += {
                'start_time': abnormal_start_time,
                'end_time': abnormal_end_time
            }
        return abnormal_time, disturbed_time
