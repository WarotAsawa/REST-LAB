#Import sections
import sys;
#Change sys.path directory
sys.path.insert(0, "../lib");
from Time import Time;
sys.path.insert(0, "../simplivity");
from SimplivityCluster import SimplivityCluster;

simpClust = SimplivityCluster("172.30.1.31", "administrator@vsphere.local", "P@ssw0rd");
simpClust.Initialize();
simpClust.BackupStateSummary();