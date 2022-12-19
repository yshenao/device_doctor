from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, DateTime, Integer, Float

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


class DeviceAnalysisCronjob(Base):
    # 定时任务执行记录表
    __tablename__ = 'mem_device_analysis_cronjob'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    rule_ids = Column(String(255), default='', comment='规则id集合')
    is_fail = Column(SmallInteger, default=0, comment='0执行成功 1执行失败')
    fail_reason = Column(Text, comment='如果失败，记录失败原因')
    pipe_cnt = Column(BigInteger, comment='管道数量')
    hdwy_cnt = Column(BigInteger, comment='恒电位仪数量')
    csz_cnt = Column(BigInteger, comment='智能测试桩数量')
    data = Column(Text, comment='附加信息')
    create_time = Column(DateTime, comment='创建时间')
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')


class HdwyMeta(Base):
    # 恒电位仪数据总表
    __tablename__ = 'mem_hdwy_meta'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    hdwy_id = Column(String(255), default='', comment='恒电位仪唯一身份id')
    location_code = Column(String(255), default='', comment='恒电位仪位置编码')
    pipe_id = Column(Integer, comment='恒电位仪管道id')
    locate_mileage = Column(Float, comment='恒电位仪管道里程数')
    collect_time = Column(BigInteger, comment='恒电位仪数据采集时间')
    mode = Column(Integer, comment='恒电位仪运行模式')
    out_volt = Column(Float, comment='恒电位仪输出电压')
    out_curr = Column(Float, comment='恒电位仪输出电流')
    set_value = Column(Float, comment='恒电位仪预设值')
    pot1 = Column(Float, comment='恒电位仪保护电位1')
    pot2 = Column(Float, comment='恒电位仪保护电位2')
    alarm_type = Column(Integer, comment='恒电位仪报警码')
    cSQ = Column(String(255), comment='恒电位仪信号强度')


class CszMeta(Base):
    # 智能测试桩数据总表
    __tablename__ = 'mem_csz_meta'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    csz_id = Column(String(255), default='', comment='智能测试桩唯一身份id')
    location_code = Column(String(255), default='', comment='智能测试桩位置编码')
    pipe_id = Column(Integer, comment='智能测试桩管道id')
    locate_mileage = Column(Float, comment='智能测试桩管道里程数')
    collect_time = Column(BigInteger, comment='智能测试桩数据采集时间')
    von_Revised = Column(Float, comment='智能测试桩通电电位')
    voff_Revised = Column(Float, comment='智能测试桩断电电位')
    cellType = Column(Integer, comment='智能测试桩电池类型')
    battery = Column(Float, comment='智能测试桩电池电压')
    cSQ = Column(String(255), comment='恒电位仪信号强度')
