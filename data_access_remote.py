import mysql.connector as connector

connection = connector.connect(
    host='',
    user='',
    password='',
    database=''
    )

cursor = connection.cursor()

cursor.execute("SELECT * FROM test_check")
rows = cursor.fetchall()
for row in rows:
    print(row)
    
cursor.close()
connection.close()
