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


time = Time.GetInstance();
print (time.GetTimeNow());
print (time.GetPreviuosNDay(5));
print (time.GetPreviuosNMonth(2));
print (time.GetPreviuosNYear(1));

simpClust = SimplivityCluster("172.30.1.31", "administrator@vsphere.local", "P@ssw0rd");
simpClust.Initialize();
simpClust.BackupStateSummary();

