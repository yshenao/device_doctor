import schedule
from datetime import datetime
from application.apps.testpoint.cronjob import Cronjob


def job():
    print(str(datetime.now()))
    try:
        Cronjob().execute()
    except Exception as e:
        print(e)


# schedule.every().day.at("00:00:00").do(job)
schedule.every(5).seconds.do(job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
