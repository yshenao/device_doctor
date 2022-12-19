from application.apps.testpoint.db.model import TestPointAbnormalAnalysis, TestPointAbnormalCronjob, \
    TestPointAbnormalRule, DeviceAnalysisCronjob, HdwyMeta, CszMeta
import json
from datetime import datetime
from sqlalchemy import create_engine
from application.settings.dev import DevelopmentConfig
from application.settings.production import ProductionConfig
from sqlalchemy.orm import sessionmaker
config = {
    'dev': DevelopmentConfig,
    'production': ProductionConfig
}
Config = config['dev']


class DBProxy(object):
    def __init__(self):
        engine = create_engine(
            Config.SQLALCHEMY_DATABASE_URI,
            encoding='utf-8',
            echo=True,
            pool_recycle=14400,
            pool_timeout=7200
        )
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.records = []

    def begin(self):
        self.session.begin()

    def commit(self):
        batch_size = 100
        records = []
        for record in self.records:
            if len(records) < batch_size:
                records.append(record)
            else:
                self.session.add_all(records)
                self.session.commit()
                records = []

        if len(records) > 0:
            self.session.add_all(records)
            self.session.commit()
        self.records = []

    def close(self):
        self.session.close()

    def add_testpoint_abnormal_analysis(self, id, result, start_time, end_time, abnormal_time, disturbed_time, expect_cnt, actual_cnt, cronjob_id):
        record = TestPointAbnormalAnalysis(
            testpoint_id=id,
            result=result,
            data=json.dumps({
                'abnormal_cnt': len(abnormal_time) if abnormal_time else 0,
                'abnormal_time': abnormal_time or [],
                'disturbed_cnt': len(disturbed_time) if disturbed_time else 0,
                'disturbed_time': disturbed_time or [],
                'expect_cnt': expect_cnt,
                'actual_cnt': actual_cnt,
                'actual_rate': float(actual_cnt) / float(expect_cnt) if expect_cnt else 0.0
            }),
            create_time=datetime.now(),
            start_time=start_time,
            end_time=end_time,
            cronjob_id=cronjob_id
        )
        self.records.append(record)

    def get_testpoint_abnormal_analysis(self, page, limit, cronjob_id):
        query = self.session.query(TestPointAbnormalAnalysis).filter(TestPointAbnormalAnalysis.cronjob_id == cronjob_id).order_by(TestPointAbnormalAnalysis.testpoint_id.asc())
        offset = 0
        if page > 1:
            offset = limit * (page - 1)
        if limit >= 0:
            query = query.limit(limit)
        if offset >= 0:
            query = query.offset(offset)
        records = query.all()
        return records

    def add_testpoint_analysis_cronjob(self, id, rule_ids, is_fail, fail_reason, testpoint_cnt, data_lost_cnt,
                                       abnormal_cnt, disturbed_cnt, normal_cnt, data, start_time, end_time):
        record = TestPointAbnormalCronjob(
            id=id,
            rule_ids=rule_ids,
            is_fail=is_fail,
            fail_reason=fail_reason,
            testpoint_cnt=testpoint_cnt,
            data_lost_cnt=data_lost_cnt,
            abnormal_cnt=abnormal_cnt,
            disturbed_cnt=disturbed_cnt,
            normal_cnt=normal_cnt,
            data=data,
            create_time=datetime.now(),
            start_time=start_time,
            end_time=end_time
        )
        self.records.append(record)

    def get_lastest_cronjob(self):
        records = self.session.query(TestPointAbnormalCronjob).order_by(TestPointAbnormalCronjob.create_time.desc()).limit(1).all()
        if not records:
            return None
        return records[0]

    def get_lastest_cronjob_v2(self):
        records = self.session.query(DeviceAnalysisCronjob).order_by(DeviceAnalysisCronjob.create_time.desc()).limit(1).all()
        if not records:
            return None
        return records[0]

    def get_rule_ids(self):
        return self.session.query(TestPointAbnormalRule).filter(TestPointAbnormalRule.is_del == 0).all()

    def add_hdwy_meta(self, hdwy_id, location_code, pipe_id, locate_mileage, collect_time, mode, out_volt, out_curr, set_value, pot1, pot2, alarm_type, cSQ):
        record = HdwyMeta(
            hdwy_id=hdwy_id,
            location_code=location_code,
            pipe_id=pipe_id,
            locate_mileage=locate_mileage,
            collect_time=collect_time,
            mode=mode,
            out_volt=out_volt,
            out_curr=out_curr,
            set_value=set_value,
            pot1=pot1,
            pot2=pot2,
            alarm_type=alarm_type,
            cSQ=cSQ
        )
        self.records.append(record)

    def add_csz_meta(self, csz_id, location_code, pipe_id, locate_mileage, collect_time, von_Revised, voff_Revised, cellType, battery, cSQ):
        record = CszMeta(
            csz_id=csz_id,
            location_code=location_code,
            pipe_id=pipe_id,
            locate_mileage=locate_mileage,
            collect_time=collect_time,
            von_Revised=von_Revised,
            voff_Revised=voff_Revised,
            cellType=cellType,
            battery=battery,
            cSQ=cSQ
        )
        self.records.append(record)

    def add_device_analysis_cronjob(self, id, rule_ids, is_fail, fail_reason, pipe_cnt, hdwy_cnt, csz_cnt, data, start_time, end_time):
        record = DeviceAnalysisCronjob(
            id=id,
            rule_ids=rule_ids,
            is_fail=is_fail,
            fail_reason=fail_reason,
            pipe_cnt=pipe_cnt,
            hdwy_cnt=hdwy_cnt,
            csz_cnt=csz_cnt,
            data=data,
            create_time=datetime.now(),
            start_time=start_time,
            end_time=end_time
        )
        self.records.append(record)
