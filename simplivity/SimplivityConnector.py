#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from Time import Time;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"simplivity")));
from SimplivityCluster import SimplivityCluster;
#sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"nimble")));
#from NimbleArray import NimbleArray;
#---------------------------------------------------------------------
#
time = Time.GetInstance();

llCluster = SimplivityCluster("172.30.5.31", "administrator@vsphere.local", "P@ssw0rd");
llCluster.Initialize();

llCluster.BackUpsSummaryAll();

llCluster.PrintHostsAll();

llCluster.PrintBackUpsAll();
#nimbleDC = NimbleArray("172.30.4.20","admin","admin","../nimble/cert/nimble-dc.cer");
#nimbleDC.Initialize();
#print(nimbleDC.name)
#nimbleDC.PrintNimbleCapacity();
