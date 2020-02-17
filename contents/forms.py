from django import forms
from .choice_dic import choice_dic, invest_stage

class MailBoard(forms.Form):
    title = forms.CharField(
        error_messages = {
            'required':'제목을 입력해주세요'
        },
        max_length=200, label="제목")
    contents = forms.CharField(
        error_messages = {
            'required':'내용을 입력해주세요'
        },
        widget = forms.Textarea, label = "내용")
    tags = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=choice_dic, label="Tags")


class ProfessorBoard(forms.Form):
    name = forms.CharField(
        error_messages = {
            'required':'이름을 입력해주세요'
        },
        max_length=50, label="교수명")
    university = forms.CharField(
        error_messages = {
            'required':'소속을 입력해주세요'
        },
        max_length=10, label = "소속")
    category = forms.ChoiceField(
        error_messages = {
            'required':'개발 아이템 입력해주세요'
        },
        choices=choice_dic, label = "분류")
    item = forms.CharField(
        error_messages = {
            'required':'개발 아이템 입력해주세요'
        },
        max_length=100, label = "아이템")
    news_link = forms.CharField(
        error_messages = {
            'required':'뉴스링크를 입력해주세요'
        },
        max_length=500, label = "링크")
    tags = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=choice_dic, label="Tags")


class StartUpBoard(forms.Form):
    name = forms.CharField(
        error_messages = {
            'required':'기업명을 입력해주세요'
        },
        max_length=50, label="기업명")
    category = forms.ChoiceField(
        error_messages = {
            'required':'개발 아이템 입력해주세요'
        },
        choices=choice_dic, label = "분류")
    item = forms.CharField(
        error_messages = {
            'required':'개발 아이템 입력해주세요'
        },
        max_length=100, label = "아이템")
    invest_stage = forms.ChoiceField(
        error_messages = {
            'required':'투자단계를 입력해주세요'
        },
        choices=invest_stage, label = "투자단계")
    investment = forms.CharField(max_length=10, empty_value='비공개', label = "투자금액")
    news_link = forms.CharField(
        error_messages = {
            'required':'뉴스링크를 입력해주세요'
        },
        max_length=500, label = "링크")
    tags = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=choice_dic, label="Tags")


class FinanceReportBoard(forms.Form):
    security_firm = forms.CharField(
        error_messages = {
            'required':'증권사을 입력해주세요'
        },
        max_length=50, label="증권사")
    title = forms.CharField(
        error_messages = {
            'required':'제목을 입력해주세요'
        },
        max_length=200, label="제목")
    category = forms.ChoiceField(
        error_messages = {
            'required':'개발 아이템 입력해주세요'
        },
        choices=choice_dic, label = "분류")
    news_link = forms.CharField(
        error_messages = {
            'required':'뉴스링크를 입력해주세요'
        },
        max_length=500, label = "링크")
    tags = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=choice_dic, label="Tags")
