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
