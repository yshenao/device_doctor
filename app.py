from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.settings.dev import DevelopmentConfig
from application.settings.production import ProductionConfig
from application.apps.view import DepartmentView, TestPointView

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


if __name__ == '__main__':
    app.run()
