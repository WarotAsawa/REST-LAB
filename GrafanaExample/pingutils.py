import os;
import subprocess;
import json
from InfluxInserter import InfluxInserter;

ic = InfluxInserter("172.30.5.21", "root", "root", 8086, "hostuptime");
with open('hostList.json') as json_file:
	data = json.load(json_file);
	for host in data['hostList']:
		address = host["hostname"];
		des = host["description"];
		res = subprocess.call(['ping', '-c', '1', address])
		if res == 0:
			print "ping to", address, "OK";
			result = ic.InsertData(measurement = 'status',tags = {"hostname":address, "description":des},fields = {"uptime":100}); 
			print result;
		elif res == 2:
			print "no response from", addressi
			ic.InsertData(measurement = 'status',tags = {"hostname":address, "description":des},fields = {"uptime":0});
		else:
			print "ping to", address, "failed!"
			ic.InsertData(measurement = 'status',tags = {"hostname":address, "description":des},fields = {"uptime":0});

