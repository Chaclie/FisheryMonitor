import pandas as pd
import sqlalchemy

DATA_DIR = '../data/water'

# 提取xlsx中的数据数据库的water表中
def extract_data():
    file_name = '/'.join([DATA_DIR,'水质数据.xlsx']) 
    df = pd.read_excel(file_name, engine='openpyxl')
    engine = sqlalchemy.create_engine('mysql://root:root@127.0.0.1:3306/myweb')
    table_name = 'water'
    df.to_sql(table_name, engine, if_exists='replace', index=False)


extract_data()