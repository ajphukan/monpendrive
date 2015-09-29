import os
a=os.popen("wmic logicaldisk get description")
dev_list=a.read()
if "Removable" in dev_list:
    print("Pendrive Detected")
else:
    print("Pendrive is not there")

    
