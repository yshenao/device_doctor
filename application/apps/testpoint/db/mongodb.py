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
