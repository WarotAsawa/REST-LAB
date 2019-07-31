#---------------------------------------------------------------------
#Import sections
import sys;
import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from Time import Time;
import time;
from datetime import datetime, timedelta

import os.path;
#Change sys.path directory
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"simplivity")));
from SimplivityCluster import SimplivityCluster;
#sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"nimble")));
#from NimbleArray import NimbleArray;
#---------------------------------------------------------------------
#

llCluster = SimplivityCluster("172.30.5.33", "administrator@vsphere.local", "P@ssw0rd");
llCluster.Initialize();
yesterday = datetime.now() - timedelta(days=1)
yesterweek = datetime.now() - timedelta(days=7)

llCluster.BackUpsSummaryAll();
llCluster.BackUpsSummaryFrom(yesterweek);


local = datetime.now();
glob = datetime.utcnow();


print(local - glob);
#llCluster.PrintHostsAll();

print(Time.GetInstance().UTCToISO(yesterweek));
#nimbleDC = NimbleArray("172.30.4.20","admin","admin","../nimble/cert/nimble-dc.cer");
#nimbleDC.Initialize();
#print(nimbleDC.name)
#nimbleDC.PrintNimbleCapacity();
