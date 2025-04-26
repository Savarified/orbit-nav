import csv
from os import read


loc = []
def readLocation():
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        loc = []
        for row in reader:
            loc.append(row['name'])
            loc.append(row['x'])
            loc.append(row['y'])
            loc.append(row['z'])

def writeLocation(name, x, y, z):
    with open('data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'x', 'y', 'z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'name': name , 'x': str(x), 'y': str(y), 'z': str(z)})

writeLocation('changedVal1', 23, 64, 75)
readLocation()
print(*loc)
writeLocation('changedVal2', 12, 24, 45)
readLocation()
print(*loc)
