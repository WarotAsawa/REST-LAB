from influxdb import InfluxDBClient;

client = InfluxDBClient('localhost', 8086, 'root', 'root');
client.get_list_database();
client.switch_database('simplivityNode');
result = client.query('select reductRatio from simplivityNode;')

print("Result: {0}".format(result))
