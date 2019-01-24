#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from Time import Time;
from RestObject import RestObject;
import requests;
#---------------------------------------------------------------------

#Begin class
class NimbleArray(RestObject):

	#Bunch of Array's parameter;

	self.id                         = "";
	self.name                       = "";
	self.force                      = "";  
	self.full_name                  = "";     
	self.search_name                = "";        
	self.status                     = "";  
	self.role                       = "";
	self.pool_name                  = "";     
	self.pool_id                    = "";  
	self.model                      = "";  
	self.serial                     = "";  
	self.version                    = "";  
	self.creation_time              = "";        
	self.last_modified              = "";        
	self.usage_valid                = "";        
	self.usable_capacity_bytes      = "";                 
	self.raw_capacity_bytes         = "";              
	self.vol_usage_bytes            = "";           
	self.vol_compression            = "";           
	self.vol_saved_bytes            = "";           
	self.snap_usage_bytes           = "";           
	self.snap_compression           = "";           
	self.snap_space_reduction       = "";                 
	self.snap_saved_bytes           = "";           
	self.pending_delete_bytes       = "";                 
	self.available_bytes            = "";           
	self.usage                      = "";  
	self.all_flash                  = "";     
	self.dedupe_capacity_bytes      = "";                 
	self.dedupe_usage_bytes         = "";              
	self.extended_model             = "";           
	self.is_supported_hw_config     = "";                 
	self.gig_nic_port_count         = "";              
	self.ten_gig_sfp_nic_port_count = "";                       
	self.ten_gig_t_nic_port_count   = "";                    
	self.fc_port_count              = "";        
	self.create_pool                = "";        
	self.pool_description           = "";           
	self.ctrlr_a_support_ip         = "";              
	self.ctrlr_b_support_ip         = ""; 

	#Directory of Nimble's Certificate file
	cafile = "";
	versions = "";
	name = "";
  	def __init__(self, ip, user, password, cafile):
		self.object_label = "Simplivity Cluster";
		self.cafile = cafile;
		super(SimplivityCluster,self).__init__(ip, user, password);

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
		self.versions = response["data"]["name"];
		self.url = self.url + self.versions + "/";

		#LOGIN check and Get Response
		auth_input = {};
		auth_input["data"]["username"] = self.auth_username;
		auth_input["data"]["password"] = self.auth_password;
		response = self.Post('token', None, self.cafile, auth_input);
		
		#Check if error
		if ("error" in response) or (response == {}):
			return;

		#Get Access Token
		if "access_token" in response:
			self.access_token = response["data"]["session_token"];
			self.headers = {'X-Auth-Token':  self.access_token};
			print("Nimble Array: " + self.auth_ip + " sucessfully authenicated!\n");

		#Get Nimble Array name:
		response = self.Get("array");
		result = response["data"][0];
		self.UpdateParameter(result);

	def PrintNimbleCapacity(self):
		print("Array name : ") + 		str(self.name);
		print("Raw Capacity : ") + 		str(self.raw_capacity_bytes/pow(1024.0,4)) + " TiB";
		print("Usable Capcity : ") +	str(self.usable_capacity_bytes/pow(1024.0,4)) + " TiB";
		print("Volume Usage : ") + 		str(self.vol_usage_bytes/pow(1024.0,4)) + " TiB";
		print("Snapshot Usage : ") + 	str(self.snap_usage_bytes/pow(1024.0,4)) + " TiB";
		print("Volume Compression : ") + 	str(self.snap_usage_bytes/pow(1024.0,4)) + " TiB";
		print("Snapsgit Usage : ") + 	str(self.snap_usage_bytes/pow(1024.0,4)) + " TiB";


	def UpdateParameter(self, result):
		self.id                         = result["id"];
		self.name                       = result["name"];
		self.force                      = result["force"];
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
		self.create_pool                = result["create_pool"];
		self.pool_description           = result["pool_description"];
		self.ctrlr_a_support_ip         = result["ctrlr_a_support_ip"];
		self.ctrlr_b_support_ip         = result["ctrlr_b_support_ip"];
		