from flask import Flask, Blueprint,request, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from application.settings.dev import DevelopmentConfig
from application.settings.production import ProductionConfig
from application.apps.view import DepartmentView, TestPointView, messagehistoryA
from application.exception import APIException, Success
from application.apps.testpoint.analyze import Analyze
from application.apps.testpoint.db.mongodb import MongoDBClient

home_page = Blueprint('home_page',__name__,template_folder='templates')


@home_page.route('/index.html')
def get_home_page():
    try:
        data = TestPointView().get_front_20()
        return render_template('index.html', data=data)
    except TemplateNotFound:
        abort(404)


@home_page.route('/96.html')
def get_96_url():
    try:
        return render_template('96.html')
    except TemplateNotFound:
        abort(404)


app = Flask(__name__)

config = {
    'dev': DevelopmentConfig,
    'production': ProductionConfig
}
Config = config['dev']
app.config.from_object(Config)
app.register_blueprint(home_page, url_prefix='/')
db = SQLAlchemy(app)


@app.route('/96')
def hello_world():
    return render_template('96.html')


@app.route('/testpoint/abnormal_analysis/list')
def get_testpoint_analysis_list():
    page = request.args.get('page', 1, int)
    limit = request.args.get('limit', 20, int)
    list = {
        'code': 200,
        'msg': 'success',
        'data': Analyze().get_list(page, limit)
    }
    # return list

    list_data = list.get('data')
    html_data = list_data.get('testpoint_info') #返回list

    total_cnt = list_data.get('total_cnt')
    pages, max_page = get_pages_new(page,total_cnt)
    active_page = page

    return render_template('abnormal_analysis_list.html', list_data=list_data, html_data=html_data, pages=pages, active_page=active_page, max_page=max_page)
def get_pages_new(page, total_cnt, index=5):
    count = total_cnt
    if (count % 20) != 0:
        pages = int(count // 20) + 1
    else:
        pages = int(count / 20)
    pages = list(i for i in range(1, pages + 1))
    # print(pages)
    max_page = max(pages)
    if page >= (max(pages)-index):
        pages_ = pages[page-3:page+2]
    else:
        pages_ = (pages[page-1:page+4])
    if len(pages_)<5:
        pages_ = pages[-5:]
    # print(pages_)
    return pages_, max_page


@app.route('/testpoint/abnormal_analysis/info')
def get_testpoint_analysis_info():
    main_page = request.args.get('page', '', int)
    testpoint_id = request.args.get('testpoint_id', '', str)
    expect_cnt = request.args.get('expect_cnt', '', float)
    actual_cnt = request.args.get('actual_cnt', '', float)
    actual_rate = request.args.get('actual_rate', '', float)
    result = request.args.get('result', '', str)
    if not testpoint_id:
        testpoint_analysis_info = {
            'code': 200,
            'msg': 'id缺失',
            'data': {}
        }
    else:
        testpoint_analysis_info = {
            'code': 200,
            'msg': 'success',
            'data': MongoDBClient().get_single_testpoint_info(testpoint_id)
        }
    # return testpoint_analysis_info
    echarts_data = testpoint_analysis_info.get('data')

    # 获取该测试桩的所有干扰周期
    testpoint_info_ls = Analyze().get_list(main_page, 20).get('testpoint_info')  #返回list
    for each in testpoint_info_ls:                                         #遍历list
        if each.get('testpoint_id') == testpoint_id:                       #找到对应id的数据
            disturbed_time_ls = each.get('disturbed_time')                 #返回list
    disturbed_section = ''
    for each in disturbed_time_ls:  #遍历list，把start—_time和end_time一个一个加到字符串里
        if each == disturbed_time_ls[-1]:
            disturbed_section = disturbed_section + each.get('start_time') + '-' + each.get('end_time')
        else:
            disturbed_section = disturbed_section + each.get('start_time') + '-' + each.get('end_time') + '、'

    start_time = echarts_data[0].get('taTimestamp')
    end_time = echarts_data[-1].get('taTimestamp')
    last_voff_revised = echarts_data[-1].get('voff_Revised')
    if result == '数据丢失':
        high_or_low = '低'
        voff_reasonable = 'None'
        disturbed_or_not = 'None'
    elif result == '正常':
        high_or_low = '高'
        voff_reasonable = '位于合理范围内判定为【正常】'
        disturbed_or_not = 'None'
    elif result == '干扰中':
        high_or_low = '高'
        voff_reasonable = '未在合理范围内。'
        disturbed_or_not = '在' + disturbed_section + '周期内均发生过类似的干扰，从而导致了断电电位数据的抖动，判定是干扰导致【干扰中】。'
    else:  #异常
        high_or_low = '高'
        voff_reasonable = '未在合理范围内。'
        disturbed_or_not = '该测试桩此前一直未发生过干扰，判定是非干扰因素导致的【异常】'
    process = {
        'data_collect': '当前测试桩采集周期为' + start_time + '-' + end_time + \
                        '，按照10分钟设备采集一次数据的规律，应当回传数据量为' + str(int(expect_cnt)) + \
                        '，实际回传数据量为' + str(int(actual_cnt)) + '，采集率为' + str(int(actual_rate)*100) + \
                        '%，' + high_or_low + '于系统设置阈值50%，判定设备采集数据正常。',
        'voff': '最后一次采集时间：' + end_time + '，采集到的断电电位数据：' + str(last_voff_revised) + 'V，' +
                voff_reasonable + '\n(国家标准：断电电位正常范围为-1.2~-0.85V，其中<-1.2V属于欠保护，>-0.85V属于过保护，判定为异常)',
        'disturbed': '通过分析历史数据，' + disturbed_or_not
    }

    return render_template('echarts_by_id.html', process=process, result=result, echarts_data=list(echarts_data), testpoint_id=testpoint_id)


@app.route('/department/info')
def department_info():
    return DepartmentView().get_all()


@app.route('/testpoint/info')
def testpoint_info():
    return TestPointView().get_front_20()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] != Config.DEVICE_PLATFORM_ADMIN_USER or request.form['password'] != Config.DEVICE_PLATFORM_ADMIN_PASSWORD:
            raise APIException('用户名或者密码不正确，请重新输入')
        return {
            'code': 200,
            'msg': 'success'
        }
    return render_template('login.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html', )


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
