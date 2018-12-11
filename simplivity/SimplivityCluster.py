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
class SimplivityCluster(RestObject):

  	def __init__(self, ip, user, password):
		self.object_label = "Simplivity Cluster";
		super(SimplivityCluster,self).__init__(ip, user, password);

	def Initialize(self):
		''' Simplvity Omni stack authentication'''

		#Set Simplivity REST API URL
		self.url = "https://" + self.auth_ip + "/api/";
		
		#LOGIN check and Get Response
		response = self.Post(self.url+'oauth/token', ('simplivity', ''), False, {'grant_type':'password','username':self.auth_username,'password':self.auth_password});
		
		#Check if error
		if ("error" in response) or (response == {}):
			print("\nFailed to authenticated with ERROR :");
			print(response["message"]);
			print("\n");

		#Get Access Token
		if "access_token" in response:
			self.access_token = response["access_token"];
			self.headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1+json'};
			print("\nOmnistack cluster: " + self.auth_ip + " sucessfully authenicated!\n");

	def GetDatastoresAll(self):
		'''Get DataStore methods, returning list of Simplivity datastores'''
		# Get host jsons
		dsList = self.Get("datastores", {"show_optional_fields":"true"});
		# Return if null 
		if dsList == {}:
			return {};
		return dsList['datastores'];

	def PrintDatastoresAll(self):
		'''Print all DataStores' detail.'''

		dsList = self.GetDatastoresAll();
		if dsList == {}:
			return;

		#Print results
		print("\n===========================================\n");
		for ds in dsList:
			printout = "";
			printout += "Name: " + 			str(ds['name']) + "\n";			
			printout += "Size: " + 			str(ds['size']) + "\n";
			printout += "Backup Policy: " + str(ds['policy_name']) + "\n";
			printout += "Deleted: " + 		str(ds["deleted"]) + "\n";
			printout += "Cluster: " + 		str(ds["compute_cluster_parent_name"]) + "\n";
			print(printout);
			print("===========================================\n");

	def GetHostsAll(self):
		'''Get hosts method, returning list of Simplivity hosts'''

		# Get host jsons
		hostList = self.Get("hosts", {"show_optional_fields":"true"});
		# Return if null 
		if hostList == {}:
			return {};
		return hostList["hosts"];

	def PrintHostsAll(self):
		'''Print all hosts' detail.'''

		hostList = self.GetHostsAll();
		if hostList == {}:
			return;
		#Print results
		print("\n===========================================\n");
		for host in hostList:
			printout = "";
			printout += "Name: " + 			str(host['name']) + 			"\n";	
			printout += "Status: " + 		str(host['state']) + 			"\n";			
			printout += "Model: " + 		str(host['model']) + 			"\n";
			printout += "Management IP: " + str(host['management_ip']) + 	"\n";
			printout += "Storage IP: " + 	str(host["storage_ip"]) + 		"\n";
			printout += "Version: " + 		str(host["version"]) + 			"\n";
			printout += "Capacity: " + 		str(host["allocated_capacity"]/pow(1024.0,4)) + 	" TiB\n";
			printout += "Used Capacity: " + str(host["used_capacity"]/pow(1024.0,4)) + 	" TiB\n";
			print(printout);
			print("===========================================\n");

	def GetBackUpsAll(self):
		'''Get backups method'''
		# Get host jsons
		backupList = self.Get("backups");
		# Return if null 
		if backupList == {}:
			return {};
		return backupList['backups'];

	def PrintBackUpsAll(self):
		'''Print backups method'''
		backupList = self.GetBackUpsAll();
		if backupList == {}:
			return;
		#Print results
		print("\n===========================================\n");
		for backup in backupList:
			printout = "";
			printout += "Name: " + 	str(backup['name']) + "\n";			
			printout += "Type: " + 	str(backup['type']) + "\n";
			printout += "Size: " + 	str(backup['size']) + "\n";
			printout += "Sent: " + 	str(backup["sent"]) + "\n";
			printout += "State: " + str(backup["state"]) + "\n";
			printout += "Created At: " + str(backup["created_at"]) + "\n";
			print(printout);
			print("===========================================\n");

	def BackUpsSummaryAll(self):
		'''Summary of all Backup's States'''
		backupList = self.GetBackUpsAll();
		if backupList == {}:
			return;

		resultList = {};
		outputText = "\nBackup summary of OmniStack Cluster " + self.auth_ip + " is : \n";

		#Check every Backup state and add counts
		for backup in backupList:
			if (backup['state'] in resultList):
				resultList[backup['state']] += 1;
			else:
				resultList[backup['state']] = 0;

		#Print all State results
		for result in resultList:
			outputText += result + " : " + str(resultList[result]) + "\n";

		outputText += "\n";

		print(outputText);

	def GetBackUpsFrom(self, time):
		'''Get backups method'''
		# Get host jsons
		backupList = self.Get("backups",{'created_after':Time.GetInstance().UTCToISO(time)});
		# Return if null 
		if backupList == {}:
			return {};
		return backupList['backups'];

	def BackUpsSummaryFrom(self,time):
		'''Summary of all Backup's States'''
		backupList = self.GetBackUpsFrom(time);
		if backupList == {}:
			return;

		resultList = {};
		outputText = "\nBackup summary of OmniStack Cluster " + self.auth_ip + " from : " + str(time) + " is : \n";

		#Check every Backup state and add counts
		for backup in backupList:
			if (backup['state'] in resultList):
				resultList[backup['state']] += 1;
			else:
				resultList[backup['state']] = 0;

		#Print all State results
		for result in resultList:
			outputText += result + " : " + str(resultList[result]) + "\n";

		outputText += "\n";

		print(outputText);