from application.apps.testpoint.rule import Rule
from application.apps.testpoint.db.mongodb import MongoDBClient
from application.util import deduplication, timestamp_to_localtime
from application.apps.testpoint.db.dal import DBProxy


class Analyze(Rule):
    def __init__(self):
        super().__init__()
        self.record_cnt = 0
        self.invalid_record_cnt = 0
        self.total_cnt = 0
        self.data_lost_cnt = 0
        self.abnormal_cnt = 0
        self.disturbed_cnt = 0
        self.normal_cnt = 0

    def preload(self):
        # 数据预加载
        # 从DB加载数据到内存中
        testpoint_list = MongoDBClient().get_all_testpoint_info()
        # 构造map，id到info的映射
        testpoint_map = {}
        for t in testpoint_list:
            # 没有唯一标识的id直接跳过不处理
            if not t.get('bsMeasureControlPointId') or not t.get('taTimestamp') or not t.get('voff_Revised'):
                continue
            if not testpoint_map.get(t['bsMeasureControlPointId']):
                testpoint_map[t['bsMeasureControlPointId']] = [
                    {
                        'taTimestamp': t.get('taTimestamp'),
                        'voff_Revised': t.get('voff_Revised')
                    }
                ]
                continue
            testpoint_map[t['bsMeasureControlPointId']].append({
                'taTimestamp': t.get('taTimestamp'),
                'voff_Revised': t.get('voff_Revised')
            })
        # 如果存在单时间点多条数据，按照如下顺序取值：众数 -> 平均数
        deduplicate_testpoint_map = {}
        for id, info in testpoint_map.items():
            deduplicate_testpoint_map[id] = deduplication(info)
        self.total_cnt = len(deduplicate_testpoint_map)
        print('第一次数据处理完成：{}'.format(self.total_cnt))
        return deduplicate_testpoint_map

    def analyze(self, testpoint_map, cronjob_id):
        self.MysqlClient2 = DBProxy()
        for id, info in testpoint_map.items():
            print('开始对测试桩进行异常分析id：{}'.format(id))
            result, abnormal_time, disturbed_time = '', None, None
            is_data_lost, start_time, end_time = self.cal_is_data_lost(info)
            if is_data_lost:
                self.data_lost_cnt += 1
                result = '数据丢失'
            else:
                abnormal_time, disturbed_time = self.cal_abnormal_data(info)
                if len(abnormal_time) == 0:
                    self.normal_cnt += 1
                    result = '正常'
                elif len(abnormal_time) > 0 and len(disturbed_time) > 0:
                    self.disturbed_cnt += 1
                    result = '干扰中'
                elif len(abnormal_time) > 0 and len(disturbed_time) == 0:
                    self.abnormal_cnt += 1
            self.MysqlClient2.add_testpoint_abnormal_analysis(
                id=id,
                result=result,
                start_time=timestamp_to_localtime(start_time),
                end_time=timestamp_to_localtime(end_time),
                abnormal_time=abnormal_time,
                disturbed_time=disturbed_time,
                cronjob_id=cronjob_id
            )

    def cal_is_data_lost(self, info):
        # 计算测试桩数据是否丢失
        start_time = info[0].get('taTimestamp')
        end_time = info[len(info) - 1].get('taTimestamp')
        # 按照10分钟采集一次数据计算
        expect_cnt = (end_time - start_time) / 1000 / 60 / 10
        actual_cnt = len(info)

        if expect_cnt == 0:
            return True, start_time, end_time
        if actual_cnt * 100 / expect_cnt > 50:
            return False, start_time, end_time
        return True, start_time, end_time

    def cal_abnormal_data(self, info):
        # 计算异常数据
        abnormal_time, disturbed_time = [], []

        is_abnormal, abnormal_start_time, abnormal_end_time = False, None, None
        for f in info:
            if f.get('voff_Revised') < -1.2 or f.get('voff_Revised') > -0.85:
                is_abnormal = True
                abnormal_end_time = timestamp_to_localtime(f.get('taTimestamp'))
                if not abnormal_start_time:
                    abnormal_start_time = timestamp_to_localtime(f.get('taTimestamp'))
                continue
            if abnormal_start_time:
                abnormal_end_time = timestamp_to_localtime(f.get('taTimestamp'))
            if abnormal_start_time and abnormal_end_time:
                # 先取前10条数据，不然太长了
                if len(disturbed_time) < 10:
                    disturbed_time.append({
                        'start_time': abnormal_start_time,
                        'end_time': abnormal_end_time
                    })
                is_abnormal, abnormal_start_time, abnormal_end_time = False, None, None

        if is_abnormal:
            abnormal_time.append({
                'start_time': abnormal_start_time,
                'end_time': abnormal_end_time
            })
        return abnormal_time, disturbed_time

    def get_list(self, page, limit):
        cronjob = self.MysqlClient.get_lastest_cronjob()
        analysis_list = self.MysqlClient.get_testpoint_abnormal_analysis(page, limit, cronjob.id)
        testpoint_ids = []
        for t in analysis_list:
            testpoint_ids.append(t.testpoint_id)
        # testpoint_ids = testpoint_ids[0:1]
        # testpoint_map = MongoDBClient().get_testpoint_info(testpoint_ids)
        result = {
            'total_cnt': cronjob.testpoint_cnt,
            'data_lost_cnt': cronjob.data_lost_cnt,
            'abnormal_cnt': cronjob.abnormal_cnt,
            'disturbed_cnt': cronjob.disturbed_cnt,
            'normal_cnt': cronjob.normal_cnt,
            'testpoint_info': []
        }
        for t in analysis_list:
            result['testpoint_info'].append(
                {
                    'testpoint_id': t.testpoint_id,
                    'analysis_result': t.result,
                    # 'testpoint_data': testpoint_map.get(t.testpoint_id)
                }
            )
        return result
