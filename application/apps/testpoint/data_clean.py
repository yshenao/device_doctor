import json
from application.apps.testpoint.db.mongodb import MongoDBClient
from application.apps.testpoint.db.dal import DBProxy


class DataClean(object):
    def __init__(self):
        self.MysqlClient = DBProxy()

    def data_clean(self):
        hdwy_his, hdwy_before_cnt, hdwy_after_cnt = MongoDBClient().get_hdwy_history()
        for h in hdwy_his:
            self.MysqlClient.add_hdwy_meta(
                hdwy_id=h.get('bsMeasureControlPointId'),
                location_code=h.get('locationCode'),
                pipe_id=h.get('bsPipeId'),
                locate_mileage=h.get('bsLocateMileage'),
                collect_time=h.get('bsTimestamp'),
                mode=h.get('operationMode'),
                out_volt=h.get('outVolt'),
                out_curr=h.get('outCurr'),
                set_value=h.get('setValue'),
                pot1=h.get('pot1'),
                pot2=h.get('pot2'),
                alarm_type=h.get('alarmType'),
                cSQ=h.get('cSQ'),
            )

        csz_his, csz_before_cnt, csz_after_cnt = MongoDBClient().get_csz_history()
        for c in csz_his:
            self.MysqlClient.add_csz_meta(
                csz_id=c.get('bsMeasureControlPointId'),
                location_code=c.get('locationCode'),
                pipe_id=c.get('bsPipeId'),
                locate_mileage=c.get('bsLocateMileage'),
                collect_time=c.get('taTimestamp'),
                von_Revised=c.get('von_Revised'),
                voff_Revised=c.get('voff_Revised'),
                cellType=c.get('cellType'),
                battery=c.get('battery'),
                cSQ=c.get('cSQ'),
            )
        self.MysqlClient.commit()
        hdwy_rate = float(hdwy_after_cnt) / hdwy_before_cnt
        csz_rate = float(csz_after_cnt) / csz_before_cnt
        all_after_cnt, all_before_cnt = hdwy_after_cnt + csz_after_cnt, hdwy_before_cnt + csz_before_cnt
        all_rate = float(all_after_cnt) / all_before_cnt
        data = json.dumps({
            'all': {
                'before_cnt': all_before_cnt,
                'after_cnt': all_after_cnt,
                'rate': all_rate
            },
            'hdwy': {
                'before_cnt': hdwy_before_cnt,
                'after_cnt': hdwy_after_cnt,
                'rate': hdwy_rate
            },
            'csz': {
                'before_cnt': csz_before_cnt,
                'after_cnt': csz_after_cnt,
                'rate': csz_rate
            }
        })
        return data


class CalRef(object):
    def __init__(self):
        self.MysqlClient = DBProxy()

    def cal_ref(self):
        hdwy_static, hdwy_locate_map = MongoDBClient().get_hdwy_static()
        csz_static, csz_locate_map = MongoDBClient().get_csz_static()
        pipes = self.MysqlClient.get_pipes()
        for p in pipes:
            print ('管道{}：恒电位仪数量{}，测试桩数量{}'.format(p.tableId, len(hdwy_static.get(p.tableId, [])), len(csz_static.get(p.tableId, []))))
            # 一条管道上没有恒电位仪或者测试桩都属于脏数据，过滤掉
            if not hdwy_static.get(p.tableId) or not csz_static.get(p.tableId):
                continue
            period_map = self.cal_min_max_period_map(hdwy_static.get(p.tableId))
            for c in csz_static.get(p.tableId):
                for hdwy_id, period in period_map.items():
                    if period[0] <= c.get('bsLocateMileage') <= period[1]:
                        print('min:{},value:{},max:{}'.format(period[0], c.get('bsLocateMileage'), period[1]))
                        self.MysqlClient.add_hdwy_csz_ref(
                            hdwy_id=hdwy_id,
                            csz_id=c.get('bsMeasureControlPointId'),
                            pipe_id=p.tableId,
                            hdwy_locate_mileage=hdwy_locate_map[hdwy_id],
                            csz_locate_mileage=csz_locate_map[c.get('bsMeasureControlPointId')],
                        )
        self.MysqlClient.commit()
        return

    def cal_min_max_period_map(self, hdwy):
        hdwy = sorted(hdwy, key=lambda i: i['bsLocateMileage'])
        period_map = {}
        start, end = -1, 10000000
        for i in range(0, len(hdwy)):
            if i+1 >= len(hdwy):
                period_map[hdwy[i].get('bsMeasureControlPointId')] = (start, end)
                continue
            old_start = start
            temp = (hdwy[i].get('bsLocateMileage') + hdwy[i+1].get('bsLocateMileage'))/2
            start = temp
            period_map[hdwy[i].get('bsMeasureControlPointId')] = [old_start, start]
        return period_map
