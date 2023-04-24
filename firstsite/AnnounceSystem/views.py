from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
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
	unit = NewsUnit.objects.get(id=detailid)  #根據參數取出資料
	category = unit.catego
	title = unit.title
	pubtime = unit.pubtime
	nickname = unit.nickname
	message = unit.message
	unit.press += 1  #點擊數加1
	unit.save()  #儲存資料
	
	return render(request, "AnnounceSystem/detail.html", locals())

def login(request, loc=None):
    title = "Login System"
    message = ""
    if loc == "guest":
        message = "請進行登入"
        return render(request, "AnnounceSystem/login.html", locals())
    
    # return render(request, "AnnounceSystem/login.html", locals())
    # return render(request, reverse('AnnounceSystem/login.html'), locals())

    return redirect('AnnounceSystem:index')