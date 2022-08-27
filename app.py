from flask import Flask, Blueprint,request, render_template, redirect,abort
from flask_sqlalchemy import SQLAlchemy
from application.settings.dev import DevelopmentConfig
from application.settings.production import ProductionConfig
from application.apps.view import DepartmentView, TestPointView
from application.exception import APIException, Success

home_page = Blueprint('home_page',__name__,template_folder='templates')

@home_page.route('/index.html')
def get_home_page():
    try:
        data = TestPointView().get_front_20()
        return render_template('index.html',data=data)
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
app.register_blueprint(home_page,url_prefix='/')
db = SQLAlchemy(app)

@app.route('/96')
def hello_world():
    return render_template('96.html')
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# @app.route('/department/info')
# def department_info():
#     return DepartmentView().get_all()
#
#
# @app.route('/testpoint/info')
# def testpoint_info():
#     return TestPointView().get_front_20()


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
    app.run()
