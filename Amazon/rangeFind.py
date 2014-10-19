import ipcalc

#Open file
f = open('prefixes.txt', 'r')

for val in f.readlines():

	#For loop to print every ip address in the subnet.
	for x in ipcalc.Network(val.strip()):
		print x
