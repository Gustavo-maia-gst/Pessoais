class Table:
    def __init__(self, matrix):
        self.matrix = matrix[1:]
        
        self.ordered_columns = matrix[0]
        self.columns = dict((matrix[0][i], []) for i in range(len(matrix[0]))) 

        for row in matrix[1:]:
            for i in range(len(matrix[0])):
                self.columns[matrix[0][i]].append(row[i])


    def get(self, columns, filters):
        if not columns:
            columns = self.columns.keys()

        if not filters:
            rows = [i for i in range(len(self.matrix))]
        else:
            rows = []
            for fil in filters:
                for i in range(len(self.columns[fil])):
                    if self.columns[fil][i] == filters[fil]:
                        rows.append(i)

        results = []


        for i in rows:
            line = []
            for column in columns:
                line.append(self.columns[column][i])
            results.append(line)

        return results
    
    def add(self, line):
        for i in range(len(self.ordered_columns)):
            self.columns[self.ordered_columns[i]].append(line[i])
        self.matrix.append(line)


class CSVManager:
    def __init__(self, path, sep=';'):
        self.archive = open(path)
        header = self.archive.readline().split(';')[:-1]
        types = [eval(e.split(':')[1]) for e in header]
        header = [[e.split(':')[0] for e in header]]

        matrix = []

        for line in self.archive.readlines():
            line = line.split(';')[:-1]
            for i in range(len(line)):
                line[i] = types[i](line[i])
            matrix.append(line)

        self.table = Table(header + matrix)

    def __enter__(self):
        return self

    def select(self, columns=None, filters=None):
        if columns is None:
            columns = []
        if not isinstance(columns, list):
            raise ValueError("You need to pass the columns")

        return self.table.get(self, columns, filters)
    
    def insert(self, line):
        self.table.add(line)
        
        new_line = ''

        for elem in line:
            new_line += f'{elem};'

        new_line += '\n'

        self.archive.write(new_line)

    def __exit__(self, exc_type, exc_value, traceback):
        self.archive.close()
