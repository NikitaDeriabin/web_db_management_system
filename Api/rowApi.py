from flask import Blueprint, jsonify, request, render_template, redirect, url_for


from Controller import Format
from Controller.DataBaseController import DataBaseController
from Controller.FileReader import FileReader
import constants as const
import sqlite3 as sql

from DataBase.Base import Base
from DataBase.Cell import Cell
from DataBase.Row import Row

app_row = Blueprint('app_row', __name__)


@app_row.route('/db/<string:db_name>/tables/<string:tb_name>/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_row(db_name, tb_name, id):
    try:
        if not FileReader.check_exists_file(const.resource_path + db_name):
            return jsonify({'message': db_name + ' not exists, check URL!'})

        db_connection = sql.connect(const.resource_path + db_name)

        if tb_name not in DataBaseController.get_tables(db_connection):
            return jsonify({'message': tb_name + ' table not exists, check URL!'})

        DataBaseController.delete_row(db_connection=db_connection, tb_name=tb_name, id=id)

        table_with_data = DataBaseController.get_records(tb_name=tb_name, db_connection=db_connection)
        json_table = Format.table_to_json(table_with_data)
        return redirect(url_for('app_row.get_rows', db_name=db_name, tb_name=tb_name))

    except Exception as ex:
        return jsonify({'message': str(ex)})


@app_row.route('/db/<string:db_name>/tables/<string:tb_name>/insert', methods=['GET', 'POST'])
def insert_row(db_name, tb_name):
    if request.method == "POST":
        try:
            if not FileReader.check_exists_file(const.resource_path + db_name ):
                return jsonify({'message': db_name + ' not exists, check URL!'})

            db_connection = sql.connect(const.resource_path + db_name)

            if tb_name not in DataBaseController.get_tables(db_connection):
                return jsonify({'message': tb_name + ' table not exists, check URL!'})


            table_with_attrs = DataBaseController.get_table_data(tb_name=tb_name, db_connection=db_connection)
            row = Row(len(table_with_attrs.attributes) - 1)
            temp_row = []

            for attr in table_with_attrs.attributes:
                cell = Cell(name_attr=attr.name, type_attr=attr.type)
                cell.set_val(request.form.get(attr.name))
                temp_row.append(cell)

            row.set_cells(temp_row)

            DataBaseController.insert_row(db_connection=db_connection, tb_name=tb_name, row=row)
            # if not 'id' in request_data:
            #     DataBaseController.insert_row(db_connection=db_connection, tb_name=tb_name, row=row)
            # else:
            #     DataBaseController.update_row(db_connection=db_connection, tb_name=tb_name, row=row,
            #                                   row_id=request_data['id'])

            table_with_data = DataBaseController.get_records(tb_name=tb_name, db_connection=db_connection)

            return redirect(url_for('app_row.get_rows', db_name=db_name, tb_name=tb_name))

        except Exception as ex:
            db_connection = sql.connect(const.resource_path + db_name)
            context_attrs = DataBaseController.get_table_data(tb_name=tb_name, db_connection=db_connection).attributes
            return render_template('insert_row.html', context_attrs=context_attrs, error_statement=str(ex))
    else:
        db_connection = sql.connect(const.resource_path + db_name)
        context_attrs = DataBaseController.get_table_data(tb_name=tb_name, db_connection=db_connection).attributes
        return render_template('insert_row.html', context_attrs=context_attrs)


@app_row.route('/db/<string:db_name>/tables/<string:tb_name>/<int:row_id>/update', methods=['GET', 'POST'])
def update_row(db_name, tb_name, row_id):
    if request.method == "POST":
        try:
            if not FileReader.check_exists_file(const.resource_path + db_name):
                return jsonify({'message': db_name + ' not exists, check URL!'})

            db_connection = sql.connect(const.resource_path + db_name)

            if tb_name not in DataBaseController.get_tables(db_connection):
                return jsonify({'message': tb_name + ' table not exists, check URL!'})

            table_with_attrs = DataBaseController.get_table_data(tb_name=tb_name, db_connection=db_connection)
            row = Row(len(table_with_attrs.attributes) - 1)
            temp_row = []

            for attr in table_with_attrs.attributes:
                cell = Cell(name_attr=attr.name, type_attr=attr.type)
                cell.set_val(request.form.get(attr.name))
                temp_row.append(cell)

            row.set_cells(temp_row)

            DataBaseController.update_row(db_connection=db_connection, tb_name=tb_name, row=row,
                                          row_id=row_id)

            table_with_data = DataBaseController.get_records(tb_name=tb_name, db_connection=db_connection)

            return redirect(url_for('app_row.get_rows', db_name=db_name, tb_name=tb_name))
        except Exception as ex:
            db_connection = sql.connect(const.resource_path + db_name)
            context_row = DataBaseController.get_row(db_connection=db_connection, tb_name=tb_name, row_id=int(row_id))

            return render_template('update_row.html', context_row=context_row, error_statement=str(ex))
    else:
        db_connection = sql.connect(const.resource_path + db_name)
        context_row = DataBaseController.get_row(db_connection=db_connection, tb_name=tb_name, row_id=int(row_id))

        return render_template('update_row.html', context_row=context_row)


@app_row.route('/db/<string:db_name>/tables/<string:tb_name>')
def get_rows(db_name, tb_name):
    try:
        if not FileReader.check_exists_file(const.resource_path + db_name):
            return jsonify({'message': db_name + ' not exists, check URL!'})

        db_connection = sql.connect(const.resource_path + db_name)

        if tb_name not in DataBaseController.get_tables(db_connection):
            return jsonify({'message': tb_name + ' table not exists, check URL!'})

        table_with_data = DataBaseController.get_records(tb_name=tb_name, db_connection=db_connection)
        context_data = Format.table_to_json(table_with_data)
        context_data["columns"] = table_with_data.attributes
        context_data["db"] = db_name
        context_data["tb_name"] = tb_name
        return render_template('get_rows.html', context_data=context_data)

    except Exception as ex:
        return jsonify({'message': str(ex)})


@app_row.route('/db/<string:db_name>/join-tables', methods=['GET', 'POST'])
def join_tables(db_name):
    if request.method == "POST":
        try:
            if not FileReader.check_exists_file(const.resource_path + db_name):
                return jsonify({'message': db_name + ' not exists, check URL!'})

            db_connection = sql.connect(const.resource_path + db_name)

            tb1_name = request.form.get('table1')
            tb2_name = request.form.get('table2')

            base = Base(db_connection=db_connection)
            comm_attrs = base.get_common_attrs(tb1_name, tb2_name)

            if len(comm_attrs) == 0:
                return jsonify({'message': 'no common attribute for those tables!'})
            if request.form.get('common_attr') not in comm_attrs:
                return jsonify({'message': request.form.get('common_attr') + ' not common for those tables'})

            table = base.get_join_table(comm_attr=request.form.get('common_attr'), tbl1=tb1_name, tbl2=tb2_name)

            context_data = Format.table_to_json(table)
            context_data["db"] = db_name
            context_data["columns"] = [attr for attr, _ in context_data['records'][0].items()]
            print(context_data["columns"])
            print(context_data["records"])

            return render_template('join_tables_view.html', context_data=context_data)

        except Exception as ex:
            return jsonify({'message': str(ex)})

    else:
        db_connection = sql.connect(const.resource_path + db_name)
        context_tables = DataBaseController.get_tables(db_connection)
        return render_template('join_tables_dialog.html', context_tables=context_tables)