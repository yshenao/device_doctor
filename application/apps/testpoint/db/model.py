from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, DateTime

Base = declarative_base()


class TestPointAbnormalAnalysis(Base):
    # 智能测试桩-异常分析表
    __tablename__ = 'testpoint_abnormal_analysis'

    id = Column(BigInteger, primary_key=True, comment='主键ID')
    testpoint_id = Column(String(255), default='', comment='测试桩唯一身份id')
    # is_data_lost = Column(SmallInteger, default=0, comment='0数据正常 1数据丢失')
    # is_abnormal = Column(SmallInteger, default=0, comment='0正常 1异常')
    # is_disturbed = Column(SmallInteger, default=0, comment='0未受到干扰 1被干扰')
    result = Column(String(255), default='', comment='诊断结果包括正常、干扰中、异常、数据丢失')
    data = Column(Text, comment='异常信息')
    create_time = Column(DateTime, comment='创建时间')
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')
    cronjob_id = Column(BigInteger, comment='定时任务执行id，关联上定时任务表')


class TestPointAbnormalRule(Base):
    # 智能测试桩-规则引擎表
    __tablename__ = 'testpoint_analysis_rule'

    rule_id = Column(BigInteger, primary_key=True, comment='主键ID')
    description = Column(String(255), default='', comment='规则')
    is_del = Column(SmallInteger, default=0, comment='1已删除 0未删除')
    create_time = Column(DateTime, comment='创建时间')


class TestPointAbnormalCronjob(Base):
    # 智能测试桩-定时任务执行记录表
    __tablename__ = 'testpoint_analysis_cronjob'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    rule_ids = Column(String(255), default='', comment='规则id集合')
    is_fail = Column(SmallInteger, default=0, comment='0执行成功 1执行失败')
    fail_reason = Column(Text, comment='如果失败，记录失败原因')
    testpoint_cnt = Column(BigInteger, comment='测试桩数量')
    data_lost_cnt = Column(BigInteger, comment='数据丢失测试桩数量')
    abnormal_cnt = Column(BigInteger, comment='异常测试桩数量')
    disturbed_cnt = Column(BigInteger, comment='干扰中测试桩数量')
    normal_cnt = Column(BigInteger, comment='正常测试桩数量')
    data = Column(Text, comment='附加信息')
    create_time = Column(DateTime, comment='创建时间')
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')
