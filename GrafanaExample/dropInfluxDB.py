import sys;
from influxdb import InfluxDBClient;

dbIP = "172.30.5.21";
dbUser = "root";
dbPassword = "root";
dbName = sys.argv[1];

client = InfluxDBClient(host=dbIP, port=8086)
client.drop_database(dbName)

dbList = client.get_list_database();

for db in dbList:
	print(db["name"]);


