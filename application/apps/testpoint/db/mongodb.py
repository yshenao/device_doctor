from application.settings import Config
import pymongo
from application.util import timestamp_to_localtime, deduplication


class MongoDBClient(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=Config.MONGODB_IP,
            port=Config.MONGODB_PORT
        )
        self.db = self.client.get_database(Config.MONGODB_NAME)
        self.db.authenticate(Config.MONGODB_USER, Config.MONGODB_PASSWORD)
        self.collection = self.db.get_collection('messageHistoryA_In3Month')

    def close(self):
        self.client.close()

    def get_all_testpoint_info(self):
        self.collection = self.db.get_collection('messageHistoryA_In3Month')
        all_cnt = self.collection.count()
        print('原始数据总量：{}'.format(all_cnt))
        select_fields = {
            '_id': 0,
            # 'bsSubCompanyId': 1,
            'bsMeasureControlPointId': 1,
            # 'von2': 1,
            # 'vac2': 1,
            # 'von_Revised': 1,
            'voff_Revised': 1,
            # 'battery': 1,
            # 'messageReceiveTimestamp': 1,
            # 'IR': 1,
            # 'pilotArea': 1,
            # 'acPilotArea': 1,
            # 'theState': 1,
            # 'cSQ': 1,
            # 'bsPipeId': 1,
            # 'longitude': 1,
            # 'latitude': 1,
            # 'bsLocateMileage': 1,
            # 'cellType': 1,
            # 'vac': 1,
            'taTimestamp': 1,
        }
        self.collection.aggregate(
            [
                {
                    '$sort': {
                        'bsMeasureControlPointId': 1,  # 1表示升序，-1表示降序
                        'taTimestamp': 1
                    }
                }
            ], allowDiskUse=True
        )
        testpoint_infos = self.collection.find({}, select_fields, no_cursor_timeout=True)
        # testpoint_infos = testpoint_infos.limit(100)
        # testpoint_infos = self.collection.find({}, select_fields).sort(
        #     [
        #         ('taTimestamp', 1),
        #         ('bsMeasureControlPointId', 1),
        #     ]
        # )
        return testpoint_infos

    def get_testpoint_info(self, ids):
        self.collection = self.db.get_collection('messageHistoryA_In3Month')
        select_fields = {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'voff_Revised': 1,
            'taTimestamp': 1,
        }
        testpoint_infos = self.collection.find(
            {
                'bsMeasureControlPointId':
                    {
                        '$in': ids
                    }
            }, select_fields
        ).sort(
            [
                ('taTimestamp', 1),
            ]
        )

        testpoint_map = {}
        for t in testpoint_infos:
            if not testpoint_map.get(t.get('bsMeasureControlPointId')):
                testpoint_map[t.get('bsMeasureControlPointId')] = [
                    {
                        'taTimestamp': timestamp_to_localtime(t.get('taTimestamp')),
                        'voff_Revised': t.get('voff_Revised'),
                        'unit': 'V'
                    }
                ]
                continue
            testpoint_map[t.get('bsMeasureControlPointId')].append(
                {
                    'taTimestamp': timestamp_to_localtime(t.get('taTimestamp')),
                    'voff_Revised': t.get('voff_Revised'),
                    'unit': 'V'
                }
            )
        result = {}
        for id, value in testpoint_map.items():
            result[id] = deduplication(value)
        return testpoint_map

    def get_single_testpoint_info(self, testpoint_id):
        return self.get_testpoint_info([testpoint_id])

    def get_hdwy_history(self):
        self.collection = self.db.get_collection('messageHistoryB_In3Month')
        origin_cnt = self.collection.count()
        select_fields = {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'locationCode': 1,
            'bsPipeId': 1,
            'bsLocateMileage': 1,
            'bsTimestamp': 1,
            'operationMode': 1,
            'outVolt': 1,
            'outCurr': 1,
            'setValue': 1,
            'pot1': 1,
            'pot2': 1,
            'alarmType': 1,
            'cSQ': 1,
        }
        self.collection.aggregate([], allowDiskUse=True)
        hdwy_infos = self.collection.find({}, select_fields, no_cursor_timeout=True)
        hdwy_infos = hdwy_infos.limit(100)

        deduplication_map = {}
        result = []
        duplication_cnt = 0
        non_duplication_cnt = 0
        for h in hdwy_infos:
            if not h.get('bsMeasureControlPointId') or not h.get('bsTimestamp'):
                # 去空
                continue
            key = str(h.get('bsMeasureControlPointId')) + str(h.get('bsTimestamp'))
            if key in deduplication_map.keys():
                if h.get('setValue') == deduplication_map[key]:
                    duplication_cnt = duplication_cnt + 1
                    # print('duplication_cnt hdwy id:{}, time:{}'.format(h.get('bsMeasureControlPointId'), h.get('bsTimestamp')))
                else:
                    non_duplication_cnt = non_duplication_cnt + 1
                    # print('non_duplication_cnt hdwy id:{}, time:{}'.format(h.get('bsMeasureControlPointId'), h.get('bsTimestamp')))
                # 去重
                continue
            result.append({
                'bsMeasureControlPointId': h.get('bsMeasureControlPointId'),
                'locationCode': h.get('locationCode'),
                'bsPipeId': h.get('bsPipeId'),
                'bsLocateMileage': h.get('bsLocateMileage'),
                'bsTimestamp': h.get('bsTimestamp'),
                'operationMode': h.get('operationMode'),
                'outVolt': h.get('outVolt'),
                'outCurr': h.get('outCurr'),
                'setValue': h.get('setValue'),
                'pot1': h.get('pot1'),
                'pot2': h.get('pot2'),
                'alarmType': h.get('alarmType'),
                'cSQ': h.get('cSQ'),
            })
            deduplication_map[key] = h.get('setValue')
        print("get_hdwy_history duplication_cnt: {}, non_duplication_cnt: {}".format(duplication_cnt, non_duplication_cnt))
        return result, origin_cnt, len(result)

    def get_csz_history(self):
        self.collection = self.db.get_collection('messageHistoryA_In3Month')
        origin_cnt = self.collection.count()
        select_fields = {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'locationCode': 1,
            'bsPipeId': 1,
            'bsLocateMileage': 1,
            'taTimestamp': 1,
            'von_Revised': 1,
            'voff_Revised': 1,
            'cellType': 1,
            'battery': 1,
            'cSQ': 1,
        }
        self.collection.aggregate([], allowDiskUse=True)
        csz_infos = self.collection.find({}, select_fields, no_cursor_timeout=True)
        csz_infos = csz_infos.limit(100)

        deduplication_map = {}
        result = []
        duplication_cnt = 0
        non_duplication_cnt = 0
        for c in csz_infos:
            if not c.get('bsMeasureControlPointId') or not c.get('taTimestamp'):
                # 去空
                continue
            key = str(c.get('bsMeasureControlPointId')) + str(c.get('taTimestamp'))
            if key in deduplication_map.keys():
                if c.get('voff_Revised') == deduplication_map[key]:
                    duplication_cnt = duplication_cnt + 1
                    # print('duplication_cnt csz id:{}, time:{}'.format(c.get('bsMeasureControlPointId'), c.get('taTimestamp')))
                else:
                    non_duplication_cnt = non_duplication_cnt + 1
                    # print('non_duplication_cnt csz id:{}, time:{}'.format(c.get('bsMeasureControlPointId'), c.get('taTimestamp')))
                # 去重
                continue
            result.append({
                'bsMeasureControlPointId': c.get('bsMeasureControlPointId'),
                'locationCode': c.get('locationCode'),
                'bsPipeId': c.get('bsPipeId'),
                'bsLocateMileage': c.get('bsLocateMileage'),
                'taTimestamp': c.get('taTimestamp'),
                'von_Revised': c.get('von_Revised'),
                'voff_Revised': c.get('voff_Revised'),
                'cellType': c.get('cellType'),
                'battery': c.get('battery'),
                'cSQ': c.get('cSQ'),
            })
            deduplication_map[key] = c.get('voff_Revised')
        print("get_csz_history duplication_cnt: {}, non_duplication_cnt: {}".format(duplication_cnt, non_duplication_cnt))
        return result, origin_cnt, len(result)

    def get_hdwy_static(self):
        # 获取恒电位仪静态数据
        self.collection = self.db.get_collection('terminalB_HDWY')
        select_fields = {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'locationCode': 1,
            'bsPipeId': 1,
            'bsLocateMileage': 1,
            'bsTimestamp': 1,
            'setValue': 1,
        }
        self.collection.aggregate([], allowDiskUse=True)
        hdwy_infos = self.collection.find({}, select_fields, no_cursor_timeout=True)

        deduplication_map = {}
        result = {}
        duplication_cnt = 0
        non_duplication_cnt = 0
        locate_map = {}
        for h in hdwy_infos:
            if not h.get('bsMeasureControlPointId') or not h.get('bsTimestamp'):
                # 去空
                continue
            key = str(h.get('bsMeasureControlPointId')) + str(h.get('bsTimestamp'))
            if key in deduplication_map.keys():
                if h.get('setValue') == deduplication_map[key]:
                    duplication_cnt = duplication_cnt + 1
                    # print('duplication_cnt hdwy id:{}, time:{}'.format(h.get('bsMeasureControlPointId'), h.get('bsTimestamp')))
                else:
                    non_duplication_cnt = non_duplication_cnt + 1
                    # print('non_duplication_cnt hdwy id:{}, time:{}'.format(h.get('bsMeasureControlPointId'), h.get('bsTimestamp')))
                # 去重
                continue
            deduplication_map[key] = h.get('setValue')
            info = {
                'bsMeasureControlPointId': h.get('bsMeasureControlPointId'),
                'bsPipeId': h.get('bsPipeId'),
                'bsLocateMileage': h.get('bsLocateMileage'),
            }
            if result.get(h.get('bsPipeId')):
                result[h.get('bsPipeId')].append(info)
            else:
                result[h.get('bsPipeId')] = [info]
            locate_map[h.get('bsMeasureControlPointId')] = h.get('bsLocateMileage')
        print("get_hdwy_static duplication_cnt: {}, non_duplication_cnt: {}".format(duplication_cnt, non_duplication_cnt))
        return result, locate_map

    def get_csz_static(self):
        self.collection = self.db.get_collection('terminalA_YBSB')
        select_fields = {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'locationCode': 1,
            'bsPipeId': 1,
            'bsLocateMileage': 1,
            'taTimestamp': 1,
            'voff_Revised': 1,
        }
        self.collection.aggregate([], allowDiskUse=True)
        csz_infos = self.collection.find({}, select_fields, no_cursor_timeout=True)

        deduplication_map = {}
        result = {}
        duplication_cnt = 0
        non_duplication_cnt = 0
        locate_map = {}
        for c in csz_infos:
            if not c.get('bsMeasureControlPointId') or not c.get('taTimestamp'):
                # 去空
                continue
            key = str(c.get('bsMeasureControlPointId')) + str(c.get('taTimestamp'))
            if key in deduplication_map.keys():
                if c.get('voff_Revised') == deduplication_map[key]:
                    duplication_cnt = duplication_cnt + 1
                    # print('duplication_cnt csz id:{}, time:{}'.format(c.get('bsMeasureControlPointId'), c.get('taTimestamp')))
                else:
                    non_duplication_cnt = non_duplication_cnt + 1
                    # print('non_duplication_cnt csz id:{}, time:{}'.format(c.get('bsMeasureControlPointId'), c.get('taTimestamp')))
                # 去重
                continue
            deduplication_map[key] = c.get('voff_Revised')
            info = {
                'bsMeasureControlPointId': c.get('bsMeasureControlPointId'),
                'bsPipeId': c.get('bsPipeId'),
                'bsLocateMileage': c.get('bsLocateMileage'),
            }
            if result.get(c.get('bsPipeId')):
                result[c.get('bsPipeId')].append(info)
            else:
                result[c.get('bsPipeId')] = [info]
            locate_map[c.get('bsMeasureControlPointId')] = c.get('bsLocateMileage')
        print("get_csz_static duplication_cnt: {}, non_duplication_cnt: {}".format(duplication_cnt, non_duplication_cnt))
        return result, locate_map
