from app import db
from application.apps.testpoint.db.model import TestPointAbnormalAnalysis, TestPointAbnormalCronjob, \
    TestPointAbnormalRule
import json


class DBProxy(object):
    def commit(self):
        db.session.commit()

    def add_testpoint_abnormal_analysis(self, id, is_data_lost, start_time, end_time, abnormal_time, disturbed_time,
                                        cronjob_id):
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
            start_time=start_time,
            end_time=end_time,
            cronjob_id=cronjob_id
        )
        db.session.add(record)

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
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(record)

    def get_lastest_cronjob_id(self):
        records = TestPointAbnormalCronjob.query.order_by(TestPointAbnormalCronjob.create_time.desc()).limit(1).all()
        if not records:
            return 0
        return records[0].id

    def get_rule_ids(self):
        return TestPointAbnormalRule.query.filter(TestPointAbnormalRule.is_del == 0).all()
