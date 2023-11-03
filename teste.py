from csvmanager import *

with CSVManager('file.csv') as csv:
    print(csv.table.get())
    csv.table.add(['Lenner', 18, 'CC', 1])
    print(csv.table.get())
    print(csv.table.get(filters={'idade': 17}))
