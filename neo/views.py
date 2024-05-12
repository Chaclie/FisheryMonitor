from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from neo.models import User
import re,json


# Create your views here.
def Index(request):

    return render(request, 'index.html')

def welcome(request):
    return render(request, 'welcome.html')

def forget(request):
    return render(request, "forget_code.html")

def system(request):
    
    uid = request.GET.get('uid')
    if uid == None:
        return redirect("/")
    user = User.objects.get(id=uid)
    dic = {0:'普通用户',1:'批发商',2:'养殖户',3:'管理员',4:'高级管理员'}
    return render(request, 'system.html', {'uid': uid, 'username': user.username, 'permission': user.permission, 'identity':dic[user.permission]})
    
    # return render(request, 'system.html')

def MainInfo(request):
    info = {
        'ele_V' : 25.9,
        'PH'    : 8.37,
        'tempreture' : 25.9,
        'NTU'   : 2.05,
        'location': '../static/images/1.jpg',
    }
    history = {
        'ele_V' : [25.9, 25.8, 25.7, 25.6, 25.5, 25.4, 25.3, 25.2, 25.1, 25.0],
        'PH'    : [8.37, 8.36, 8.35, 8.34, 8.33, 8.32, 8.31, 8.30, 8.29, 8.28],
        'tempreture' : [25.9, 25.8, 25.7, 25.6, 25.5, 25.4, 25.3, 25.2, 25.1, 25.0],
        'NTU'   : [2.05, 2.04, 2.03, 2.02, 2.01, 2.00, 1.99, 1.98, 1.97, 1.96],
    }



    return render(request, 'MainInfo.html')

def Underwater(request):
    return render(request, 'Underwater.html')

def Datacenter(request):
    data = {
        'Prosess': 999,
        'disk_used': 1000,
        'disk_rest': 1500,
        'transport_time' : "02:45",
        'CPU': 80,
        'memory': 60,
        'GPU': 50,
    }
    return render(request, 'datacenter.html',data)

def AIcenter(request):
    
    return render(request, 'AIcenter.html')

def AdminControl(request):
    return render(request, 'admincontrol.html')


# 注册登录
def login(request):
    if request.method == 'GET':
        # 先尝试从cookie登录
        usrname = request.COOKIES.get('username')
        pwd = request.COOKIES.get('password')
        try:
            user = User.objects.get(username=usrname)
            if user.password == pwd and request.GET.get('status') != 'quit': # cookie验证成功，直接前往主页
                return redirect(f'/system/?uid={user.id}')
            # 否则渲染登录页
            return render(request, 'login.html')
        except:
            return render(request, 'login.html')
    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    verify_code = request.POST.get('verify_code') # 获取用户输入的验证码
    if str(verify_code).lower() != 'xszg':
        return render(request, 'login.html', {'error': '验证码错误！'})
    # 检查用户输入的用户名和密码
    curr_user = User.objects.filter(username=username)
    if len(curr_user) == 0:
        return render(request, 'login.html', {'error': '用户名不存在！'})
    if curr_user[0].password != password:
        return render(request, 'login.html', {'error': '密码错误！'})
    cookie = {
        'username': username,
        'password': password
    }
    response = HttpResponseRedirect('/system/')
    for k,v in cookie.items():
        response.set_cookie(k,v,max_age=60*60*24,path='/') # 设置一天的cookie
    return response

def register_page(request):
    if request.method == 'GET':
        return render(request,'register.html')
    # POST
    # 用户名不能重复
    username = request.POST.get('username')
    if len(User.objects.filter(username=username))!=0:
        return render(request, 'register.html', {'error': '用户名已存在！'})

    # 邮箱格式检查，并且邮箱不能重复
    email = request.POST.get('email')
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern,str(email)):
        return render(request, 'register.html', {'error': '邮箱格式错误！'})
    if len(User.objects.filter(email=email))!=0:
        return render(request, 'register.html', {'error': '邮箱已存在！'})

    password = request.POST.get('password')
    # 创建新用户
    User.objects.create(username=username, password=password, email=email)
    response = HttpResponseRedirect('/') # 返回登录页
    # 创建新用户之后，删除所有cookie
    cookie_names = request.COOKIES.keys()
    for cookie_name in cookie_names:
        response.delete_cookie(cookie_name)
    return response

def edit_data(request):
    username = request.GET.get('username')
    return render(request, 'edit.html', {'username': username})

def edit_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    permission = request.POST.get('interest')

    # 定位原来的用户
    origin = request.POST.get('origin')
    user = User.objects.get(username=origin)
    user.username = username
    user.password = password
    user.email = email
    user.permission = permission
    user.save()
    return redirect('/backend/table.html')

def backend(request):
    return render(request, 'backend.html')

def table(request):
    return render(request, 'table.html')

def get_data(request):
    users = list(User.objects.all().values())  # 获取所有用户数据，并转换为字典列表
    return JsonResponse({"code": 0, "data": users})

def smart_qa(request):
    return render(request, 'smart_QA.html')