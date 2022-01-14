from DataBase.DataTypes import DataType


class Cell:
    def __init__(self, name_attr, type_attr):
        self.name_attr = name_attr
        self.type = type_attr
        self.val = None

    def __str__(self):
        return self.val + " " + self.name_attr

    def set_val(self, val):
        #validate
        if self.type == DataType.INT:
            DataType.validate_int(self.name_attr, val)
        elif self.type == DataType.REAL:
            DataType.validate_float(self.name_attr, val)
        elif self.type == DataType.CHAR:
            DataType.validate_char(self.name_attr, val)
        elif self.type == DataType.MONEY:
            DataType.validate_money(self.name_attr, val)
        elif self.type == DataType.LNVL_MONEY:
            DataType.validate_lnvl_money(self.name_attr, val)

        self.val = val
