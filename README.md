# 设备健康诊断平台代码仓库
- 健康诊断云平台，提供阴保设备（恒电位仪，智能测试桩）的异常诊断能力，通过分析设备采集的数据反向推理设备的健康状况。
- 提供一套异常诊断能力的开放接口Open API，供外部服务调用

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
- Mysql & MongoDB Config
```
device_doctor/application/settings/__init__.py
```

## Run Service
### Run Web for develop
```
$ python device_doctor/app.py
```
- 首页:  `http://39.105.108.252:8000/testpoint/abnormal_analysis/list`

### Run Cronjob for develop
```
$ python scripts/testpoint_abnormal_analyze.py
```


