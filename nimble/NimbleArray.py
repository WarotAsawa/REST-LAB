#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from Time import Time;
from RestObject import RestObject;
import requests;
import json;
#---------------------------------------------------------------------

#Begin class
class NimbleArray(RestObject):

	#Bunch of Array's parameter;

	id                         = "";
	name                       = "";
	force                      = "";  
	full_name                  = "";     
	search_name                = "";        
	status                     = "";  
	role                       = "";
	pool_name                  = "";     
	pool_id                    = "";  
	model                      = "";  
	serial                     = "";  
	version                    = "";  
	creation_time              = "";        
	last_modified              = "";        
	usage_valid                = "";        
	usable_capacity_bytes      = "";                 
	raw_capacity_bytes         = "";              
	vol_usage_bytes            = "";           
	vol_compression            = "";           
	vol_saved_bytes            = "";           
	snap_usage_bytes           = "";           
	snap_compression           = "";           
	snap_space_reduction       = "";                 
	snap_saved_bytes           = "";           
	pending_delete_bytes       = "";                 
	available_bytes            = "";           
	usage                      = "";  
	all_flash                  = "";     
	dedupe_capacity_bytes      = "";                 
	dedupe_usage_bytes         = "";              
	extended_model             = "";           
	is_supported_hw_config     = "";                 
	gig_nic_port_count         = "";              
	ten_gig_sfp_nic_port_count = "";                       
	ten_gig_t_nic_port_count   = "";                    
	fc_port_count              = "";        
	create_pool                = "";        
	pool_description           = "";           
	ctrlr_a_support_ip         = "";              
	ctrlr_b_support_ip         = ""; 

	#Directory of Nimble's Certificate file
	cafile = "";
	versions = "";
	name = "";

  	def __init__(self, ip, user, password, cafile):
		self.object_label = "Nimble Array";
		self.cafile = cafile;
		super(NimbleArray,self).__init__(ip, user, password);

	def Initialize(self):
		''' Nimble Array authentication'''

		#Set Nimble Array REST API URL
		self.url = "https://" + self.auth_ip + ":5392/";
		
		#Get Nimble Array's version
		response = self.Get('versions');
		if response == {}:
			print("Cannot get Nimble's API version !!\n");
			return;
		#Update URL with version number
		self.versions = response["data"][0]["name"];
		self.url = self.url + self.versions + "/";

		#LOGIN check and Get Response
		auth_input = {};
		auth_input["data"] = {};
		auth_input["data"]["username"] = self.auth_username;
		auth_input["data"]["password"] = self.auth_password;
		auth_input = json.dumps(auth_input);

		response = self.Post('tokens', None, False, auth_input);

		#Check if error
		if ("error" in response) or (response == {}):
			return;

		#Get Access Token
		if "session_token" in response["data"]:
			self.access_token = response["data"]["session_token"];
			self.headers = {'X-Auth-Token':  self.access_token};
			print("Nimble Array: " + self.auth_ip + " sucessfully authenicated!\n");

		#Get Nimble Array name:
		response = self.Get("arrays/detail");
		result = response["data"][0];
		self.UpdateParameter(result);

	def PrintNimbleCapacity(self):
		print("Array name : ") + 		str(self.name);
		print("Raw Capacity : ") + 		str(round(self.raw_capacity_bytes/pow(1024.0,4),3)) + " TiB";
		print("Usable Capcity : ") +	str(round(self.usable_capacity_bytes/pow(1024.0,4),3)) + " TiB";
		print("Volume Usage : ") + 		str(round(self.vol_usage_bytes/pow(1024.0,4),3)) + " TiB";
		print("Snapshot Usage : ") + 	str(round(self.snap_usage_bytes/pow(1024.0,4),3)) + " TiB";
		print("Volume Compression : ") +str(round(self.snap_usage_bytes/pow(1024.0,4),3)) + " TiB";
		print("Snapsgit Usage : ") + 	str(round(self.snap_usage_bytes/pow(1024.0,4),3)) + " TiB";


	def UpdateParameter(self, result):
		self.id                         = result["id"];
		self.name                       = result["name"];
		self.full_name                  = result["full_name"];
		self.search_name                = result["search_name"];
		self.status                     = result["status"];
		self.role                       = result["role"];
		self.pool_name                  = result["pool_name"];
		self.pool_id                    = result["pool_id"];
		self.model                      = result["model"];
		self.serial                     = result["serial"];
		self.version                    = result["version"];
		self.creation_time              = result["creation_time"];
		self.last_modified              = result["last_modified"];
		self.usage_valid                = result["usage_valid"];
		self.usable_capacity_bytes      = result["usable_capacity_bytes"];
		self.raw_capacity_bytes         = result["raw_capacity_bytes"];
		self.vol_usage_bytes            = result["vol_usage_bytes"];
		self.vol_compression            = result["vol_compression"];
		self.vol_saved_bytes            = result["vol_saved_bytes"];
		self.snap_usage_bytes           = result["snap_usage_bytes"];
		self.snap_compression           = result["snap_compression"];
		self.snap_space_reduction       = result["snap_space_reduction"];
		self.snap_saved_bytes           = result["snap_saved_bytes"];
		self.pending_delete_bytes       = result["pending_delete_bytes"];
		self.available_bytes            = result["available_bytes"];
		self.usage                      = result["usage"];
		self.all_flash                  = result["all_flash"];
		self.dedupe_capacity_bytes      = result["dedupe_capacity_bytes"];
		self.dedupe_usage_bytes         = result["dedupe_usage_bytes"];
		self.extended_model             = result["extended_model"];
		self.is_supported_hw_config     = result["is_supported_hw_config"];
		self.gig_nic_port_count         = result["gig_nic_port_count"];
		self.ten_gig_sfp_nic_port_count = result["ten_gig_sfp_nic_port_count"];
		self.ten_gig_t_nic_port_count   = result["ten_gig_t_nic_port_count"];
		self.fc_port_count              = result["fc_port_count"];