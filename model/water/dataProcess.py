import pandas as pd
import numpy as np
import os,json

DATA_DIR = '../data/water'
OUT_DIR = '../data/water/processed'

'''
    Date:日期
    temp:温度
    pH:pH值
    Ox:含氧量
    Dao:导电率
    Zhuodu:浊度
    Yandu:盐度
    Andan:氨氮
    Zonglin:总磷
    Zongdan:总氮
'''

file = '../data/water/水质数据.xlsx'

# 数据导入
def extract_data():
    df = pd.read_excel(file, names = ['Date', 'temp', 'pH', 'Ox', 'Dao', 'Zhuodu', 'Yandu', 'Andan', 'Zonglin', 'Zongdan'], usecols = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    df.to_csv(os.path.join(OUT_DIR, 'water.csv'))

# 数据处理
def clean_data():
    df=pd.read_csv(os.path.join(OUT_DIR, 'water.csv'))
    #删除空项
    df=df.dropna()
    #删除非法项
    for i in ['Date', 'temp', 'pH', 'Ox', 'Dao', 'Zhuodu', 'Yandu', 'Andan', 'Zonglin', 'Zongdan']:
        df=df.drop(df[df[i]=='--'].index)
    #类型转换
    df=df.astype('float64')
    #打印
    print(df)
    print(df['Andan'])
    #保存
    df.to_csv(os.path.join(OUT_DIR, 'water_cleaned.csv'))

if __name__ == '__main__':
    extract_data()
    clean_data()