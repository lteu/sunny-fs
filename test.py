import os
import sys

def filterE16(arr):
	for indx, val in enumerate(arr):
		num = str(val)
		print 'original ',val,' str', num, ' found ',num.find("e-0")
		if num.find("e-0") != -1:
			num = float(num)
			num = round(num,5)
		arr[indx] = str(num)

	return arr

# num = 4.6273748721681329e-16
# num2 = str(num)
# stridx = num2.find("ae-16")

#print round(num,15),' size', sys.getsizeof(num), ' len',len(num2),' index', stridx


arr = [12,33,23,4.6273748721681329e-16,4.958e-07,1.4e-07]
arr = filterE16(arr)

res = ",".join(arr)

print res