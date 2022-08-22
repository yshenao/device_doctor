from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from application.settings.dev import DevelopmentConfig
from application.settings.production import ProductionConfig
from application.apps.view import DepartmentView, TestPointView
from application.exception import APIException, Success

app = Flask(__name__)

config = {
    'dev': DevelopmentConfig,
    'production': ProductionConfig
}
Config = config['dev']
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
    app.run()
