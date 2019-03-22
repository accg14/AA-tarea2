import random

list = []
while len(list) <= 40:
	a = random.randint(1,50)
	if not a in list:
		list.append(a)
print(list)
	

