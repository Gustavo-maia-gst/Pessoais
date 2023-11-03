from glob import glob1
from csvmanager import CSVManager
from threading import Thread
import os


class DataBase:
    def __init__(self, path):
        self._path = path
        self.tables = {}
        self.changed = set()
        for archive in glob1(path, '*.csv'):
            name = archive.replace(path, '').replace('.csv', '').replace('/', '').replace('\\', '')
            try:
                self.tables[name] = CSVManager(archive)
            except:
                raise ValueError(f"Wrong format to table for file {name}.csv")

    def select(self, table, columns=None, filters=None):
        if not table in self.tables:
            raise KeyError(f"The table {table} aren't present in this DataBase")
        return self.tables[table].select(columns, filters)

    def insert(self, table, line):
        if not table in self.tables:
            raise KeyError(f"The table {table} aren't present in this DataBase")
        self.tables[table].insert(line)
        self.changed.add(table)

    def delete(self, table, filters=None):
        if not table in self.tables:
            raise KeyError(f"The table {table} aren't present in this DataBase")
        self.tables[table].delete(filters)
        self.changed.add(table)

    def create_table(self, name, columns):
        if name in self.tables:
            raise ValueError(f"The table '{name}' already exists")
        new_table = open(f'{self._path}/{name}.csv', 'w')
        header = ''
        for column, c_type in columns.items():
            header += f'{column}:{c_type};'
        header += '\n'
        new_table.write(header)
        new_table.flush()
        self.tables[name] = CSVManager(f'{self._path}/{name}.csv')

    def drop_table(self, name):
        if name not in self.tables:
            raise NameError(f"Table {name} not present in this database")

        del self.tables[name]
        os.remove(f'{self._path}/{name}.csv')

    def commit(self):
        for table in self.changed:
            new_thread = Thread(target=self.tables[table].commit)
            new_thread.start()


if __name__ == '__main__':
    db = DataBase('../DataBase')

    print(db.select('alunos', filters={'idade': 17}))
    db.insert('sites', ['facebook', 'https://www.facebook.com', 2])
    db.commit()
