from getdata import WaterDataset, getdata_from_xlsx
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from ResMLP import ResMLP

def premanage(data):
    # 采用地表水水质评价指标

    out_dict = {0:'I', 1:'II', 2:'III', 3:'IV', 4:'V'}
    error = []

    # 水温
    if data[0] >0 and data[0]<20:
        error.append(0)
    elif data[0] <30:
        error.append(2)
    else:
        error.append(4)

    # PH
    if data[1]>6 and data[1]<9:
        error.append(0)
    else:
        error.append(4)

    # 溶氧量
    if data[2] is None:
        error.append(0)
    elif data[2]>=7.5:
        error.append(0)
    elif data[2]>=6:
        error.append(1)
    elif data[2]>=5:
        error.append(2)
    elif data[2]>=3:
        error.append(3)
    else:
        error.append(4)

    # 高锰酸
    if data[5] is None:
        error.append(0)
    elif data[5]<=2:
        error.append(0)
    elif data[5]<=4:
        error.append(1)
    elif data[5]<=6:
        error.append(2)
    elif data[5]<=10:
        error.append(3)
    else:
        error.append(4)
    
    # an氮
    if data[6] is None:
        error.append(0)
    elif data[6]<=0.15:
        error.append(0)
    elif data[6]<=0.5:
        error.append(1)
    elif data[6]<=1:
        error.append(2)
    elif data[6]<=1.5:
        error.append(3)
    else:
        error.append(4)

    # 磷
    if data[7] is None:
        error.append(0)
    elif data[7]<=0.02:
        error.append(0)
    elif data[7]<=0.1:
        error.append(1)
    elif data[7]<=0.2:
        error.append(2)
    elif data[7]<=0.3:
        error.append(3)
    else:
        error.append(4)
    
    # 总氮
    if data[8] is None:
        error.append(0)
    elif data[8]<=0.2:
        error.append(0)
    elif data[8]<=0.5:
        error.append(1)
    elif data[8]<=1.0:
        error.append(2)
    elif data[8]<=1.5:
        error.append(3)
    else:
        error.append(4)

    return error 

def model_predict(data, path = "./model.pth", in_dim=7, out_dim=5, device='cpu'):
    model = ResMLP(in_dim, out_dim)
    model.load_state_dict(torch.load(path))
    model = model.to(device)
    model.eval()

    data = premanage(data)
    data = torch.tensor(data).float().to(device)
    data = data.view(-1,7)
    # print(data.shape)
    output = model(data)
    pred = output.data.max(1)[1]

    if pred[0] == 0:
        return 'Ⅰ'
    elif pred[0] == 1:
        return 'Ⅱ'
    elif pred[0] == 2:
        return 'Ⅲ'
    elif pred[0] == 3:
        return 'Ⅳ'
    elif pred[0] == 4:
        return '劣Ⅴ'
    else:
        return 'III'
        