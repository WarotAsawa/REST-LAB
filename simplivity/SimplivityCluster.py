#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from RestObject import RestObject;
import request;

#Begin class
class SimplivityCluster(RestObject):

  	def __init__(self, ip, user, password):
		self.object_label = "Simplivity Cluster";
		super(SimplivityCluster,self).__init__(ip, user, password);

	def Initialize(self):
		''' Simplvity Omni stack authentication'''

		#Set Simplivity REST API URL
		self.url = "https://" + self.auth_ip + "/api/";
		
		#LOGIN check
		try:
			output = request.post(self.url+'oauth/token', auth=('simplivity', ''), verify=False, data={'grant_type':'password','username':self.auth_username,'password':self.auth_password});
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

	def GetDatastores(self):
		'''Get DataStore methods, returning list of Simplivity datastores'''
		# Get host jsons
		dsList = self.Get("datastores", {"show_optional_fields":"true"});
		# Return if null 
		if dsList == {}:
			return {};
		return dsList['datastores'];

	def PrintDatastores(self):
		'''Print all DataStores' detail.'''

		dsList = self.GetDatastores();
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

	def GetHosts(self):
		'''Get hosts method, returning list of Simplivity hosts'''

		# Get host jsons
		hostList = self.Get("hosts", {"show_optional_fields":"true"});
		# Return if null 
		if hostList == {}:
			return {};
		return hostList["hosts"];

	def PrintHosts(self):
		'''Print all hosts' detail.'''

		hostList = self.GetHosts();
		if hostList == {}:
			return;
		#Print results
		print("\n===========================================\n");
		for host in hostList:
			printout = "";
			printout += "Name: " + 			str(host['name']) + 			"\n";			
			printout += "Model: " + 		str(host['model']) + 			"\n";
			printout += "Management IP: " + str(host['management_ip']) + 	"\n";
			printout += "Storage IP: " + 	str(host["storage_ip"]) + 		"\n";
			printout += "Version: " + 		str(host["version"]) + 			"\n";
			print(printout);
			print("===========================================\n");


	def GetBackUps(self):
		'''Get backups method'''
		# Get host jsons
		backupList = self.Get("backups");
		# Return if null 
		if backupList == {}:
			return {};
		return backupList['backups'];

	def PrintBackUps(self):
		'''Print backups method'''
		backupList = self.GetBackUps();
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
			print(printout);
			print("===========================================\n");

	def BackupStateSummary(self):
		'''Summary of all Backup's States'''
		backupList = self.GetBackUps();
		if backupList == {}:
			return;

		resultList = {};
		outputText = "\nBackup summary of OmniStack Cluster " + self.auth_ip + " is : \n";

		#Check every Backup state and add counts
		for backup in backupList:
			if (backup['state'] in resultList):
				print(resultList[backup['state']])
				resultList[backup['state']] += 1;
			else:
				resultList[backup['state']] = 0;

		#Print all State results
		for result in resultList:
			outputText += result + " : " + str(resultList[result]) + "\n";

		outputText += "\n";

		print(outputText);

	