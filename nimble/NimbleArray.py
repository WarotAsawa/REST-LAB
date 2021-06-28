from nimbleclient import NimOSClient
import csv
import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "my-bucket"

client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
now = datetime.datetime.now()
nimbleArray = '172.30.4.80'
nimbleUsername = 'admin'
nimblePassword = 'password'
api = NimOSClient(nimbleArray, nimbleUsername, nimblePassword)

allFolder = {};
allVol = {};
pulledVol = api.volumes.list()
#print(pulledVol)
for vol in pulledVol:
  volID =  vol.attrs['id']
  volDetail = api.volumes.get(volID).attrs
  #print(volDetail)
  volName               = volDetail["name"]
  volFolder             = volDetail["folder_name"]
  allVol[volName] = {}
  allVol[volName]["vol_usage_uncompressed_GiB"]  = volDetail["vol_usage_uncompressed_bytes"]/1024/1024/1024
  allVol[volName]["vol_usage_compressed_GiB"]    = volDetail["vol_usage_compressed_bytes"]/1024/1024/1024
  allVol[volName]["snap_usage_uncompressed_GiB"] = volDetail["snap_usage_uncompressed_bytes"]/1024/1024/1024
  allVol[volName]["snap_usage_compressed_GiB"]   = volDetail["snap_usage_compressed_bytes"]/1024/1024/1024
  allVol[volName]["size_GiB"]                    = volDetail["size"]/1024
  allVol[volName]["read_iops"]                   = volDetail["read_iops"]
  allVol[volName]["read_throughput"]             = volDetail["read_throughput"]
  allVol[volName]["read_latency"]                = volDetail["read_latency"]
  allVol[volName]["write_iops"]                  = volDetail["write_iops"]
  allVol[volName]["write_throughput"]            = volDetail["write_throughput"]
  allVol[volName]["write_latency"]               = volDetail["write_latency"]
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
    allFolder[volFolder]["volList"].append(volName)
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
    allFolder[volFolder]["volList"] = [volName]


