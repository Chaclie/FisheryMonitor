from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from GroupWork import settings
from neo.models import User,FishInfo,WaterInfo
from model.fish.LSTM_fish import LSTMModel
import re,json,os
import pandas as pd
import numpy as np

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
    res=get_water_statistics(request)
    data=json.loads(res.content)
    return render(request,'MainInfo.html',{'data':data})

def Underwater(request):
    res = get_fish_statistics(request)
    data = json.loads(res.content)
    print(data)
    return render(request, 'Underwater.html', {'data':data})

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
    if len(request.GET) == 0:
        return render(request, 'AIcenter.html')
    show = int(request.GET.get('show')[0])
    w = str(round(float(request.GET.get('w')),2))+ ' kg'
    l = str(round(float(request.GET.get('l')),2))+ ' cm'
    print(show,w,l)
    return render(request, 'AIcenter.html', {'show':show, 'w':w, 'l':l})

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

# 用户数据
def get_data(request):
    users = list(User.objects.all().values())  # 获取所有用户数据，并转换为字典列表
    return JsonResponse({"code": 0, "data": users})

def smart_qa(request):
    return render(request, 'smart_QA.html')

# 获取鱼类统计信息
def get_fish_statistics(request):
    # 获取当前绝对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR,"model/data/fish/processed")
    data = pd.read_csv(os.path.join(path,'fish.csv'),index_col=0)
    # 获取鱼类种类和数量
    fish_species = data['Latin_Name'].unique()
    fish_count = int(data['Count'].sum())
    data = pd.read_csv(os.path.join(path,'fish_final.csv'),index_col=0)
    # 获取平均体长和平均体重，保留两位小数
    mean_length = round(data['Mean_Length'].mean(),2)
    mean_weight = round(data['Mean_Weight'].mean(),2)
    return JsonResponse({'fish_species':len(fish_species),
                         'fish_count':fish_count,
                         'mean_length':mean_length,
                         'mean_weight':mean_weight
                         })

def getTOP5(request):
    # 获取当前绝对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "model/data/fish/processed")
    data = pd.read_csv(os.path.join(path,'fish_cleaned.csv'),index_col=0)
    # 获取top5
    all_groups = data.groupby('Latin_Name')
    tuples = []
    for group_name in all_groups.groups:
        curr_group = all_groups.get_group(group_name)
        dates = curr_group['Date'].unique()
        tuples.append((group_name, len(dates)))
    tuples.sort(key=lambda x: x[1], reverse=True)
    tuples = tuples[:30]
    top5 = [{'value':tuples[i][1],'name':tuples[i][0]} for i in range(30)]
    return JsonResponse(top5, safe=False)

def get_fish_change(request):
    # 获取当前绝对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "model/data/fish/processed")
    data = pd.read_csv(os.path.join(path,'fish_time.csv'),index_col=0)
    data['Date'] = pd.to_datetime(data['Date'])
    return JsonResponse(data.to_dict(orient='list'))

def get_top_info(request):
    # 获取当前绝对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "model/data/fish/processed")
    with open(os.path.join(path,'top_info.json'),'r') as f:
        data = json.load(f)
    return JsonResponse(data,safe=False)

def writ1eDB(request):
    FishInfo.objects.all().delete() # 防止重复写入
    usecols = ['Year','Date', 'Latin_Name', 'Count', 'Mean_Length', 'Mean_Weight']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "model/data/fish/processed")
    data = pd.read_csv(os.path.join(path,"fish_final.csv"),usecols=usecols)
    for i in range(len(data)):
        row = data.iloc[i]
        FishInfo.objects.create(year=row['Year'], date=row['Date'], latin_name=row['Latin_Name'], count=row['Count'], mean_length=row['Mean_Length'], mean_weight=row['Mean_Weight'])
    return HttpResponse("success")

def fish_predict(request):
    if request.method == "GET":
        fish_species = FishInfo.objects.values('latin_name').distinct()
        return render(request, 'fish_predict.html', {'fish_species':fish_species})
    else:
        fish_name = request.POST.get('fish_name')
        duration = int(request.POST.get('duration'))
        fish_data = FishInfo.objects.filter(latin_name=fish_name)
        data = pd.DataFrame(list(fish_data.values()),columns=['id','year','date','latin_name','count','mean_length','mean_weight'])
        data['date_ordinal'] = data['date'].apply(lambda x: x.toordinal())
        data = data[['year', 'date_ordinal', 'count']]
        data = np.array(data)[-1*duration:]
        data = np.expand_dims(data, axis=0)

        # 获取当前绝对路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        SAVE_PATH = os.path.join(BASE_DIR, "model/data/fish/save")
        model = LSTMModel(3,100,2,2,SAVE_PATH=SAVE_PATH)
        predictions = model.api(data,DATA_PATH=os.path.join(BASE_DIR, "model/data/fish/processed/fish_final.csv"))
        return redirect(f'http://127.0.0.1:8000/system/AIcenter.html?show=1&w={predictions[1]}&l={predictions[0]}')
    
# 获取水质统计信息
# '''
#     Date:日期
#     temp:温度
#     pH:pH值
#     Ox:含氧量
#     Dao:导电率
#     Zhuodu:浊度
#     Yandu:盐度
# '''
def get_water_statistics(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR,"model/data/water/processed")
    data = pd.read_csv(os.path.join(path,'water_cleaned.csv'),index_col=0)
    # 获取统计图信息
    FormData={}
    for tag in ['Day','Week','Month','All']:
        temp,pH,Ox,Dao,Zhuodu,Yandu=[],[],[],[],[],[]
        
        step=0
        match tag:
            case 'Day':
                step=30
            case 'Week':
                step=70
            case 'Month':
                step=140
            case 'All':
                step=300

        for i in range(7):
            temp.append(round(data['temp'].head((i+1)*step).mean(),3))
            pH.append(round(data['pH'].head((i+1)*step).mean(),3))
            Ox.append(round(data['Ox'].head((i+1)*step).mean(),3))
            Dao.append(round(data['Dao'].head((i+1)*step).mean(),3))
            Zhuodu.append(round(data['Zhuodu'].head((i+1)*step).mean(),3))
            Yandu.append(round(data['Yandu'].head((i+1)*step).mean(),3))
        
        match tag:
            case 'Day':
                Day={'temp':temp,'pH':pH,'Ox':Ox,'Dao':Dao,'Zhuodu':Zhuodu,'Yandu':Yandu}
                FormData[tag]=Day
            case 'Week':
                Week={'temp':temp,'pH':pH,'Ox':Ox,'Dao':Dao,'Zhuodu':Zhuodu,'Yandu':Yandu}
                FormData[tag]=Week
            case 'Month':
                Month={'temp':temp,'pH':pH,'Ox':Ox,'Dao':Dao,'Zhuodu':Zhuodu,'Yandu':Yandu}
                FormData[tag]=Month
            case 'All':
                All={'temp':temp,'pH':pH,'Ox':Ox,'Dao':Dao,'Zhuodu':Zhuodu,'Yandu':Yandu}
                FormData[tag]=All

    # 获取表格数据
    AvgData={}
    for tag in ['temp','pH','Ox','Dao','Zhuodu','Yandu']:
        AvgData[tag]=round(data[tag].mean(),3)

    print(FormData)
    print(AvgData)

    return JsonResponse({'FormData':FormData,'AvgData':AvgData})

# 导入水质数据到数据库
def writ2eDB(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "model/data/water/processed")
    data = pd.read_csv(os.path.join(path,"water_cleaned.csv"))

    WaterInfo.objects.all().delete()
    for i in range(len(data)):
        row = data.iloc[i]
        WaterInfo.objects.create(Date=row['Date'],temp=row['temp'],pH=row['pH'],Ox=row['Ox'],Dao=row['Dao'],Zhuodu=row['Zhuodu'],Yandu=row['Yandu'])
    return HttpResponse("success")

# 从这里开始是视频和图像处理：
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        upload_type = request.POST.get('upload_type', 'unknown')

        # 构造保存路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir  = os.path.join(BASE_DIR, "neo\static\\video\\")
        print(upload_dir)
        video_file.name = f'{upload_type}.mp4'
        # 保存文件
        with open(os.path.join(upload_dir, video_file.name), 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        return render(request, 'MainInfo.html')
    else :
        # 处理 GET 请求
        return render(request, 'MainInfo.html', {'error': '未上传视频！'})
