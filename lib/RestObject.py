#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
print(sys.path[0])
import request;

#Begin class
class RestObject:
	#REST API's URL
	url = "";
	object_label = "REST Object";
	#Omnistack IP and username password
	auth_ip = "";
	auth_username = "";
	auth_password = "";
	#Auth Token for authentication
	access_token = "";
	#Complete header for Authentication
	headers = {};

##Constructor
 	def __init__(self, ip, user, password):
		self.auth_ip = ip;
		self.auth_username = user;
		self.auth_password = password;


	# REST Object Initialization
	def Initialize(self):
		return;

	# REST Object GET methods with parameters
	def Get(self,input,parameter={}):
		#LOGIN check
		try:
			output = request.get(self.url+input, verify=False, headers=self.headers, params = parameter);
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + ": " + self.auth_ip + " is not reachable!\n");
			return {};

		#Check if valid Omnistack controller 
		try:
			response = output.json();
		#and Convert Output to Response
		except:
			print("\nFailed to authenticated with ERROR :");
			print(self.object_label + ": "+ self.auth_ip + " is not a valid " + self.object_label + "\n");
			return {};
		
		#Check if error
		if ("error_code" in response) or ("error" in response):
			print("\nFaile to authenticated with ERROR :");
			print(response["error"]);
			print("\n");
			return {};
		# Return response JSON
		return response;
