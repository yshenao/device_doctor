from application.apps.testpoint.db.model import TestPointAbnormalAnalysis, TestPointAbnormalCronjob, \
    TestPointAbnormalRule
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

    def add_testpoint_abnormal_analysis(self, id, is_data_lost, start_time, end_time, abnormal_time, disturbed_time, cronjob_id):
        record = TestPointAbnormalAnalysis(
            testpoint_id=id,
            is_data_lost=is_data_lost,
            is_abnormal=len(abnormal_time) > 0,
            is_disturbed=len(disturbed_time) > 0,
            data=json.dumps({
                'abnormal_cnt': len(abnormal_time),
                'abnormal_time': abnormal_time,
                'disturbed_cnt': len(disturbed_time),
                'disturbed_time': disturbed_time,
            }),
            create_time=datetime.now(),
            start_time=start_time,
            end_time=end_time,
            cronjob_id=cronjob_id
        )
        self.records.append(record)

    def add_testpoint_analysis_cronjob(self, id, rule_ids, is_fail, fail_reason, testpoint_cnt, abnormal_cnt,
                                       disturbed_cnt, data, start_time, end_time):
        record = TestPointAbnormalCronjob(
            id=id,
            rule_ids=rule_ids,
            is_fail=is_fail,
            fail_reason=fail_reason,
            testpoint_cnt=testpoint_cnt,
            abnormal_cnt=abnormal_cnt,
            disturbed_cnt=disturbed_cnt,
            data=data,
            create_time=datetime.now(),
            start_time=start_time,
            end_time=end_time
        )
        self.records.append(record)

    def get_lastest_cronjob_id(self):
        records = self.session.query(TestPointAbnormalCronjob).order_by(TestPointAbnormalCronjob.create_time.desc()).limit(1).all()
        if not records:
            return 0
        return records[0].id

    def get_rule_ids(self):
        return self.session.query(TestPointAbnormalRule).filter(TestPointAbnormalRule.is_del == 0).all()
