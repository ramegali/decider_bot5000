
# 2D lists in Python holy FUCK why is it so complicated
# and after furter testing this isn't even a proper 2D array.....

list1 = []
list2 = []

for i in range(0,3):
	list2.append(i)

for i in range(0,10):
	list1.append(i)
	list1[(len(list1) - 1)] = list2

print "LIST 1:", list1
print "LIST 2:", list2

i = 0
for element in list1:
	print "Index: ", i
	print element
	i += 1
	for j in element:
		print j