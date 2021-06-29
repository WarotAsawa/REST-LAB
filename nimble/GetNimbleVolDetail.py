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
nimbleArrays = ['172.30.4.80', '172.30.4.85']
nimbleUsername = 'influxdbquery'
nimblePassword = 'P@ssw0rd'

for nimbleArray in nimbleArrays:
  #Login to Nimble Array
  nimbleClient = NimOSClient(nimbleArray, nimbleUsername, nimblePassword)
  #Get Array Name
  array = nimbleClient.arrays
  arrayName = array.list()[0].attrs['name']
  #Query all Nimble Vol's detial via API
  pulledVol = nimbleClient.volumes.list()

  result = GetVolFolList(pulledVol)
  allVol = result["allVol"]
  allFolder = result["allFolder"]
  
  for vol in allVol:
    write_api.write(bucket, org, {"measurement": "volDetail", "tags": {"array": arrayName, "volName":vol},"fields": allVol[vol], "time": now}) 

  for folder in allFolder:
    write_api.write(bucket, org, {"measurement": "folderDetail", "tags": {"array": arrayName, "folderName":folder},"fields": allFolder[folder], "time": now})
   


def GetVolFolList(pulledVol):
  result = {};
  result["allVol"] = {}
  result["allFolder"] = {}
  #print(pulledVol)
  for vol in pulledVol:
    volID =  vol.attrs['id']
    volDetail = nimbleClient.volumes.get(volID).attrs
    #print(volDetail)
    volName               = volDetail["name"]
    volFolder             = volDetail["folder_name"]
    result["allVol"][volName] = {}
    result["allVol"][volName]["vol_usage_uncompressed_GiB"]  = float(volDetail["vol_usage_uncompressed_bytes"]/1024/1024/1024)
    result["allVol"][volName]["vol_usage_compressed_GiB"]    = float(volDetail["vol_usage_compressed_bytes"]/1024/1024/1024)
    result["allVol"][volName]["snap_usage_uncompressed_GiB"] = float(volDetail["snap_usage_uncompressed_bytes"]/1024/1024/1024)
    result["allVol"][volName]["snap_usage_compressed_GiB"]   = float(volDetail["snap_usage_compressed_bytes"]/1024/1024/1024)
    result["allVol"][volName]["size_GiB"]                    = float(volDetail["size"]/1024)
    result["allVol"][volName]["read_iops"]                   = int(volDetail['avg_stats_last_5mins']["read_iops"])
    result["allVol"][volName]["read_throughput"]             = float(volDetail['avg_stats_last_5mins']["read_throughput"])
    result["allVol"][volName]["read_latency"]                = float(volDetail['avg_stats_last_5mins']["read_latency"])
    result["allVol"][volName]["write_iops"]                  = int(volDetail['avg_stats_last_5mins']["write_iops"])
    result["allVol"][volName]["write_throughput"]            = float(volDetail['avg_stats_last_5mins']["write_throughput"])
    result["allVol"][volName]["write_latency"]               = float(volDetail['avg_stats_last_5mins']["write_latency"])
    #All data kept in GiB. Size returned as MiB. Used return as Bytes
    if volFolder in allFolder:
      result["allFolder"][volFolder]["vol_usage_uncompressed_GiB"]  += allVol[volName]["vol_usage_uncompressed_GiB"]  
      result["allFolder"][volFolder]["vol_usage_compressed_GiB"]    += allVol[volName]["vol_usage_compressed_GiB"]    
      result["allFolder"][volFolder]["snap_usage_uncompressed_GiB"] += allVol[volName]["snap_usage_uncompressed_GiB"] 
      result["allFolder"][volFolder]["snap_usage_compressed_GiB"]   += allVol[volName]["snap_usage_compressed_GiB"]   
      result["allFolder"][volFolder]["size_GiB"]                    += allVol[volName]["size_GiB"]                    
      result["allFolder"][volFolder]["read_iops"]                   += allVol[volName]["read_iops"]                   
      result["allFolder"][volFolder]["read_throughput"]             += allVol[volName]["read_throughput"]             
      result["allFolder"][volFolder]["read_latency"]                += allVol[volName]["read_latency"]                
      result["allFolder"][volFolder]["write_iops"]                  += allVol[volName]["write_iops"]                  
      result["allFolder"][volFolder]["write_throughput"]            += allVol[volName]["write_throughput"]            
      result["allFolder"][volFolder]["write_latency"]               += allVol[volName]["write_latency"]               
    else:
      result["allFolder"][volFolder] = {}
      result["allFolder"][volFolder]["vol_usage_uncompressed_GiB"]  = allVol[volName]["vol_usage_uncompressed_GiB"]  
      result["allFolder"][volFolder]["vol_usage_compressed_GiB"]    = allVol[volName]["vol_usage_compressed_GiB"]    
      result["allFolder"][volFolder]["snap_usage_uncompressed_GiB"] = allVol[volName]["snap_usage_uncompressed_GiB"] 
      result["allFolder"][volFolder]["snap_usage_compressed_GiB"]   = allVol[volName]["snap_usage_compressed_GiB"]   
      result["allFolder"][volFolder]["size_GiB"]                    = allVol[volName]["size_GiB"]                    
      result["allFolder"][volFolder]["read_iops"]                   = allVol[volName]["read_iops"]                   
      result["allFolder"][volFolder]["read_throughput"]             = allVol[volName]["read_throughput"]             
      result["allFolder"][volFolder]["read_latency"]                = allVol[volName]["read_latency"]                
      result["allFolder"][volFolder]["write_iops"]                  = allVol[volName]["write_iops"]                  
      result["allFolder"][volFolder]["write_throughput"]            = allVol[volName]["write_throughput"]            
      result["allFolder"][volFolder]["write_latency"]               = allVol[volName]["write_latency"]               

  #print(allVol)
  #print(allFolder)
  return result
