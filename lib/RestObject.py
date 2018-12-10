#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
print(sys.path[0])
import request;

#Begin class
class RestObject(object):
	'''
	---------------------------------------------------
	REST Object's IP Address and username password
	---------------------------------------------------
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
			output = request.get(self.url+input, verify=False, headers=self.headers, params = parameter);
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + ": " + self.auth_ip + " is not reachable!\n");
			return {};

		# Check if valid Omnistack controller 
		try:
			response = output.json();
		# and Convert Output to Response
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + ": "+ self.auth_ip + " is not a valid " + self.object_label + "\n");
			return {};
		
		# Check if error
		if ("error_code" in response) or ("error" in response):
			print("\nFaile to authenticated with ERROR :");
			print(response["error"]);
			print("\n");
			return {};

		# Return response JSON
		return response;
