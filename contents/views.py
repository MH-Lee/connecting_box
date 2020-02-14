from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import MailBoard
from django.views.generic import TemplateView, ListView
from .models import Rescue, EmailContents, ProfessorDev, FinanceReport, StartUp, Tag
from accounts.models import User
import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'home.html')

def rescue_detail(request, pk):
    try:
        rescue = Rescue.objects.get(pk=pk)
    except Rescue.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'contents/rescue_detail.html', {'rescue':rescue})

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
    return render(request, 'information/rescue_list.html', {'rescues':rescues, 'order_by':order_by , 'direction':direction,\
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
                print(query)
                email_obj = EmailContents.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).order_by('-id').distinct()
                print(email_obj)
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
    except EmailContent.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render(request, 'emailboard/email_detail.html', {'EmailContent':EmailContent})