from nimbleclient import NimOSClient

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "jmXujLPq0rE1QRIOGVxBS-9ZXtYJMeZwkhGGxrrsSFHDw_KaGe2yNYlbwrX0x5mNm-ugIduA-IS7LQMZjey47Q=="
org = "gotham"
bucket = "gotham-bucket"
#Login to InfluxDB
client = InfluxDBClient(url="http://influxdb.ezmeral.hpe.lab", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

now = datetime.utcnow()


#Nimble Credential
nimbleArray = '172.30.4.80'
nimbleUsername = 'admin'
nimblePassword = 'password'
#Login to Nimble Array
nimbleClient = NimOSClient(nimbleArray, nimbleUsername, nimblePassword)

#Query all Nimble Vol's detial via API
allFolder = {};
allVol = {};
pulledVol = nimbleClient.volumes.list()
#print(pulledVol)
for vol in pulledVol:
  volID =  vol.attrs['id']
  volDetail = nimbleClient.volumes.get(volID).attrs
  #print(volDetail)
  volName               = volDetail["name"]
  volFolder             = volDetail["folder_name"]
  allVol[volName] = {}
  allVol[volName]["vol_usage_uncompressed_GiB"]  = float(volDetail["vol_usage_uncompressed_bytes"]/1024/1024/1024)
  allVol[volName]["vol_usage_compressed_GiB"]    = float(volDetail["vol_usage_compressed_bytes"]/1024/1024/1024)
  allVol[volName]["snap_usage_uncompressed_GiB"] = float(volDetail["snap_usage_uncompressed_bytes"]/1024/1024/1024)
  allVol[volName]["snap_usage_compressed_GiB"]   = float(volDetail["snap_usage_compressed_bytes"]/1024/1024/1024)
  allVol[volName]["size_GiB"]                    = float(volDetail["size"]/1024)
  allVol[volName]["read_iops"]                   = int(volDetail['avg_stats_last_5mins']["read_iops"])
  allVol[volName]["read_throughput"]             = float(volDetail['avg_stats_last_5mins']["read_throughput"])
  allVol[volName]["read_latency"]                = float(volDetail['avg_stats_last_5mins']["read_latency"])
  allVol[volName]["write_iops"]                  = int(volDetail['avg_stats_last_5mins']["write_iops"])
  allVol[volName]["write_throughput"]            = float(volDetail['avg_stats_last_5mins']["write_throughput"])
  allVol[volName]["write_latency"]               = float(volDetail['avg_stats_last_5mins']["write_latency"])
  #All data kept in GiB. Size returned as MiB. Used return as Bytes
  if volFolder in allFolder:
    allFolder[volFolder]["vol_usage_uncompressed_GiB"]  += allVol[volName]["vol_usage_uncompressed_GiB"]  
    allFolder[volFolder]["vol_usage_compressed_GiB"]    += allVol[volName]["vol_usage_compressed_GiB"]    
    allFolder[volFolder]["snap_usage_uncompressed_GiB"] += allVol[volName]["snap_usage_uncompressed_GiB"] 
    allFolder[volFolder]["snap_usage_compressed_GiB"]   += allVol[volName]["snap_usage_compressed_GiB"]   
    allFolder[volFolder]["size_GiB"]                    += allVol[volName]["size_GiB"]                    
    allFolder[volFolder]["read_iops"]                   += allVol[volName]["read_iops"]                   
    allFolder[volFolder]["read_throughput"]             += allVol[volName]["read_throughput"]             
    allFolder[volFolder]["read_latency"]                += allVol[volName]["read_latency"]                
    allFolder[volFolder]["write_iops"]                  += allVol[volName]["write_iops"]                  
    allFolder[volFolder]["write_throughput"]            += allVol[volName]["write_throughput"]            
    allFolder[volFolder]["write_latency"]               += allVol[volName]["write_latency"]               
    #allFolder[volFolder]["volList"].append(volName)
  else:
    allFolder[volFolder] = {}
    allFolder[volFolder]["vol_usage_uncompressed_GiB"]  = allVol[volName]["vol_usage_uncompressed_GiB"]  
    allFolder[volFolder]["vol_usage_compressed_GiB"]    = allVol[volName]["vol_usage_compressed_GiB"]    
    allFolder[volFolder]["snap_usage_uncompressed_GiB"] = allVol[volName]["snap_usage_uncompressed_GiB"] 
    allFolder[volFolder]["snap_usage_compressed_GiB"]   = allVol[volName]["snap_usage_compressed_GiB"]   
    allFolder[volFolder]["size_GiB"]                    = allVol[volName]["size_GiB"]                    
    allFolder[volFolder]["read_iops"]                   = allVol[volName]["read_iops"]                   
    allFolder[volFolder]["read_throughput"]             = allVol[volName]["read_throughput"]             
    allFolder[volFolder]["read_latency"]                = allVol[volName]["read_latency"]                
    allFolder[volFolder]["write_iops"]                  = allVol[volName]["write_iops"]                  
    allFolder[volFolder]["write_throughput"]            = allVol[volName]["write_throughput"]            
    allFolder[volFolder]["write_latency"]               = allVol[volName]["write_latency"]               
    #allFolder[volFolder]["volList"] = [volName]

#print(allVol)
#print(allFolder)

for vol in allVol:
  write_api.write(bucket, org, {"measurement": "volDetail", "tags": {"array": "172.30.4.80", "volName":vol},"fields": allVol[vol], "time": now}) 

for folder in allFolder:
  write_api.write(bucket, org, {"measurement": "folderDetail", "tags": {"array": "172.30.4.80", "folderName":folder},"fields": allFolder[folder], "time": now})
 
