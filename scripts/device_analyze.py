import schedule
from datetime import datetime
from application.apps.testpoint.cronjob_v2 import Cronjob


def job():
    print('Cronjob execute begin')
    print(str(datetime.now()))
    try:
        Cronjob().execute()
    except Exception as e:
        print('Cronjob execute fail error {}'.format(e))
        return
    print('Cronjob execute success')


# schedule.every().day.at("00:00:00").do(job)
schedule.every(5).seconds.do(job)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
