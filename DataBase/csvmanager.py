class Table:
    def __init__(self, matrix):
        self.matrix = matrix[1:]
        self.header = matrix[0]
        
        self.ordered_columns = matrix[0]
        self.columns = dict((matrix[0][i], []) for i in range(len(matrix[0]))) 

        for row in matrix[1:]:
            for i in range(len(matrix[0])):
                self.columns[matrix[0][i]].append(row[i])

    def _get_selected_rows(self, filters):
        if not filters:
            return list(range(len(self.matrix)))
        rows = []
        for fil in filters:
            for i in range(len(self.columns[fil])):
                if self.columns[fil][i] == filters[fil]:
                    rows.append(i)
        return rows

    def get(self, columns=None, filters=None):
        if columns is None and filters is None:
            return self.matrix
        if not columns:
            columns = self.columns.keys()

        rows = self._get_selected_rows(filters)
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

    def _remove_row(self, i):
        self.matrix.pop(i)
        for column in self.columns:
            self.columns[column].pop(i)

    def remove(self, filters):
        if not filters:
            for column in self.columns:
                self.columns[column] = []
            self.matrix = []
            return

        rows = self._get_selected_rows(filters)
        for i in range(len(rows)-1, -1, -1):
            self._remove_row(rows[i])


class CSVManager:
    def __init__(self, path, sep=';'):
        self.path = path
        self.archive = open(path, 'r')
        self.header = self.archive.readline().split(';')[:-1]
        types = [eval(e.split(':')[1]) for e in self.header]
        header = [[e.split(':')[0] for e in self.header]]

        matrix = []

        for line in self.archive.readlines():
            line = line.split(';')[:-1]
            for i in range(len(line)):
                line[i] = types[i](line[i])
            matrix.append(line)

        self.table = Table(header + matrix)

    def select(self, columns=None, filters=None):
        if columns is None:
            columns = []
        if filters is None:
            filters = {}
        if not isinstance(columns, list):
            raise ValueError(f"You need to pass the columns as a list, not {type(columns)}")
        if not isinstance(filters, dict):
            raise ValueError(f"You need to pass the filters as a dict of the type: {{'column': 'value'}}, not {type(filters)}")

        return self.table.get(columns, filters)

    def writeline(self, line):
        new_line = ''
        for elem in line:
            new_line += f'{elem};'
        new_line += '\n'

        self.archive.write(new_line)
    
    def insert(self, line):
        try:
            self.table.add(line)
        except LookupError:
            raise ValueError("Wrong format for table")

    def delete(self, filters=None):
        if filters is None:
            filters = {}
        if not isinstance(filters, dict):
            raise ValueError(f"You need to pass the filters as a dict of the type: {{'column': 'value'}}, not {type(filters)}")

        self.table.remove(filters)

    def commit(self):
        self.archive = open(self.path, 'w')
        self.writeline(self.header)
        for line in self.table.get():
            self.writeline(line)

    def __repr__(self):
        return f"<CSVManager('{self.path}')>"

    def __del__(self):
        self.archive.close()


if __name__ == '__main__':
    table = CSVManager('alunos.csv')
    print(table.select(filters={'idade': 17}))
    table.commit()
    print('Tudo ocorreu bem')