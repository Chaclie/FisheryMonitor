import pymysql

def connectDB():
    db = pymysql.connect(
        host = "127.0.0.1",
        post = 3306,
        use = "root",
        password = "root",
        db = "myweb",
    )
    cursor = db.cursor()
    return cursor

def AverageVal(time):
    cur = connectDB()
    if time == "All":
        sql = '''select avg(水温（℃）) from water '''
    if time == "近1天":
        sql = '''select avg(水温（℃）) from (select (水温（℃）) from water limit 200) as daysub'''
    if time == "近1周":
        sql = '''select avg(水温（℃）) from (select (水温（℃）) from water limit 200) as daysub'''

