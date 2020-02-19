import sys;
from influxdb import InfluxDBClient;

dbIP = "172.30.5.21";
dbUser = "root";
dbPassword = "root";

client = InfluxDBClient(host=dbIP, port=8086)

dbList = client.get_list_database();

for db in dbList:
	print(db["name"]);


