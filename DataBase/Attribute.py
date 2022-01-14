class Attribute:
    data_types = ['int', 'str', 'char', 'float', 'lnvl']

    def __init__(self, name, data_type, table_name):
        self.num = 0
        self.name = name
        self.type = data_type
        self.table_name = table_name

    def __str__(self):
        return self.name

    def set_num(self, num):
        self.num = num

