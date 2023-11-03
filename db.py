class DataBase:
    def __init__(self, database):
        self.database = database

    def select(self, table, columns=None, filters=None):
        


    def __del__(self):
        close(self.archive)
