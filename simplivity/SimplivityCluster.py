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
		response = self.Post('oauth/token', ('simplivity', ''), False, {'grant_type':'password','username':self.auth_username,'password':self.auth_password});
		
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

	def GetVMsAll(self):
		'''Get VMs methods, returning list of Simplivity VMs'''
		# Get host jsons
		dsList = self.Get("virtual_machines", {"show_optional_fields":"true"});
		# Return if null 
		if dsList == {}:
			return {};
		return dsList['virtual_machines'];

	def PrintVMsAll(self):
		'''Print all VMs' detail.'''

		dsList = self.GetVMsAll();
		if dsList == {}:
			return;

		#Print results
		print("\n===========================================\n");
		for ds in dsList:
			printout = "";
			printout += "Name: " + 			str(ds['name']) + "\n";			
			printout += "DataStore: " + 	str(ds['datastore_name']) + "\n";
			printout += "Backup Policy: " + str(ds['policy_name']) + "\n";
			printout += "State: " + 		str(ds["state"]) + "\n";
			printout += "Host: " + 			str(ds["host_id"]) + "\n";
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

	def CloneVM(self,old_vm_name ,new_vm_name):
		''' Clone existing VM to new VM '''
		vmList = self.Get("virtual_machines", {"name": old_vm_name});
		if (vmList == {}):
			#Print error if there is no VM
			print ("\nCannot find VM named " + old_vm_name + " in Simplivity " + self.auth_ip);
			return;
		vm = vmList["virtual_machines"][0];
		#Set URL for POST
		cloneUrl = "virtual_machines/" + vm["id"] + "/clone";
		#Set Cloning parameters, content type and Payloads
		header = self.headers;
		header['content-type'] = 'application/vnd.simplivity.v1+json';
		payload = '{"virtual_machine_name":"' + new_vm_name + '"}';
		
		#Issue Clone VM
		result = self.Post(cloneUrl,None, False, payload,self.headers);

		if result == {}:
			print("\nFAILED to Clone VM " + old_vm_name + " to " + new_vm_name);
		else:
			print(result);
			print("\nSUCCESS to Clone VM " + old_vm_name + " to " + new_vm_name);

	def MoveVM(self,vm_name ,target_ds):
		''' Move VM to targeted DataStore '''
		vmList = self.Get("virtual_machines", {"name": vm_name});
		if (vmList == {}):
			#Print error if there is no VM
			print ("\nCannot find VM named " + vm_name + " in Simplivity " + self.auth_ip);
		vm = vmList["virtual_machines"][0];

		dsList = self.Get("datastores", {"name": target_ds});
		if (dsList == {}):
			#Print error if there is no VM
			print ("\nCannot find target DataStore named " + target_ds + " in Simplivity " + self.auth_ip);
		ds = dsList["datastores"][0];
		#Set URL for POST
		moveUrl = "virtual_machines/" + vm["id"] + "/move";
		#Set Moving parameters, content type and Payloads
		header = self.headers;
		header['content-type'] = 'application/vnd.simplivity.v1+json';
		payload = '{"virtual_machine_name":"' + new_vm_name + '" , "destination_datastore_id":"' + target_ds + '"}';
		#Issue Move VM
		result = self.Post(moveUrl,None, False, payload,self.headers);

		if result == {}:
			print("\nFAILED to Move VM " + vm_name + " to Datastore " + target_ds);
		else:
			print(result);
			print("\nSUCCESS to Clone VM " + vm_name + " to Datastore " + target_ds);

