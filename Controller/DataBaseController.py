import sqlite3 as sql
import constants as const
from DataBase.Table import Table
from DataBase.Row import Row
from DataBase.Cell import Cell
from DataBase.Attribute import Attribute


class DataBaseController:
    @staticmethod
    def create_db(name):
        def create_attr_table(db_path):
            connection = sql.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS attribute(
                name_table TEXT,
                col_name TEXT,
                 type_name TEXT);
            """)
            connection.commit()

        file_path = const.resource_path + name
        file = open(file_path + ".db", "a")
        file.close()
        create_attr_table(file_path + ".db")

    @staticmethod
    def get_tables(db_connection):
        cursor = db_connection.cursor()
        cursor.execute("""SELECT * FROM sqlite_master WHERE type='table'""")
        tables = cursor.fetchall()
        return list(filter(lambda x: x != const.attr_table, [tb[1] for tb in tables]))

    @staticmethod
    def create_table(db_connection, table_name, attrs):
        cursor = db_connection.cursor()

        def check_for_same_attr(attrs):
            attrs_set = set([i.name for i in attrs])
            return len(attrs_set) == len(attrs)

        table = Table(table_name)
        attr_str = " (id integer primary key, "
        for attr in attrs:
            if len(attr['name']) == 0:
                continue
            inst_attr = Attribute(attr['name'].replace(' ', ''), attr['type'].replace(' ', ''),
                                  table.name.replace(' ', ''))
            table.add_attribute(inst_attr)
            attr_str += inst_attr.name + " " + "TEXT, "

        attr_str = attr_str[:-2] + ");"
        if len(table.attributes) == 0:
            raise Exception("At least one attribute must be created and filled!")

        if not check_for_same_attr(table.attributes):
            raise Exception("There are common fields!")

        cursor.execute("""CREATE TABLE IF NOT EXISTS """ + table.name.replace(' ', '') + attr_str)

        # insert data to attribute table
        for attr in table.attributes:
            cursor.execute("""INSERT INTO """ + const.attr_table + " (" + \
                                const.attr_table_name + ", " + const.attr_table_column_name + ", " + \
                                const.attr_table_type + ")" + " VALUES (?, ?, ?)",
                                (attr.table_name, attr.name, attr.type))

        db_connection.commit()

    @staticmethod
    def delete_table(db_connection, table_name):
        cursor = db_connection.cursor()
        cursor.execute("""DROP TABLE IF EXISTS """ + table_name)
        cursor.execute("""DELETE FROM """ + const.attr_table + " WHERE " +
                       const.attr_table_name + " = " + "?" + ";", (table_name,))
        db_connection.commit()

    @staticmethod
    def get_table_data(tb_name, db_connection):
        table = Table(tb_name)
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM " + const.attr_table + " WHERE " + const.attr_table_name
                       + " = " + "?" + ";", (tb_name,))
        attr_records = cursor.fetchall()
        for rec in attr_records:
            attr = Attribute(table_name=rec[0], name=rec[1], data_type=rec[2])
            table.add_attribute(attr)

        return table

    @staticmethod
    def get_records(tb_name, db_connection):
        table = DataBaseController.get_table_data(tb_name, db_connection)
        table.attributes.insert(0, Attribute("id", "int", tb_name))
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM " + tb_name + ";")
        table_records = cursor.fetchall()

        for rec in table_records:
            row_list = []

            for i in enumerate(table.attributes):
                cell = Cell(name_attr=i[1].name, type_attr=i[1].type)
                cell.set_val(rec[i[0]])
                row_list.append(cell)

            row = Row(len(table.attributes))
            row.set_cells(row_list)
            table.add_row(row)

        return table

    @staticmethod
    def get_row(db_connection, tb_name, row_id):
        table = DataBaseController.get_table_data(tb_name, db_connection)
        table.attributes.insert(0, Attribute("id", "int", tb_name))
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM " + tb_name + " WHERE id = " + "?" + ";", (row_id,))
        record = cursor.fetchall()

        row_list = []

        for rec in record:
            for i in enumerate(table.attributes):
                cell = Cell(name_attr=i[1].name, type_attr=i[1].type)
                cell.set_val(rec[i[0]])
                row_list.append(cell)

        row = Row(len(table.attributes))
        row.set_cells(row_list)
        return row


    @staticmethod
    def insert_row(db_connection, tb_name, row):
        cursor = db_connection.cursor()
        request_str = "INSERT INTO " + tb_name + " ("
        for cell in row.cells:
            request_str += cell.name_attr + ", "
        request_str = request_str[:-2] + ") VALUES ("
        for i in range(len(row.cells)):
            request_str += "?, "
        request_str = request_str[:-2] + ")"

        insert_values = tuple([cell.val for cell in row.cells])

        cursor.execute(request_str, insert_values)
        db_connection.commit()

    @staticmethod
    def update_row(db_connection, tb_name, row, row_id):
        cursor = db_connection.cursor()
        request_str = "UPDATE " + tb_name + " SET "

        for cell in row.cells:
            request_str += cell.name_attr + "=?, "
        request_str = request_str[:-2] + " WHERE id=?"

        insert_values = tuple([cell.val for cell in row.cells] + [row_id])

        cursor.execute(request_str, insert_values)
        db_connection.commit()

    @staticmethod
    def delete_row(db_connection, tb_name, id):
        cursor = db_connection.cursor()
        request_str = "DELETE FROM " + tb_name + " WHERE id=?;"
        cursor.execute(request_str, (id,))

        db_connection.commit()
