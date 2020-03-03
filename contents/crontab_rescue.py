from datetime import datetime, timedelta, date
import os, sys, glob
import time
import platform
import pandas as pd

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connectingbox.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
import django

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from contents.models import Rescue, RescueUpdateCheck
from contents.task_module.rescue_crawler import RescueCrawler

def rescue_send(data):
    data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))
    rescue_list = []
    for i in range(data.shape[0]):
        date = data.loc[i,'date']
        area = data.loc[i,'area']
        case_num = data.loc[i,'case_num']
        company_name = data.loc[i,'company']
        court = data.loc[i,'court']
        subject = data.loc[i,'subject']
        category = data.loc[i,'company_category']
        contents = data.loc[i,'html']
        news_title = data.loc[i,'news_title']
        news_url = data.loc[i,'news_url']
        address = data.loc[i,'address2']
        ceo = data.loc[i,'ceo']
        if i % 200 == 0:
            print(date)
            print(address)
        rescue_obj = Rescue(date=date, area=area, case_num=case_num, company_name=company_name, \
                            court=court, subject=subject, category=category, contents=contents,\
                            news_title=news_title, news_url=news_url, company_address=address, ceo=ceo)
        rescue_list.append(rescue_obj)
    Rescue.objects.bulk_create(rescue_list)
    print('회생법인 업로드')

def rescue_data_send():
    start_time = time.time()
    print(os.getcwd())
    path = os.getcwd()
    if platform.system() == 'Linux':
        # path = '/home/ubuntu/sunbo_django/information/task_module'
        backup_filename = path + "/contents/task_module/backup/rescue/" + datetime.today().strftime("%Y%m%d")+ "_rescue_court.csv"
    else:
        backup_filename = path + "\\contents\\task_module\\backup\\rescue\\" + datetime.today().strftime("%Y%m%d")+ "_rescue_court.csv"

    r = RescueCrawler()
    print("data_update")
    rescue_data = r.rescue_crawling()
    rescue_data.fillna('None', inplace=True)
    rescue_data.sort_values('date', ascending=False, inplace=True)
    rescue_data.to_csv(backup_filename,  encoding = "utf-8-sig", header=True, index=False)
    rescue_send(rescue_data)
    RescueUpdateCheck.objects.all().delete()
    uc_obj = RescueUpdateCheck(recent_date=pd.to_datetime(rescue_data['date'])[0].date().strftime('%Y-%m-%d'))
    uc_obj.save()
    print("data_update complete")
    end_time = time.time()
    print(end_time - start_time)


if __name__ == "__main__":
    rescue_data_send()