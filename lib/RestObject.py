#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
#Disable unnessary warnings
import urllib3;
urllib3.disable_warnings();
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
print(sys.path[0])
import requests;
#---------------------------------------------------------------------
#Begin class
class RestObject(object):
	'''
	------------------------------------------------------------------
	REST Object's IP Address and username password
	------------------------------------------------------------------
	'''
	url = "";							# REST Target URL
	object_label = "REST Object";		# Object label used to print out
	
	auth_ip = "";						# Object's IP Address		
	auth_username = "";					# Object's Username	
	auth_password = "";					# Object's Password	
	
	access_token = "";					# Auth Token for authentication
	
	headers = {};						# Complete header for Authentication

 	def __init__(self, ip, user, password):
 		''' REST Object's Constructer: Setting up IP,username and password '''
		self.auth_ip = ip;
		self.auth_username = user;
		self.auth_password = password;

	def Initialize(self):
		'''REST Object Initialization method. Requires inherit and update'''
		return;

	def Get(self,input,parameter={}):
		'''REST Object GET : Included ERROR check and handling.'''

		# LOGIN check
		try:
			output = requests.get(self.url+input, verify=False, headers=self.headers, params = parameter);
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + ": " + self.auth_ip + " is not reachable!\n");
			return {};

		# Check if error
		response = self.CheckOutputError(output);

		# Return response JSON
		return response;

	def Post(self, url="", auth=None, verify=False, data={}, header=None):
		'''REST Object PUT : Included ERROR check and handling.'''

		#LOGIN check

		try:
			if (header == None):
				output = requests.post(self.url+url, auth=auth, verify=verify, data=data);
			else:
				output = requests.post(self.url+url , verify=verify, data=data, headers=header);
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + " : " + self.auth_ip + " is not reachable!\n");
			return {};

		
		# Check if error
		response = self.CheckOutputError(output);

		# Return response JSON
		return response;

	def CheckOutputError(self, output):
		#Check response error and return True or False;

		#Check if valid Omnistack controller 
		try:
			response = output.json();
		#and Convert Output to Response
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + " : " + self.auth_ip + " is not a valid " + self.object_label + "!\n");
			return {};

		if ("error_code" in response):
			print("\nFailed with ERROR :");
			print(response["error_code"]);
			print("\n");
			return {};

		if ("error" in response):
			print("\nFailed with ERROR :");
			print(response["error"]);
			print("\n");
			return {};

		if (response == {}):
			print("\nFailed to get output from :");
			print(self.object_label + " : " + self.auth_ip + "\n");
			return {};

		return response;
			