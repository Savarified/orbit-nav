#Example of stored inputs with opencsv
import csv

file_path = 'CSV_EXAMPLE.csv'
#READING
things = []
print(f'{file_path} originally had this:')
with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            things.append(row)
        for thing in things:
            print(f'thing #{things.index(thing)+1}: {thing['things']}')

#WRITING
print(f'\nRewriting values to: ')
for thing in things:
    new_value = input(f'thing #{things.index(thing)+1}: ')
    thing = new_value
f = open(file_path, "w+")
f.close()

with open(file_path, 'wt') as f:
    csv_writer = csv.writer(f)
    fields = ['things']
    csv_writer.writerow(fields)
    row = [things]
    csv_writer.writerow(row)
