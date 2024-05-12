from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from query import select_by_name, herb_select_by_info, smart_consultation
from go_grasph import ChatBotGraph
from query import cypher_change as cychange
from django.views.decorators.clickjacking import xframe_options_exempt
import json
# from query import query_name,query_kind
# import inquiry

# Create your views here.

@xframe_options_exempt
def welcome(request):
    return render(request, 'welcome.html')

@xframe_options_exempt
def system(request):
    return render(request, 'system.html')

@xframe_options_exempt
def zstp_show(request):
    return render(request, 'zstp_show.html')


@xframe_options_exempt
def select_attribute(request):
    return render(request, 'select_attribute.html')

@xframe_options_exempt
def admin_list(request):
    return render(request, 'admin-list.html')

@xframe_options_exempt
def admin_role(request):
    return render(request, 'admin-role.html')

@xframe_options_exempt
def simple_select_herb(request, methods=['GET', 'POST']): # 查询药材
    title = request.POST.get('title')
    if title != None:
        node = select_by_name(title,'药材')
        link = None
        if node != None:
            return render(request, 'simple_select_herb.html', {'result':json.dumps(node)})
    
    return render(request, 'simple_select_herb.html')

@xframe_options_exempt
def smart_consult(request, methods=['GET', 'POST']):
    title = request.POST.get('attending')
    if title != None:
        node = smart_consultation(title) # 调用select
        link = None
        if node != None:
            return render(request, 'smart_Consult.html', {'result':json.dumps(node)})
    return render(request, 'smart_Consult.html')

@xframe_options_exempt
def simple_select_medicine(request, methods=['GET', 'POST']): # 查询中成药
    title = request.POST.get('title')
    if title != None:
        node = select_by_name(title,'中成药')
        print(node)
        link = None
        if node != None:
            return render(request, 'simple_select_medicine.html', {'result':json.dumps(node)})
    return render(request, 'simple_select_medicine.html')

@xframe_options_exempt
def simple_select_prescr(request, methods=['GET', 'POST']): # 查询方剂
    title = request.POST.get('title')
    if title != None:
        node = select_by_name(title,'方剂')
        link = None
        if node != None:
            return render(request, 'simple_select_prescr.html', {'result':json.dumps(node)})
    return render(request, 'simple_select_prescr.html')

@xframe_options_exempt
def select_attribute(request, methods= ['GET', 'POST']):
    #kind = request.POST.get('kind')
    hrep_type = request.POST.get('hrep_type')
    hrep_feel = request.POST.get('hrep_feel')
    hrep_place = request.POST.get('hrep_place')
    #if(kind == '0'):
    if(hrep_type == None and hrep_feel == None and hrep_place == None):     
        return render(request, 'select_attribute.html')
    else:
        node = herb_select_by_info(feature=hrep_type,flavour=hrep_feel,province=hrep_place)   
        return render(request, 'select_attribute.html',{'result':json.dumps(node)})
    
@xframe_options_exempt
def cypher_change(request):
    cypher_statement = request.POST.get('cypher_statement')
    if(cypher_statement != None):
        success,result = cychange(cypher_statement)
        if(success):
        # 将查询结果result传递到messages框架，使用success级别的消息
            messages.success(request, f'执行成功，执行结果如下：')
            return render(request, 'cypher_change.html', {'result':json.dumps(result)})
        # 将异常信息exception传递到messages框架，使用error级别的消息
        else:
            messages.error(request, f'错误：{result}')
        
    return render(request, 'cypher_change.html')


@xframe_options_exempt
def smart_qa(request):
    return render(request, 'smart_QA.html')




@xframe_options_exempt
def bot_response(request):
    if request.method == 'GET':
        # 获取前端发送的消息内容
        msg_text = request.GET.get('msg')

        # 在这里编写后端处理逻辑，这里只做一个简单的示例
        if msg_text:
            handler = ChatBotGraph()
            bot_response_text = handler.chat_main(msg_text)
        else:
            bot_response_text = "请输入消息内容。"

        # 将处理结果封装为 JSON 格式，并返回给前端
        response_data = {'bot_response': bot_response_text}
        return JsonResponse(response_data)

def MainInfo(request):
    return render(request, 'MainInfo.html')

def Underwater(request):
    return render(request, 'Underwater.html')

def Datacenter(request):
    return render(request, 'datacenter.html')

def AIcenter(request):
    return render(request, 'AIcenter.html')

def AdminControl(request):
    return render(request, 'admincontrol.html')