# HPE Simplivity REST API Connector

Simplivity REST API connector provides methods for getting some information from Simplivity by calling Simplivity's REST API interface. There are sample code for Simplivity connection, which you can edit or add some modules as you like.

## Getting Started

These instructions will help you understand about how to you this code.

## Getting into Simplivity folder

Simply get into the directory using this following path

```
cd /<install-directory>/REST-LAB/simplivity
```
You can find these following file in the directory
* **SimplivityCluster.py** - Contains Simplivity REST API features.
* **SimplivityContainer.py** - Use to run Simplivity REST API script.
* **OVC-MON.py** - Use to present Simplivity additional dashboard as Web interface.

## About SimplivityCluster.py

Here is the function list for Simplivity Cluster.

* **Initialize():** - Sing in to Simplivity's OVC.
* **GetDatastoresAll():** - Get All DataStores as Dictionary.
* **PrintDatastoresAll():** - Print All DataStores on to the console.
* **GetClustersAll():** - Get All Simplivity Clusters as Dictionary.
* **PrintClustersAll():** - Print All Simplivity Clusters on to the console.
* **GetHostsAll():** - Get All Simplivity Hosts as Dictionary.
* **PrintHostsAll():** - Print All Simplivity Hosts on to the console.
* **GetBackUpsAll():** - Get All Simplivity Backups as Dictionary.
* **PrintBackUpsAll():** - Print All Simplivity Backups on to the console.
* **GetVMsAll():** - Get All Simplivity VMs as Dictionary.
* **PrintVMsAll():** - Print All Simplivity VMs on to the console.
* **BackUpsSummaryAll():** Print All Simplivity Backups' summary on to the console.
* **GetBackUpsFrom(time):** - Get Simplivity Backups since input time as Dictionary.
* **BackUpsSummaryFrom(time):** - Print All Simplivity Backups since input time on to the console.
* **CloneVM(old_vm_name ,new_vm_name):** - Clone VM by inputting VM's name and new VM's name.
* **MoveVM(vm_name ,target_ds):** - Move VM to target DataStore.

## How to use SimplivityCluster.py

You can find SimplivityCluster example in SimplivityConnector. Just create new SimplivityCluster's instance using OVC's IP, OVC's username and OVC's Password and Initailize. For example ,

```
from SimplivityCluster import SimplivityCluster;

llCluster = SimplivityCluster("<ovc'shostname or IP address>", "<ovc's username>", "<ovs's password>");
llCluster.Initialize();

llCluster.PrintHostsAll();
```

## How to use OVC-MON.py

OVC-MON.py is an example which provides a webservice that will display Simplivity Dashboard. Simpliy run OVC-MON.py in the simplivity directory.

```
python OVC-MON.py
```

Then open web browser and open OVC Mon page

```
http://<ovc-mon-ip>
```

Using web page's top banner to login to OVC.

![Banner Login](screenshots/banner.PNG?raw=true "Banner Login")

After login, the graphs will appears as figure as below.

![Graph GUI](screenshots/graph.PNG?raw=true "Graph Login")
