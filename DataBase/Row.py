import copy


class Row:
    def __init__(self, amount_of_attr):
        self.cells = list()
        self.amount_of_attr = amount_of_attr

    def set_cells(self, cells):
        self.cells = copy.deepcopy(cells)


