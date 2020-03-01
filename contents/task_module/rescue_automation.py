from contents.task_module.rescue_crawler import RescueCrawler
from datetime import datetime
import os

r = RescueCrawler()
final_result = r.rescue_crawling()
final_result.fillna('None', inplace=True)
path = os.getcwd()
final_result.to_csv(path + '/information/task_module/backup/rescue/' + datetime.today().strftime("%Y%m%d")+'_rescue_court.csv',  encoding = "utf-8-sig", header=True, index=False)
