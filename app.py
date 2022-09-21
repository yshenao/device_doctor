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


@app.route('/table')
def table():
    page = request.args.get('page', 1, int)
    pages, max_page = get_pages(page)
    per_page = 20
    if page == 1:
        # 请求为默认的第一页
        data = messagehistoryA().get_data().limit(per_page)
        active_page = 1
    else:
        data = messagehistoryA().get_data().skip((page-1)*per_page).limit(per_page)
        active_page = page
    return render_template('table.html', data=list(data), pages=pages, active_page=active_page, max_page=max_page)


@app.route('/testpoint/abnormal_analysis/list')
def get_testpoint_analysis_list():
    page = request.args.get('page', 1, int)
    limit = request.args.get('limit', 20, int)
    return {
        'code': 200,
        'msg': 'success',
        'data': Analyze().get_list(page, limit)
    }


@app.route('/testpoint/abnormal_analysis/info')
def get_testpoint_analysis_info():
    testpoint_id = request.args.get('testpoint_id', '', str)
    if not testpoint_id:
        return {
            'code': 200,
            'msg': 'id缺失',
            'data': {}
        }

    return {
        'code': 200,
        'msg': 'success',
        'data': MongoDBClient().get_single_testpoint_info(testpoint_id)
    }


def get_pages(page, index=3):
    count = messagehistoryA().get_data().count()
    if (count % 20) != 0:
        pages = int(count // 20) + 1
    else:
        pages = int(count / 20)
    pages = list(i for i in range(1, pages + 1))
    # print(pages)
    max_page = max(pages)
    if page >= (max(pages)-index):
        pages_ = pages[page-2:page+1]
    else:
        pages_ = (pages[page-1:page+2])
    if len(pages_)<3:
        pages_ = pages[-3:]
    return pages_, max_page


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
