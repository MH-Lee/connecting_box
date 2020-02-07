from django.db import models
from django.conf import settings
from .choice_dic import choice_dic

# Create your models here.
class RescueUpdateCheck(models.Model):
    recent_date = models.CharField(max_length=10, blank=True, null=True, \
                                   verbose_name='업데이트 날짜')
    update_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.recent_date

    class Meta:
        db_table = 'rescue_update_checker'
        verbose_name = 'Rescue 업데이트 확인'
        verbose_name_plural = 'Rescue 업데이트 확인'


class Rescue(models.Model):
    date = models.CharField(max_length=10, verbose_name="공고일자")
    area = models.CharField(max_length=10, verbose_name="법원위치")
    case_num = models.CharField(max_length=30, verbose_name="사건번호")
    company_name = models.CharField(max_length=128, verbose_name="신청기업")
    company_address = models.CharField(max_length=128, verbose_name="신청기업주소", null=True)
    court = models.CharField(max_length=10, verbose_name="법정")
    subject = models.CharField(max_length=50, verbose_name="문서내용")
    category = models.CharField(max_length=300, verbose_name="카테고리")
    contents = models.TextField(verbose_name='판결문')
    ceo = models.CharField(max_length=30, verbose_name="ceoname", null=True)
    news_title = models.CharField(max_length=200, verbose_name="관련뉴스기사", null=True)
    news_url = models.CharField(max_length=500, verbose_name="관련뉴스 url", null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.case_num

    class Meta:
        db_table = 'rescue'
        verbose_name = '회생법인공고'
        verbose_name_plural = '회생법인공고'


class EmailContents(models.Model):
    title = models.CharField(max_length=200, verbose_name="E-mail 제목")
    contents = models.TextField(verbose_name='E-mail 내용')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                        verbose_name='등록시간')

    def __str__(self):
        return "{}-{}".format(self.title, self.registered_dttm)

    class Meta:
        db_table = 'email-contents'
        verbose_name = 'Email-connecting-letter'
        verbose_name_plural = 'Email-connecting-letter'


# class Tag(models.Model):
#     name = models.CharField(max_length=32,
#                                 verbose_name="태그명")
#     registered_dttm = models.DateTimeField(auto_now_add=True,
#                                             verbose_name='등록시간')

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'item tag'
#         verbose_name = 'Connecting box 태그'
#         verbose_name_plural = 'Connecting box 태그'


class StartUp(models.Model):
    name = models.CharField(max_length=50, verbose_name="기업명", choices=choice_dic)
    item = models.CharField(max_length=50, verbose_name='아이템')
    invest_state = models.CharField(max_length=10, verbose_name='투자단계')
    news_link = models.CharField(max_length=500, verbose_name='링크')

    def __str__(self):
        return '회사이름 : {} 아이템: {} 투자단계: {}'.format(self.name, self.item)


class ProfessorDev(models.Model):
    name = models.CharField(max_length=50, verbose_name="교수명")
    university = models.CharField(max_length=10, verbose_name='소속')
    item = models.CharField(max_length=50, verbose_name='아이템', choices=choice_dic)
    news_link = models.CharField(max_length=500, verbose_name='링크')

    def __str__(self):
        return '교수명 : {} 소속대학:{} 아이템: {}'.format(self.name, self.university, self.item)
    

class FinanceReport(models.Model):
    item = models.CharField(max_length=50, verbose_name='아이템', choices=choice_dic)
    title = models.CharField(max_length=50, verbose_name="제목")
    security_firm = models.CharField(max_length=10, verbose_name='증권사')
    news_link = models.CharField(max_length=500, verbose_name='링크')

    def __str__(self):
        return '제목: {} 증권사: {}'.format(self.title, self.security_firm)


