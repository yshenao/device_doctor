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
    pages, max_page = get_pages_new(page, total_cnt)
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
    testpoint_id = request.args.get('testpoint_id', '', str)
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
            'data': MongoDBClient().get_single_testpoint_info(testpoint_id).get(testpoint_id, {})
        }
    # return testpoint_analysis_info
    echarts_data = testpoint_analysis_info.get('data')
    return render_template('echarts_by_id.html', echarts_data=list(echarts_data), testpoint_id=testpoint_id)


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
