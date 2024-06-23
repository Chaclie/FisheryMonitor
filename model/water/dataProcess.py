import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

DATA_DIR = '../data/water'

# 提取xlsx中的数据数据库的water表中
def extract_waterdata():
    file_name = '/'.join([DATA_DIR,'水质数据.xlsx']) 
    df = pd.read_excel(file_name, engine='openpyxl')
    engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/myweb')
    table_name = 'water'
    df.to_sql(table_name, engine, if_exists='replace', index=False)

#添加设备运行状态数据表device
def extract_devicedata():
    engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/myweb')
    metadata =MetaData()
    
    devices = Table('device', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(20)),
                  Column('situation', String(20)),
                  )
    metadata.create_all(engine)

    #每次添加一组8个设备状态，用于模拟实时的设备状态






extract_waterdata()
extract_devicedata()