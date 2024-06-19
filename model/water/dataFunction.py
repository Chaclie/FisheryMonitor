import pymysql

def connectDB():
    db = pymysql.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        password = "root",
        db = "myweb",
    )
    cursor = db.cursor()
    return cursor

#返回每行的数据，每行类型为tuple
def allVal():
    cur = connectDB()
    
    sql = '''select * from water'''
    cur.execute(sql)
    data=cur.fetchall() 
    return data

#返回表格所用数据，类型为{"temp":val, "pH":val, "Ox":val, "Dao":val, "Zhuodu":val, "Yandu":val}
#其中val可为维数为7的浮点数组,
def formVal(time):
    cur = connectDB()
    
    if time == "All":
        temp, pH, Ox, Dao, Zhuodu, KMnO4 = [], [], [], [], [], []
        for i in range(7):
            tempsql = '''select avg(`水温（℃）`) from (select `水温（℃）` from water limit ''' + str(300*(i+1)) + ''') as d0'''
            pHsql = '''select avg(`pH(无量纲)`) from (select `pH(无量纲)` from water limit ''' + str(300*(i+1)) + ''') as d1'''
            Oxsql = '''select avg(`溶氧量(mg/L)`) from (select `溶氧量(mg/L)` from water limit ''' + str(300*(i+1)) + ''') as d2'''
            Dsql = '''select avg(`电导率（μS/cm）`) from (select `电导率（μS/cm）` from water limit ''' + str(300*(i+1)) + ''') as d3'''
            Nsql = '''select avg(`浊度（NTU）`) from (select `浊度（NTU）` from water limit ''' + str(300*(i+1)) + ''') as d4'''
            Ksql = '''select avg(`高锰酸盐指数（mg/L）`) from (select `高锰酸盐指数（mg/L）` from water limit ''' + str(300*(i+1)) + ''') as d5'''
            cur.execute(tempsql)
            temp.append(cur.fetchall()[0][0])
            cur.execute(pHsql)
            pH.append(cur.fetchall()[0][0])
            cur.execute(Oxsql)
            Ox.append(cur.fetchall()[0][0])
            cur.execute(Dsql)
            Dao.append(cur.fetchall()[0][0])
            cur.execute(Nsql)
            Zhuodu.append(cur.fetchall()[0][0])
            cur.execute(Ksql)
            KMnO4.append(cur.fetchall()[0][0])
        return {"temp":temp, "pH":pH, "Ox":Ox, "Dao":Dao, "Zhuodu":Zhuodu, "Yandu":KMnO4}
    
    if time == "近1天":
        temp, pH, Ox, Dao, Zhuodu, KMnO4 = [], [], [], [], [], []
        for i in range(7):
            tempsql = '''select avg(`水温（℃）`) from (select `水温（℃）` from water limit ''' + str(30*(i+1)) + ''') as d0'''
            pHsql = '''select avg(`pH(无量纲)`) from (select `pH(无量纲)` from water limit ''' + str(30*(i+1)) + ''') as d1'''
            Oxsql = '''select avg(`溶氧量(mg/L)`) from (select `溶氧量(mg/L)` from water limit ''' + str(30*(i+1)) + ''') as d2'''
            Dsql = '''select avg(`电导率（μS/cm）`) from (select `电导率（μS/cm）` from water limit ''' + str(30*(i+1)) + ''') as d3'''
            Nsql = '''select avg(`浊度（NTU）`) from (select `浊度（NTU）` from water limit ''' + str(30*(i+1)) + ''') as d4'''
            Ksql = '''select avg(`高锰酸盐指数（mg/L）`) from (select `高锰酸盐指数（mg/L）` from water limit ''' + str(30*(i+1)) + ''') as d5'''
            cur.execute(tempsql)
            temp.append(cur.fetchall()[0][0])
            cur.execute(pHsql)
            pH.append(cur.fetchall()[0][0])
            cur.execute(Oxsql)
            Ox.append(cur.fetchall()[0][0])
            cur.execute(Dsql)
            Dao.append(cur.fetchall()[0][0])
            cur.execute(Nsql)
            Zhuodu.append(cur.fetchall()[0][0])
            cur.execute(Ksql)
            KMnO4.append(cur.fetchall()[0][0])
        return {"temp":temp, "pH":pH, "Ox":Ox, "Dao":Dao, "Zhuodu":Zhuodu, "Yandu":KMnO4}
    
    if time == "近1周":
        temp, pH, Ox, Dao, Zhuodu, KMnO4 = [], [], [], [], [], []
        for i in range(7):
            tempsql = '''select avg(`水温（℃）`) from (select `水温（℃）` from water limit ''' + str(70*(i+1)) + ''') as w0'''
            pHsql = '''select avg(`pH(无量纲)`) from (select `pH(无量纲)` from water limit ''' + str(70*(i+1)) + ''') as w1'''
            Oxsql = '''select avg(`溶氧量(mg/L)`) from (select `溶氧量(mg/L)` from water limit ''' + str(70*(i+1)) + ''') as w2'''
            Dsql = '''select avg(`电导率（μS/cm）`) from (select `电导率（μS/cm）` from water limit ''' + str(70*(i+1)) + ''') as w3'''
            Nsql = '''select avg(`浊度（NTU）`) from (select `浊度（NTU）` from water limit ''' + str(70*(i+1)) + ''') as w4'''
            Ksql = '''select avg(`高锰酸盐指数（mg/L）`) from (select `高锰酸盐指数（mg/L）` from water limit ''' + str(70*(i+1)) + ''') as w5'''
            cur.execute(tempsql)
            temp.append(cur.fetchall()[0][0])
            cur.execute(pHsql)
            pH.append(cur.fetchall()[0][0])
            cur.execute(Oxsql)
            Ox.append(cur.fetchall()[0][0])
            cur.execute(Dsql)
            Dao.append(cur.fetchall()[0][0])
            cur.execute(Nsql)
            Zhuodu.append(cur.fetchall()[0][0])
            cur.execute(Ksql)
            KMnO4.append(cur.fetchall()[0][0])
        return {"temp":temp, "pH":pH, "Ox":Ox, "Dao":Dao, "Zhuodu":Zhuodu, "Yandu":KMnO4}
    
    if time == "近1月":
        temp, pH, Ox, Dao, Zhuodu, KMnO4 = [], [], [], [], [], []
        for i in range(7):
            tempsql = '''select avg(`水温（℃）`) from (select `水温（℃）` from water limit ''' + str(140*(i+1)) + ''') as m0'''
            pHsql = '''select avg(`pH(无量纲)`) from (select `pH(无量纲)` from water limit ''' + str(140*(i+1)) + ''') as m1'''
            Oxsql = '''select avg(`溶氧量(mg/L)`) from (select `溶氧量(mg/L)` from water limit ''' + str(140*(i+1)) + ''') as m2'''
            Dsql = '''select avg(`电导率（μS/cm）`) from (select `电导率（μS/cm）` from water limit ''' + str(140*(i+1)) + ''') as m3'''
            Nsql = '''select avg(`浊度（NTU）`) from (select `浊度（NTU）` from water limit ''' + str(140*(i+1)) + ''') as m4'''
            Ksql = '''select avg(`高锰酸盐指数（mg/L）`) from (select `高锰酸盐指数（mg/L）` from water limit ''' + str(140*(i+1)) + ''') as m5'''
            cur.execute(tempsql)
            temp.append(cur.fetchall()[0][0])
            cur.execute(pHsql)
            pH.append(cur.fetchall()[0][0])
            cur.execute(Oxsql)
            Ox.append(cur.fetchall()[0][0])
            cur.execute(Dsql)
            Dao.append(cur.fetchall()[0][0])
            cur.execute(Nsql)
            Zhuodu.append(cur.fetchall()[0][0])
            cur.execute(Ksql)
            KMnO4.append(cur.fetchall()[0][0])
        return {"temp":temp, "pH":pH, "Ox":Ox, "Dao":Dao, "Zhuodu":Zhuodu, "Yandu":KMnO4}

#返回表内所有数据的每项平均值
def avgVal():
    cur = connectDB()

    tempsql = '''select avg(`水温（℃）`) from water'''
    pHsql = '''select avg(`pH(无量纲)`) from water'''
    Oxsql = '''select avg(`溶氧量(mg/L)`) from water'''
    Dsql = '''select avg(`电导率（μS/cm）`) from water'''
    Nsql = '''select avg(`浊度（NTU）`) from water'''
    Ksql = '''select avg(`高锰酸盐指数（mg/L）`) from water'''
    cur.execute(tempsql)
    temp=round(cur.fetchall()[0][0],3)
    cur.execute(pHsql)
    pH=round(cur.fetchall()[0][0],3)
    cur.execute(Oxsql)
    Ox=round(cur.fetchall()[0][0],3)
    cur.execute(Dsql)
    Dao=round(cur.fetchall()[0][0],3)
    cur.execute(Nsql)
    Zhuodu=round(cur.fetchall()[0][0],3)
    cur.execute(Ksql)
    KMnO4=round(cur.fetchall()[0][0],3)
    return {"temp":temp, "pH":pH, "Ox":Ox, "Dao":Dao, "Zhuodu":Zhuodu, "Yandu":KMnO4}
