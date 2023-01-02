from datetime import datetime
import traceback
import json
from application.apps.testpoint.db.dal import DBProxy
from application.apps.testpoint.data_clean import DataClean, CalRef


class Cronjob(object):
    def __init__(self):
        self.MysqlClient = DBProxy()

    def execute(self):
        is_fail, fail_reason = False, ''
        start_time = datetime.now()
        try:
            lastest_cronjob = self.MysqlClient.get_lastest_cronjob_v2()
            if lastest_cronjob:
                new_cronjob_id = lastest_cronjob.id + 1
            else:
                new_cronjob_id = 1
            # 数据清洗
            # data = DataClean().data_clean()
            # 建立ref表
            CalRef().cal_ref()
            # TODO
            # 自学习阈值

            # 干扰识别

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

        self.commit_task(new_cronjob_id, is_fail, fail_reason, '', start_time)

    def commit_task(self, new_cronjob_id, is_fail, fail_reason, data, start_time):
        self.MysqlClient = DBProxy()
        self.MysqlClient.add_device_analysis_cronjob(
            id=new_cronjob_id,
            rule_ids='',
            is_fail=is_fail,
            fail_reason=fail_reason,
            pipe_cnt=0,
            hdwy_cnt=0,
            csz_cnt=0,
            data=data,
            start_time=start_time,
            end_time=datetime.now()
        )
        self.MysqlClient.commit()
