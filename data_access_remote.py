import mysql.connector as connector

connection = connector.connect(
    host='ec2-54-165-234-73.compute-1.amazonaws.com',
    user='username',
    password='Password@1',
    database='cps_project_g7'
    )

cursor = connection.cursor()

cursor.execute("SELECT * FROM test_check")
rows = cursor.fetchall()
for row in rows:
    print(row)
    
cursor.close()
connection.close()