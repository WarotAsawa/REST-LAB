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
#---------------------------------------------------------------------

time = Time.GetInstance();

bblCluster = SimplivityCluster("172.30.5.31", "administrator@vsphere.local", "P@ssw0rd");
bblCluster.Initialize();

bblCluster.BackUpsSummaryAll();

for i in range(11,15):
	bblCluster.CloneVM("Centos", "BBL-Clone-" + str(i));

