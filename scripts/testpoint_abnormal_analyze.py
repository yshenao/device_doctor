import schedule
from datetime import datetime
from application.apps.testpoint.cronjob import Cronjob


def job():
    print(str(datetime.now()))
    Cronjob().execute()


# schedule.every().day.at("00:00:00").do(job)
schedule.every(2).seconds.do(job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
