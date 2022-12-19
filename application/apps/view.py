from application.util import timestamp_to_localtime
import pymongo


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
        resp += '<thead><tr>'
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
        resp += '<th>交流试片面积（平方厘米）</th></thead><tbody>'

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
                if attr == 'bsMeasureControlPointId':
                    resp += '<td><a href="96.html">' + str(value) + '</a></td>'
                else:
                    resp += '<td>' + str(value) + '</td>'
        resp += '</tbody></table>'

        mongoclient.close()
        return resp

    def get_data(self):
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
        # }).limit(20)
        })

        mongoclient.close()
        return testpoint_infos


class messagehistoryA(object):
    def get_data(self):
        user = 'anko'
        passwd = 'ANKO.main.610'
        mongoclient = pymongo.MongoClient(host='39.105.189.175', port=27017)
        db = mongoclient.sub
        db.authenticate(user, passwd)
        collection = db.messageHistoryA_In3Month

        messagehistoryA_infos = collection.find({}, {
            '_id': 0,
            'bsSubCompanyId': 1,
            'bsMeasureControlPointId': 1,
            'von2': 1,
            'vac2': 1,
            'von_Revised': 1,
            'voff_Revised': 1,
            'battery': 1,
            'messageReceiveTimestamp': 1,
            'IR': 1,
            'pilotArea': 1,
            'acPilotArea': 1,
            'theState': 1,
            'cSQ': 1,
            'bsPipeId': 1,
            'longitude': 1,
            'latitude': 1,
            'bsLocateMileage': 1,
            'cellType': 1,
            'vac': 1,
            'taTimestamp': 1,
        })

        mongoclient.close()
        return messagehistoryA_infos

    def data(self):
        user = 'anko'
        passwd = 'ANKO.main.610'
        mongoclient = pymongo.MongoClient(host='39.105.189.175', port=27017)
        db = mongoclient.sub
        db.authenticate(user, passwd)
        collection = db.messageHistoryA_In3Month

        mongoclient.close()
        return collection
