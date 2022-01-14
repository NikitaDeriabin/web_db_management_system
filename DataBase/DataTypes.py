import re


class DataType:
    INT = 'int'
    REAL = 'float'
    STRING = 'str'
    CHAR = 'char'
    MONEY = 'money'
    LNVL_MONEY = 'lnvl_money'

    type_list = ['int', 'str', 'char', 'float', 'money', 'lnvl_money']
    MAX_MONEY = 1e13

    @staticmethod
    def validate_int(attr_name, val):
        try:
            temp = int(val)
        except:
            raise TypeError("Invalid type on attr '" + attr_name + "'. Must be int value!")

    @staticmethod
    def validate_float(attr_name, val):
        try:
            temp = float(val)
        except:
            raise TypeError("Invalid type on attr '" + attr_name + "'. Must be real value!")

    @staticmethod
    def validate_char(attr_name, val):
        if not re.compile(".?$").match(val):
            raise TypeError("Invalid type on attr '" + attr_name + "'. Must be char value!")

    @staticmethod
    def validate_money(attr_name, val):
        if not re.compile("\\d+(\\.\d{1,2})?\\$").match(val):
            raise TypeError("Invalid type on attr '" + attr_name + "'. Must be money!")
        else:
            mon_val = float(val[:-1])
            if mon_val > DataType.MAX_MONEY:
                raise TypeError("Invalid value on attr '" + attr_name + "'. Value must be less than "
                                + str(DataType.MAX_MONEY))

    @staticmethod
    def validate_lnvl_money(attr_name, val):
        if not re.compile("\\d+(\\.\d{1,2})?\\$;\\d+(\\.\d{1,2})?\\$").match(val):
            raise TypeError("Invalid type on attr '" + attr_name + "'. Must be lvnl_money!")
        else:
            mon_val = val.split(';')
            if float(mon_val[0][:-1]) > DataType.MAX_MONEY or \
                    float(mon_val[1][:-1]) > DataType.MAX_MONEY:
                raise TypeError("Invalid value on attr '" + attr_name + "'. Value must be less than "
                                + str(DataType.MAX_MONEY))
