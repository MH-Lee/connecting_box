from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import TemplateView, ListView
from django.views.decorators.http import require_POST
from .forms import MailBoard, StartUpBoard, ProfessorBoard, FinanceReportBoard
from .models import Rescue, EmailContents, ProfessorDev, FinanceReport, StartUp, Tag
from accounts.models import User
import pandas as pd

# Create your views here.
def home(request):
    pd_count = Tag.objects.annotate(tag_count=Count('professordev')) 
    su_count = Tag.objects.annotate(tag_count=Count('startup')) 
    fr_count = Tag.objects.annotate(tag_count=Count('financereport')) 
    pd_top_rank = dict(pd_count.filter(tag_count__gt=0).order_by('tag_count')[0:5].values_list('name', 'tag_count'))
    su_top_rank = dict(su_count.filter(tag_count__gt=0).order_by('tag_count')[0:5].values_list('name', 'tag_count'))
    fr_top_rank = dict(fr_count.filter(tag_count__gt=0).order_by('tag_count')[0:5].values_list('name', 'tag_count'))
    return render(request, 'home.html', {'pd_top_rank' : pd_top_rank, 'su_top_rank':su_top_rank, 'fr_top_rank':fr_top_rank})

def total_search(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
    return render(request, 'contentsboard/total_search.html', {'query':query})

def rescue_detail(request, pk):
    try:
        rescue = Rescue.objects.get(pk=pk)
    except Rescue.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'rescue/rescue_detail.html', {'rescue':rescue})

def rescue_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                rescue_obj = Rescue.objects.all().order_by(order_by)
            else:
                rescue_obj = Rescue.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                rescue_obj = Rescue.objects.filter(
                    Q(area__icontains=query) | Q(case_num__icontains=query) |\
                    Q(subject__icontains=query) | Q(company_name__icontains=query) |\
                    Q(category__icontains=query) | Q(news_title__icontains=query) |\
                    Q(date=query)
                ).order_by('-date')
                direction = None
            except:
                rescue_obj = Rescue.objects.all().order_by('-date')
                direction = None
    else:
        rescue_obj = Rescue.objects.all().order_by('-date')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(rescue_obj, 15)
        rescues = paginator.get_page(page)
    except:
        paginator = Paginator(rescue_obj, 15)
        rescues = None
    index = rescues.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    return render(request, 'rescue/rescue_list.html', {'rescues':rescues, 'order_by':order_by , 'direction':direction,\
                                                            'page_range':page_range, 'max_index':max_index-2})


def mail_contents_write(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        form = MailBoard(request.POST)
        if form.is_valid():
            username = request.user
            tags = form.cleaned_data['tags']
            print(tags)
            mail_content = EmailContents()
            mail_content.title = form.cleaned_data['title']
            mail_content.contents = form.cleaned_data['contents']
            mail_content.writer = User.objects.get(username=username)
            mail_content.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, created = Tag.objects.get_or_create(name=tag)
                mail_content.tags.add(_tag)


            return redirect('/contents/mail_list/')
    else:
        form = MailBoard()
    return render(request, 'emailboard/email_write.html', {'form':form})


def email_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                email_obj = EmailContents.objects.all().order_by(order_by)
                # print(email_obj)
            else:
                email_obj = EmailContents.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                email_obj = EmailContents.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).order_by('-id').distinct()
                direction = None
            except:
                email_obj = EmailContents.objects.all().order_by('-id')
                direction = None
    else:
        email_obj = EmailContents.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(email_obj, 15)
        email_contents = paginator.get_page(page)
    except:
        paginator = Paginator(email_obj, 15)
        email_contents = None
    index = email_contents.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    return render(request, 'emailboard/email_list.html', {'email_contents':email_contents, 'order_by':order_by , 'direction':direction,\
                                                          'page_range':page_range, 'max_index':max_index-2})

def mail_contents_detail(request, pk):
    try:
        EmailContent = EmailContents.objects.get(pk=pk)
        is_liked = False
        
        if EmailContent.likes.filter(id=request.user.id).exists():
            is_liked = True
    except EmailContent.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'emailboard/email_detail.html', {'EmailContent':EmailContent, 'is_liked':is_liked, 'total_likes':EmailContent.total_likes()})

@require_POST
def emailcontent_like(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    EmailContent = get_object_or_404(EmailContents, id=request.POST.get('email_contetns_id'))
    is_liked = EmailContent.likes.filter(id=request.user.id).exists()

    if is_liked:
        EmailContent.likes.remove(request.user)
    else:
        EmailContent.likes.add(request.user)

    return HttpResponseRedirect(reverse('mail_detail', kwargs={'pk': EmailContent.id}))

def professor_dev_write(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        form = ProfessorBoard(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            print(tags)
            professor_dev = ProfessorDev()
            professor_dev.name = form.cleaned_data['name']
            professor_dev.university = form.cleaned_data['university']
            professor_dev.category = form.cleaned_data['category']
            professor_dev.item = form.cleaned_data['item']
            professor_dev.news_link = form.cleaned_data['news_link']
            professor_dev.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, created = Tag.objects.get_or_create(name=tag)
                professor_dev.tags.add(_tag)

            return redirect('/contents/pd_list/')
    else:
        form = ProfessorBoard()
    return render(request, 'contentsboard/pd_write.html', {'form':form})

def start_up_write(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        form = StartUpBoard(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            print(tags)
            start_up = StartUp()
            start_up.name = form.cleaned_data['name']
            start_up.category = form.cleaned_data['category']
            start_up.item = form.cleaned_data['item']
            start_up.invest_stage = form.cleaned_data['invest_stage']
            start_up.investment = form.cleaned_data['investment']
            start_up.news_link = form.cleaned_data['news_link']
            start_up.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, created = Tag.objects.get_or_create(name=tag)
                start_up.tags.add(_tag)

            return redirect('/contents/su_list/')
    else:
        form = StartUpBoard()
    return render(request, 'contentsboard/su_write.html', {'form':form})

def finance_report_write(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        form = FinanceReportBoard(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            print(tags)
            finance_report = FinanceReport()
            finance_report.security_firm = form.cleaned_data['security_firm']
            finance_report.title = form.cleaned_data['title']
            finance_report.category = form.cleaned_data['category']
            finance_report.news_link = form.cleaned_data['news_link']
            finance_report.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, created = Tag.objects.get_or_create(name=tag)
                finance_report.tags.add(_tag)

            return redirect('/contents/fr_list/')
    else:
        form = FinanceReportBoard()
    return render(request, 'contentsboard/fr_write.html', {'form':form})

def all_table(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    return render(request, 'contentsboard/all_table.html')


def professor_dev_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                pd_obj = ProfessorDev.objects.all().order_by(order_by)
                # print(email_obj)
            else:
                pd_obj = ProfessorDev.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                pd_obj = ProfessorDev.objects.filter(Q(name__icontains=query) | Q(item__icontains=query) |\
                                                     Q(university__icontains=query) | Q(tags__name__icontains=query)).order_by('-id').distinct()
                direction = None
            except:
                pd_obj = ProfessorDev.objects.all().order_by('-id')
                direction = None
    else:
        pd_obj = ProfessorDev.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(pd_obj, 15)
        pd_contents = paginator.get_page(page)
    except:
        paginator = Paginator(pd_obj, 15)
        pd_contents = None
    index = pd_contents.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    return render(request, 'contentsboard/pd_list.html', {'pd_contents':pd_contents, 'order_by':order_by , 'direction':direction,\
                                                          'page_range':page_range, 'max_index':max_index-2, 'query':query})

def start_up_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                su_obj = StartUp.objects.all().order_by(order_by)
                # print(email_obj)
            else:
                su_obj = StartUp.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                su_obj = StartUp.objects.filter(Q(name__icontains=query) | Q(category__icontains=query) |\
                                                Q(invest_stage__icontains=query) | Q(tags__name__icontains=query)).order_by('-id').distinct()
                direction = None
            except:
                su_obj = StartUp.objects.all().order_by('-id')
                direction = None
    else:
        su_obj = StartUp.objects.all().order_by('-id')
        direction = None
        query = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(su_obj, 15)
        su_contents = paginator.get_page(page)
    except:
        paginator = Paginator(su_obj, 15)
        su_contents = None
    index = su_contents.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    return render(request, 'contentsboard/su_list.html', {'su_contents':su_contents, 'order_by':order_by , 'direction':direction,\
                                                          'page_range':page_range, 'max_index':max_index-2, 'query':query})

def finance_report_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.method == 'GET':
        query =  request.GET.get('q')
        order_by = request.GET.get('order_by')
        direction = request.GET.get('direction')
        if order_by != None:
            if direction == 'asc':
                fr_obj = FinanceReport.objects.all().order_by(order_by)
                # print(email_obj)
            else:
                fr_obj = FinanceReport.objects.all().order_by('-{}'.format(order_by))
        else:
            try:
                fr_obj = FinanceReport.objects.filter(Q(title__icontains=query) | Q(security_firm__icontains=query) |\
                                                      Q(tags__name__icontains=query)).order_by('-id').distinct()
                direction = None
            except:
                fr_obj = FinanceReport.objects.all().order_by('-id')
                direction = None
    else:
        fr_obj = FinanceReport.objects.all().order_by('-id')
        direction = None
    page = int(request.GET.get('p',1))
    try:
        paginator = Paginator(fr_obj, 15)
        fr_contents = paginator.get_page(page)
    except:
        paginator = Paginator(fr_obj, 15)
        fr_contents = None
    index = fr_contents.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])
    return render(request, 'contentsboard/fr_list.html', {'fr_contents':fr_contents, 'order_by':order_by , 'direction':direction,\
                                                          'page_range':page_range, 'max_index':max_index-2, 'query':query})
