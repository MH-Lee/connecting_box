import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import os, sys, glob
import datetime
from ast import literal_eval

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connectingbox.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
import django

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from contents.models import Rescue


def nan_remove(data):
    ret = str(data)
    str1 = 'https://help.naver.com/support/'
    if ret =='nan':
        ret = None
    elif str1 in ret:
        ret = None
    else:
        ret = ret
    return ret

# data = pd.read_excel('./utils/data/rescue_all.xlsx')
# data.head(2)
# data.sort_values(by=['date'], inplace=True)
# data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))

def rescue_send():
    data = pd.read_excel('./utils/data/transfer2.xlsx')
    data.sort_values(by=['date'], inplace=True)
    data['date'] = data['date'].apply(lambda x:str(x).replace('.','-'))
    rescue_list = []
    for i in range(data.shape[0]):
        date = datetime.datetime.strptime(str(data.iloc[i,0]), "%Y-%m-%d").date().strftime("%Y-%m-%d")
        area = data.iloc[i,1]
        case_num = data.iloc[i,2]
        company_name = data.iloc[i,3]
        court = data.iloc[i,4]
        subject = data.iloc[i,5]
        category = data.iloc[i,6]
        contents = data.iloc[i,7]
        ceo = data.iloc[i,8]
        news_title = data.iloc[i,9]
        news_url = data.iloc[i,10]
        address = data.iloc[i,11]
        if i % 200 == 0:
            print(date)
            print(address)
        # writer = User.objects.get(username='admin')
        rescue_obj = Rescue(date=date, area=area, case_num=case_num, company_name=company_name, \
                            court=court, subject=subject, category=category, contents=contents,\
                            news_title=news_title, news_url=news_url, company_address=address, ceo=ceo)
        rescue_list.append(rescue_obj)
    Rescue.objects.bulk_create(rescue_list)
    print('회생법인 업로드')


if __name__ == "__main__":
    print(os.getcwd())
    rescue_send()