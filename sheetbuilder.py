import math
import random
import csv
import shutil

if __name__ == "__main__":
	duration = 60
	numspots1 = 48
	#numcars = 80


	f = open('./testinput.csv', 'w')
	writer = csv.writer(f)
	#f2 = open('./')
	services = [0]*numspots1
	colors = [0]*numspots1
	numc = 0
	for k in range(0, duration):
		num_arrivals = random.randint(-10, 5)
		if num_arrivals < 0:
			num_arrivals = 0

		for z in range(0, num_arrivals):
			numc+=1
			indexes = [i for i, j in enumerate(services) if j == 0]
			#print(indexes)
			numspots = len(indexes)
			#print(numspots)
			if numspots == 0:
				break
			which = random.randint(1, numspots)
			ide = indexes[which-1]
			service = random.randint(9, 15)
			color = random.randint(1, 5)
			services[ide] = service
			colors[ide] = color
		for i, serv in enumerate(services):
			if serv>0:
				services[i]-=1
				if services[i] == 0:
					colors[i] = 0

		row = colors
		writer.writerow(row)
	f.close()
	filename = './inputsheets/d' + str(duration) + 'c' + str(numc) + 's' + str(numspots1) + '.csv'
	shutil.copy('./testinput.csv', filename)
	#print(num_arrivals)