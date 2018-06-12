import pymysql,csv
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd = '0811', db='chipsort', charset='utf8')
cursor = conn.cursor()
cursor.execute('SELECT * FROM overtime')
data = cursor.fetchall()
cursor.close()
f=open('overtime.csv','w')
csv_write = csv.writer(f)

for x in data:
    csv_write.writerow(list(x))
f.close()

print(data)