import Datalink

datalink_cursor = Datalink.get_cursor()
datalink_cursor.execute("SELECT * FROM Reported_Items")

data = datalink_cursor.fetchall()

Datalink.disconnect_datalink()

for row_data in data:
    print(row_data)

#print(data)