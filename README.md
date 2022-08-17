# 设备健康诊断平台代码仓库
平台介绍

### 插件:
- Flask Web框架

- PyMySQL 连接Mysql

- pymongo 连接MongoDB


## 安装

运行命令前，确保开发机已经安装好了python、pip等基础包

Install with pip:

```
$ pip install -r requirements.txt
```

## 代码结构
```

```
## 配置信息
- Mysql Config
```
device_doctor/application/settings/__init__.py
```
- MongoDB Config
```
device_doctor/application/apps/view.py   后续会调整
```

## Run Flask
### Run flask for develop
```
$ python device_doctor/app.py
```
In flask, Default port is `5000`

- 首页:  `http://127.0.0.1:5000/`

- Mysql部门数据： `http://127.0.0.1:5000/department/info`

- MongoDB测试桩数据： `http://127.0.0.1:5000/testpoint/info`


