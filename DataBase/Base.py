from Controller.DataBaseController import DataBaseController
from DataBase.Row import Row
from DataBase.Table import Table
import constants as const


class Base:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.tables = list()
        self.name_pos_table = dict() # словарь имен таблиц и их позиций в списке tables

    def get_common_attrs(self, table1, table2):
        tbl1_attrs = []
        tbl2_attrs = []
        cursor = self.db_connection.cursor()

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (table1,))

        rows = cursor.fetchall()
        for row in rows:
            tbl1_attrs.append(row[1].lower())

        # print("table1:", tbl1_attrs)

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (table2,))
        rows = cursor.fetchall()
        for row in rows:
            tbl2_attrs.append(row[1].lower())

        # print("table2:", tbl2_attrs)
        # print()

        return list(set(tbl1_attrs) & set(tbl2_attrs))

    def get_join_table(self, comm_attr, tbl1, tbl2):
        def concat_row(r1, r2):
            temp_result_row = []
            for cell in r1.cells:
                temp_result_row.append(cell)
            for cell in r2.cells:
                if cell.name_attr.lower() == comm_attr:
                    continue
                temp_result_row.append(cell)

            res_row = Row(len(temp_result_row))
            res_row.set_cells(temp_result_row)
            return res_row

        table1 = DataBaseController.get_records(tbl1, self.db_connection)
        table2 = DataBaseController.get_records(tbl2, self.db_connection)

        table1_comm_attr_values = set()
        for row in table1.rows:
            for cell in row.cells:
                if cell.name_attr.lower() == comm_attr.lower():
                    table1_comm_attr_values.add(cell.val)

        table2_comm_attr_values = set()
        for row in table2.rows:
            for cell in row.cells:
                if cell.name_attr.lower() == comm_attr.lower():
                    table2_comm_attr_values.add(cell.val)

        result_comm_attr_values = table1_comm_attr_values & table2_comm_attr_values

        res_table = Table(tbl1 + " join " + tbl2)

        for row1 in table1.rows:
            for cell1 in row1.cells:
                if cell1.name_attr.lower() == comm_attr.lower():
                    if cell1.val in result_comm_attr_values:
                        for row2 in table2.rows:
                            for cell2 in row2.cells:
                                if cell2.name_attr.lower() == comm_attr.lower():
                                    if cell2.val == cell1.val:
                                        res_table.add_row(concat_row(row1, row2))

        return res_table

    def create_table(self, table):
        self.tables.append(table)
        self.name_pos_table[table.name] = len(self.tables)

    def get_table(self, table_name):
        return self.tables[self.name_pos_table[table_name]]