
class Table:
    def __init__(self, name):
        self.name = name
        self.attributes = list() # возможно dict()
        self.rows = list() # возможно dict()

    def __str__(self):
        return self.name

    def add_attribute(self, attr):
        attr.set_num(len(self.attributes))
        self.attributes.append(attr)

    def add_row(self, row):
        self.rows.append(row)
