from application.util import timestamp_to_localtime
import pymongo

class DepartmentView(object):
    def get_all(self):
        from application.apps.model import Department
        resp = '<table border="1">'
        resp += '<tr>'
        resp += '<th>id</th>'
        resp += '<th>部门名称</th>'
        resp += '<th>所属子站</th>'
        resp += '<th>状态可用</th>'
        resp += '<th>创建时间</th>'
        resp += '<th>删除原因</th>'
        resp += '<th>是否为管理中心</th>'
        resp += '<th>管理处排序</th>'
        resp += '<th>自动报告排序</th>'

        data = Department.query.all()
        for d in data:
            resp += '<tr>'
            resp += '<td>' + str(d.tableId) + '</td>'
            resp += '<td>' + d.theName + '</td>'
            resp += '<td>' + str(d.subCompanyEx) + '</td>'
            resp += '<td>' + str(d.theState) + '</td>'
            resp += '<td>' + timestamp_to_localtime(d.createDatetimeStamp) + '</td>'
            delete_reason = d.deleteReason or ''
            resp += '<td>' + delete_reason + '</td>'
            is_super_department = d.isSuperDepartment or ''
            resp += '<td>' + is_super_department + '</td>'
            order_number = d.orderNumber or ''
            resp += '<td>' + str(order_number) + '</td>'
            report_number = d.reportNumber or ''
            resp += '<td>' + str(report_number) + '</td>'
        resp += '</table>'

        return resp


class TestPointView(object):
    def get_front_20(self):
        user = 'anko'
        passwd = 'ANKO.main.610'
        mongoclient = pymongo.MongoClient(host='39.105.189.175', port=27017)
        db = mongoclient.sub
        db.authenticate(user, passwd)
        collection = db.testPointA_CSZ

        testpoint_infos = collection.find({}, {
            '_id': 0,
            'bsMeasureControlPointId': 1,
            'taTimestamp': 1,
            'address': 1,
            'locationDes': 1,
            'von_Revised': 1,
            'voff_Revised': 1,
            'battery': 1,
            'cellType': 1,
            'von2': 1,
            'pilotArea': 1,
            'vac2': 1,
            'acPilotArea': 1,
        }).limit(20)

        resp = '<table border="1">'
        resp += '<tr>'
        resp += '<th>id</th>'
        resp += '<th>地址</th>'
        resp += '<th>位置描述</th>'
        resp += '<th>采集时间</th>'
        resp += '<th>通电电压（V）</th>'
        resp += '<th>断电电压（V）</th>'
        resp += '<th>电池电压(v)</th>'
        resp += '<th>电池类型</th>'
        resp += '<th>直流电流（mA）</th>'
        resp += '<th>极化试片面积（平方厘米）</th>'
        resp += '<th>交流电流（mA）</th>'
        resp += '<th>交流试片面积（平方厘米）</th>'

        for t in testpoint_infos:
            resp += '<tr>'
            attrs = [
                'bsMeasureControlPointId',
                'address',
                'locationDes',
                'taTimestamp',
                'von_Revised',
                'voff_Revised',
                'battery',
                'cellType',
                'von2',
                'pilotArea',
                'vac2',
                'acPilotArea',
            ]

            for attr in attrs:
                value = t.get(attr, '')
                if attr == 'taTimestamp':
                    value = timestamp_to_localtime(value)
                resp += '<td>' + str(value) + '</td>'
        resp += '</table>'

        mongoclient.close()
        return resp
