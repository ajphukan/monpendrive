import os
a=os.popen("lsblk -nl -d")
b=[]
for c in a:
	b.append(c.split()[2])

if '1' in b:
	print("Pendrive Detected")
else:
	print("Pendrive is not there")
