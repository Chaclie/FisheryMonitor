from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
# from query import select_by_name, herb_select_by_info, smart_consultation
# from go_grasph import ChatBotGraph
# from query import cypher_change as cychange
from django.views.decorators.clickjacking import xframe_options_exempt
import json
# from query import query_name,query_kind
# import inquiry

# Create your views here.
def Index(request):

    return render(request, 'index.html')

def welcome(request):
    return render(request, 'welcome.html')

def system(request):
    return render(request, 'system.html')

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
    return render(request, 'datacenter.html')

def AIcenter(request):
    
    return render(request, 'AIcenter.html')

def AdminControl(request):
    return render(request, 'admincontrol.html')