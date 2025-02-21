# import sqlite3
# conn = sqlite3.connect('aws_costs.db')
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM cost_data")
# for row in cursor.fetchall():
#     print(row)
# conn.close()
import sqlite3

conn = sqlite3.connect('aws_costs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM cost_data")
data = cursor.fetchall()
print("Number of records:", len(data))
if data:
    print("Sample record:", data[0])
conn.close()