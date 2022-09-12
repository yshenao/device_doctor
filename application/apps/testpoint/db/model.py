from app import db


class TestPointAbnormalAnalysis(db.Model):
    # 智能测试桩-异常分析表
    __tablename__ = 'testpoint_abnormal_analysis'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    testpoint_id = db.Column(db.String(255), default='', comment='测试桩唯一身份id')
    is_data_lost = db.Column(db.SmallInteger, default=0, comment='0数据正常 1数据丢失')
    is_abnormal = db.Column(db.SmallInteger, default=0, comment='0正常 1异常')
    is_disturbed = db.Column(db.SmallInteger, default=0, comment='0未受到干扰 1被干扰')
    data = db.Column(db.Text, default='', comment='异常信息')
    create_time = db.Column(db.DateTime, comment='创建时间')
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    cronjob_id = db.Column(db.BigInteger, comment='定时任务执行id，关联上定时任务表')


class TestPointAbnormalRule(db.Model):
    # 智能测试桩-规则引擎表
    __tablename__ = 'testpoint_analysis_rule'

    rule_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    description = db.Column(db.String(255), default='', comment='规则')
    is_del = db.Column(db.SmallInteger, default=0, comment='1已删除 0未删除')
    create_time = db.Column(db.DateTime, comment='创建时间')


class TestPointAbnormalCronjob(db.Model):
    # 智能测试桩-定时任务执行记录表
    __tablename__ = 'testpoint_analysis_cronjob'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    rule_ids = db.Column(db.String(255), default='', comment='规则id集合')
    is_fail = db.Column(db.SmallInteger, default=0, comment='0执行成功 1执行失败')
    fail_reason = db.Column(db.String(255), default='', comment='如果失败，记录失败原因')
    testpoint_cnt = db.Column(db.BigInteger, comment='测试桩数量')
    abnormal_cnt = db.Column(db.BigInteger, comment='异常测试桩数量')
    disturbed_cnt = db.Column(db.BigInteger, comment='受干扰测试桩数量')
    data = db.Column(db.Text, default='', comment='附加信息')
    create_time = db.Column(db.DateTime, comment='创建时间')
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
