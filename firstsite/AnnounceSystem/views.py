from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import NewsUnit


import math
# Create your views here.

# def index(request):
    # return HttpResponse('<h1> this is AnnSystem </h1>')

def test_error(request, status=None):
    status = 404
    return HttpResponse(status=status)

#def index(request):
#    context = {'message' : "hello"}
#    return render(request, 'AnnounceSystem/index.html', context)

page1 = 1  #目前頁面

def index(request, pageindex=None):
    global page1  #重複開啟本網頁時需保留 page1 的值
    pagesize = 4  #每頁顯示的資料筆數
    newsall = NewsUnit.objects.all().order_by('-id')  #讀取新聞資料表,依時間遞減排序
    # NewsUnit.objects.all()[:5] 取出前五筆 or 排序 NewsUnit.objects.all().order_by('-id')[:5]
    # NewsUnit.objects.filter().count() -> int
    datasize = len(newsall)  #新聞筆數
    totpage = math.ceil(datasize / pagesize)  #總頁數
    if pageindex==None:  #無參數
        page1 = 1
        newsunits = NewsUnit.objects.filter(enabled=False).order_by('-id')[:pagesize]
    elif pageindex=='1':  #上一頁
        start = (page1-2)*pagesize  #該頁第1筆資料
        if start >= 0:  #有前頁資料就顯示
            # newsunits = NewsUnit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
            newsunits = NewsUnit.objects.filter(enabled=False).order_by('-id')[start:(start+pagesize)]
            page1 -= 1
    elif pageindex=='2':  #下一頁
        start = page1*pagesize  #該頁第1筆資料
        if start < datasize:  #有下頁資料就顯示
            # newsunits = NewsUnit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
            newsunits = NewsUnit.objects.filter(enabled=False).order_by('-id')[start:(start+pagesize)]
            page1 += 1
    elif pageindex=='3':  #由詳細頁面返回首頁
        start = (page1-1)*pagesize  #取得原有頁面第1筆資料
        # newsunits = NewsUnit.objects.filter(enabled=True).order_by('-id')[start:(start+pagesize)]
        newsunits = NewsUnit.objects.filter(enabled=False).order_by('-id')[start:(start+pagesize)]

    currentpage = page1  #將目頁前頁面以區域變數傳回html
    return render(request, "AnnounceSystem/index.html", locals())

def detail(request, detailid=None):
	unit = NewsUnit.objects.get(id=detailid)
	category = unit.catego
	title = unit.title
	pubtime = unit.pubtime
	nickname = unit.nickname
	message = unit.message
	unit.press += 1
	unit.save()
	
	return render(request, "AnnounceSystem/detail.html", locals())

def login(request, loc=None):
    title = "Login System"
    message = ""
    if loc == "guest":
        message = "請進行登入"
        return render(request, "AnnounceSystem/login.html", locals())
    
    if request.method == 'POST' and loc == "admin":
        name = request.POST['username'].strip()
        password = request.POST['password']
        admin01 = authenticate(username=name, password=password)
        if admin01 is not None:
            if admin01.is_active:
                auth.login(request, admin01)
                message = "login success" + " loc = " +loc
                # return render(request, "AnnounceSystem/announadmin.html", locals())
                return redirect('AnnounceSystem:showData')
            else:
                message = "Invalid account."
            
        else:
            message = " Lonin not pass. "
            return render(request, "AnnounceSystem/login.html", locals())

    return render(request, "AnnounceSystem/login.html", locals())
    # return render(request, reverse('AnnounceSystem/login.html'), locals())
    # return redirect('AnnounceSystem:index')

def adminShow(request, pageindex=None):
    global page1  
    pagesize = 4 
    newsall = NewsUnit.objects.all().order_by('-id')
    datasize = len(newsall) 
    totpage = math.ceil(datasize / pagesize)
    if pageindex==None:
        page1 = 1
        newsunits = NewsUnit.objects.order_by('-id')[:pagesize]
    elif pageindex=='1': 
        start = (page1-2)*pagesize 
        if start >= 0:  
            newsunits = NewsUnit.objects.order_by('-id')[start:(start+pagesize)]
            page1 -= 1
    elif pageindex=='2':  
        start = page1*pagesize  
        if start < datasize:  
            newsunits = NewsUnit.objects.order_by('-id')[start:(start+pagesize)]
            page1 += 1
    elif pageindex=='3':  
        start = (page1-1)*pagesize  
        newsunits = NewsUnit.objects.order_by('-id')[start:(start+pagesize)]
    currentpage = page1  
    return render(request, "AnnounceSystem/announadmin.html", locals())

def newsadd(request):
    message = ""
    category = request.POST.get('news_type', '')
    subject = request.POST.get('news_subject', '')
    editor = request.POST.get('news_editor', '')
    content = request.POST.get('news_content', '')
    ok = request.POST.get('news_ok', '')

    if subject == '' or editor == '' or content == '':
        message = "Can not be blank."
    else:
        if ok == "yes":
            enabled = True
        else:
            enabled = False
        unit = NewsUnit.objects.create(catego=category, nickname=editor, title=subject, message=content, enabled=enabled, press=0)
        unit.save()
        return redirect('AnnounceSystem:showData')
    return render(request, "AnnounceSystem/newsadd.html", locals())

def newsedit(request, newsid=None, edittype=None):  #修改資料
	unit = NewsUnit.objects.get(id=newsid)  #讀取指定資料
	categories = ["公告", "更新", "活動", "新書", "其他"]
	if edittype == None:  #進入修改頁面,顯示原有資料
		type = unit.catego
		subject = unit.title
		editor = unit.nickname
		content = unit.message
		ok = unit.enabled
	elif edittype == '1':  #修改完畢,存檔
		category = request.POST.get('news_type', '')
		subject = request.POST.get('news_subject', '')
		editor = request.POST.get('news_editor', '')
		content = request.POST.get('news_content', '')
		ok = request.POST.get('news_ok', '')
		if ok=='yes':
			enabled = True
		else:
			enabled = False
		unit.catego=category
		unit.nickname=editor
		unit.title=subject
		unit.message=content
		unit.enabled=enabled
		unit.save()
		return redirect('AnnounceSystem:showData')
	return render(request, "AnnounceSystem/newsedit.html", locals())

def newsdelete(request, newsid=None, deletetype=None):  #刪除資料
	unit = NewsUnit.objects.get(id=newsid)  #讀取指定資料
	if deletetype == None:  #進入刪除頁面,顯示原有資料
		type = str(unit.catego.strip())
		subject = unit.title
		editor = unit.nickname
		content = unit.message
		date = unit.pubtime
	elif deletetype == '1':  #按刪除鈕
		unit.delete()
		return redirect('AnnounceSystem:showData')
	return render(request, "AnnounceSystem/newsdelete.html", locals())
