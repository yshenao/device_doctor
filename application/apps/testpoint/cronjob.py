from application.apps.testpoint.analyze import Analyze
from datetime import datetime
import traceback
import json


class Cronjob(Analyze):
    def __init__(self):
        super().__init__()

    def execute(self):
        is_fail, fail_reason = False, ''
        start_time = datetime.now()
        try:
            lastest_cronjob = self.MysqlClient.get_lastest_cronjob()
            if lastest_cronjob:
                new_cronjob_id = lastest_cronjob.id + 1
            else:
                new_cronjob_id = 1
            testpoint_map = self.preload()
            self.analyze(testpoint_map, new_cronjob_id)
        except Exception as e:
            # 失败打印失败信息和堆栈，方便排查问题
            print(e)
            traceback.print_exc()
            is_fail = True
            fail_reason = json.dumps(
                {
                    'err_msg': str(e),
                    'traceback': str(traceback.format_stack())
                }
            )

        end_time = datetime.now()
        self.MysqlClient2.add_testpoint_analysis_cronjob(
            id=new_cronjob_id,
            rule_ids=self.rule_ids,
            is_fail=is_fail,
            fail_reason=fail_reason,
            testpoint_cnt=self.total_cnt,
            data_lost_cnt=self.data_lost_cnt,
            abnormal_cnt=self.abnormal_cnt,
            disturbed_cnt=self.disturbed_cnt,
            normal_cnt=self.normal_cnt,
            data='',
            start_time=start_time,
            end_time=end_time
        )
        self.MysqlClient2.commit()
