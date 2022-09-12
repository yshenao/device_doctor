from app import db


class Department(db.Model):
    __tablename__ = 'department'

    tableId = db.Column(db.BigInteger, primary_key=True, comment='主键ID')
    theName = db.Column(db.String(255), default=None, comment='部门名称')
    subCompanyEx = db.Column(db.BigInteger, default=None, comment='所属子站')
    theState = db.Column(db.Integer, default=None, comment='状态可用')
    createDatetimeStamp = db.Column(db.BigInteger, default=None, comment='创建时间')
    deleteReason = db.Column(db.String(255), default=None, comment='删除原因')
    isSuperDepartment = db.Column(db.String(255), default=None, comment='是否为管理中心')
    orderNumber = db.Column(db.Integer, default=None, comment='管理处排序')
    reportNumber = db.Column(db.Integer, default=None, comment='自动报告排序')
