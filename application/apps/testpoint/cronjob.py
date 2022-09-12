from application.apps.testpoint.analyze import Analyze
from datetime import datetime


class Cronjob(Analyze):
    def __init__(self):
        super(Analyze, self).__init__()

    def execute(self):
        is_fail, fail_reason = False, ''
        start_time = datetime.now()
        try:
            lastest_cronjob_id = self.MysqlClient.get_lastest_cronjob_id()
            new_cronjob_id = lastest_cronjob_id + 1
            self.process(new_cronjob_id)
        except Exception as e:
            print(e)
            is_fail, fail_reason = True, str(e)
        end_time = datetime.now()

        self.MysqlClient.add_testpoint_analysis_cronjob(
            id=new_cronjob_id,
            rule_ids=self.rule_ids,
            is_fail=is_fail,
            fail_reason=fail_reason,
            testpoint_cnt=self.total_cnt,
            abnormal_cnt=self.abnormal_cnt,
            disturbed_cnt=self.disturbed_cnt,
            data='',
            start_time=start_time,
            end_time=end_time
        )

        self.MysqlClient.commit()
