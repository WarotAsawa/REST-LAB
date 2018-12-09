#Import sections
import sys;
#Change sys.path directory
sys.path.insert(0, "../lib");
from RestObject import RestObject;
import requests;

#Begin class
class SimplivityCluster(RestObject):

  	def __init__(self, ip, user, password):
		self.auth_ip = ip;
		self.auth_username = user;
		self.auth_password = password;
		self.object_label = "Simplivity Cluster";

	# Simplvity Omni stack authentication
	def Initialize(self):

		#Set Simplivity REST API URL
		self.url = "https://" + self.auth_ip + "/api/";
		
		#LOGIN check
		try:
			output = requests.post(self.url+'oauth/token', auth=('simplivity', ''), verify=False, data={'grant_type':'password','username':self.auth_username,'password':self.auth_password});
		except:
			print("\nFailed to authenticated with ERROR :");
			print("Omnistack controller: " + self.auth_ip + " is not reachable!\n");
			return;

		#Check if valid Omnistack controller 
		try:
			response = output.json();
		#and Convert Output to Response
		except:
			print("\nFailed to authenticated with ERROR :");
			print("Omnistack controller: " + self.auth_ip + " is not a valid controller!\n");
			return;
		
		#Check if error
		if "error" in response:
			print("\nFailed to authenticated with ERROR :");
			print(response["message"]);
			print("\n");

		#Get Access Token
		if "access_token" in response:
			self.access_token = response["access_token"];
			self.headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1+json'};
			print("Omnistack cluster: " + self.auth_ip + " sucessfully authenicated!\n");

	#Get DataStore methods
	def GetDatastores(self):
		# Get host jsons
		dsList = self.Get("datastores?show_optional_fields=true");
		# Return if null 
		if dsList == {}:
			return;
		#Print results
		print("\n===========================================\n");
		for ds in dsList['datastores']:
			printout = "";
			printout += "Name: " + ds['name'] + "\n";			
			printout += "Size: " + str(ds['size']) + "\n";
			printout += "Backup Policy: " + ds['policy_name'] + "\n";
			printout += "Deleted: " + str(ds["deleted"]) + "\n";
			printout += "Cluster: " + ds["compute_cluster_parent_name"] + "\n";
			print(printout);
			print("===========================================\n");

	#Get hosts method
	def GetHosts(self):
		# Get host jsons
		hostList = self.Get("hosts?show_optional_fields=true");
		# Return if null 
		if hostList == {}:
			return;
		#Print results
		print("\n===========================================\n");
		for host in hostList['hosts']:
			printout = "";
			printout += "Name: " + host['name'] + "\n";			
			printout += "Model: " + host['model'] + "\n";
			printout += "Management IP: " + host['management_ip'] + "\n";
			printout += "Storage IP: " + host["storage_ip"] + "\n";
			printout += "Version: " + host["version"] + "\n";
			print(printout);
			print("===========================================\n");

	