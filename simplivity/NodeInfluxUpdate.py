#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
from influxdb import InfluxDBClient;

#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from Time import Time;
import time;
from datetime import datetime

import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"simplivity")));
from SimplivityCluster import SimplivityCluster;
#sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"nimble")));
#from NimbleArray import NimbleArray;
#---------------------------------------------------------------------
#

OVC_IP = "172.30.6.36";
OVC_USERNAME = "administrator@vsphere.local";
OVC_PASSWORD = "P@ssw0rd";

INFLUX_IP = "localhost";
INFLUX_PORT = "8086";
INFLUX_DB = "simplivityNode";
INFLUX_USERNAME = "root";

llCluster = SimplivityCluster(OVC_IP,OVC_USERNAME,OVC_PASSWORD);
llCluster.Initialize();
client = InfluxDBClient(INFLUX_IP, INFLUX_PORT, INFLUX_USERNAME, INFLUX_USERNAME, INFLUX_DB);
now = datetime.utcnow();
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)	

nodes = llCluster.GetHostsAll();
clusters = llCluster.GetClustersAll();
backups = llCluster.GetBackUpsAll();

json_body = [];
for node in nodes:
	name = node["name"]
	state = node["state"]
	model = node["model"]
	mgtIP = node["management_ip"]
	storageIP = node["storage_ip"]
	version = node["version"]
	vmData=float("{0:.2f}".format(node["stored_virtual_machine_data"]/pow(1024.0,4)));
	localBackup = float("{0:.2f}".format(node["local_backup_capacity"]/pow(1024.0,4)));
	remoteBackup = float("{0:.2f}".format(node["remote_backup_capacity"]/pow(1024.0,4)));
	usedCapacity = float("{0:.2f}".format(node["used_capacity"]/pow(1024.0,4)));
	freeCapacity = float("{0:.2f}".format(node["free_space"]/pow(1024.0,4)));
	dedupe = node["deduplication_ratio"].split(":");
	dedupeRatio = float(dedupe[0]);
	compress = node["compression_ratio"].split(":");
	compressRatio = float(compress[0]);
	reduct = node["efficiency_ratio"].split(":");
	reductRatio = float(reduct[0]);
	data =	{"measurement": 'simplivityNode',
        	"tags": {
        	    "hostname": node["name"]
        	},
        	"time": str(now),
        	"fields": {
        	    	"name":name,
			"state":state,
			"model":model,
			"mgtIP":mgtIP,
			"storageIP":storageIP,
			"version":version,
			"vmData":vmData,
			"localBackup":localBackup,
			"remoteBackup":remoteBackup,
			"usedCapacity":usedCapacity,
			"freeCapacity":freeCapacity,
			"dedupeRatio":dedupeRatio,
			"compressRatio":compressRatio,
			"reductRatio":reductRatio
        	}
   	}
	json_body.append(data);

for cluster in clusters:
	data =  {"measurement": 'simplivityCluster',
                "tags": {
                    "hostname": cluster['name']
                },
                "time": str(now),
                "fields": {
			"name": cluster["name"],
			"vmData":float("{0:.2f}".format(cluster["stored_virtual_machine_data"]/pow(1024.0,4))),
			"localBackup": float("{0:.2f}".format(cluster["local_backup_capacity"]/pow(1024.0,4))),
			"remoteBackup": float("{0:.2f}".format(cluster["remote_backup_capacity"]/pow(1024.0,4))),
			"usedCapacity": float("{0:.2f}".format(cluster["used_capacity"]/pow(1024.0,4))),
			"freeCapacity": float("{0:.2f}".format(cluster["free_space"]/pow(1024.0,4))),
			"dedupeRatio": float(cluster["deduplication_ratio"].split(":")[0]),
			"compressRatio": float(cluster["compression_ratio"].split(":")[0]),
			"reductRatio": float(cluster["efficiency_ratio"].split(":")[0])
		}
	}
	json_body.append(data);

for backup in backups:
	createTime = time.strptime(backup['created_at'], '%Y-%m-%dT%H:%M:%SZ')
	if backup['expiration_time'] == "NA":
		retentionDay = -1;
	else:
		expiredTime = time.strptime(backup['expiration_time'], '%Y-%m-%dT%H:%M:%SZ')
		createTime = time.mktime(createTime);
		expiredTime = time.mktime(expiredTime);
		diff = expiredTime - createTime;
		retentionDay = int(diff) / 86400;
	data = {"measurement": 'simplivityBackup',
		"tags": {
			"state": backup['state'],
			"virtual_machine_name" : backup['virtual_machine_name']
		},
		"time":backup['created_at'],
		"fields": {
			'sent_duration': backup['sent_duration'],
			'id': backup['id'],
			'omnistack_cluster_id': backup['omnistack_cluster_id'],
			'size': backup['size'],
			'state': backup['state'],
			'expiration_time': backup['expiration_time'],
			'sent': backup['sent'],
			'virtual_machine_name': backup['virtual_machine_name'],
			'name': backup['name'],
			'type': backup['type'],
			'created_at': backup['created_at'],
			'datastore_name': backup['datastore_name'],
			'omnistack_cluster_name': backup['omnistack_cluster_name'],
			'retentionDay':retentionDay
		}
	}
	json_body.append(data);

if json_body == []:
	print("Cannot connect to " + OVC_IP);
else:
	result = client.write_points(json_body, database=INFLUX_DB);
	if result == True:
		print("Add successful to " + INFLUX_DB);
	else:
		print("Failed to add data to " + INFLUX_DB);

