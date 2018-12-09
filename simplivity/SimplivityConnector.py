from SimplivityCluster import SimplivityCluster;

simpClust = SimplivityCluster("172.30.1.31", "administrator@vsphere.local", "P@ssw0rd");
simpClust.Initialize();
simpClust.GetHosts();
simpClust.GetDatastores();