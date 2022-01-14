from flask import Blueprint, jsonify, request, render_template, redirect, url_for

from Controller.DataBaseController import DataBaseController
from Controller.FileReader import FileReader
import constants as const
import sqlite3 as sql


app_table = Blueprint('app_table', __name__)


@app_table.route('/db/<string:db_name>/tables/create', methods=['GET', 'POST'])
def create_table(db_name):
    if request.method == 'POST':
        table_name = request.form.get("table_name")

        try:
            if not FileReader.check_exists_file(const.resource_path + db_name):
                return jsonify({'message': db_name + ' not exists, check URL!'})

            db_connection = sql.connect(const.resource_path + db_name)

            table_name = request.form.get("table_name")

            attrs = list()

            for attr_name, attr_type in zip(request.form.getlist('attr_name'),
                                            request.form.getlist('attr_type')):
                attr = dict()
                attr["name"] = attr_name
                attr["type"] = attr_type
                attrs.append(attr)

            print(attrs)
            DataBaseController.create_table(db_connection, table_name, attrs)

            return redirect(url_for('app_table.get_tables', db_name=db_name))
        except Exception as ex:
            return jsonify({'message': str(ex)})
    else:
        return render_template('create_table.html')


@app_table.route('/db/<string:db_name>/tables/delete', methods=['GET', 'DELETE'])
def delete_table(db_name):
    try:
        if not FileReader.check_exists_file(const.resource_path + db_name):
            return jsonify({'message': db_name + ' not exists, check URL!'})

        db_connection = sql.connect(const.resource_path + db_name)

        table_name = request.args.get('name')
        DataBaseController.delete_table(db_connection, table_name)
        return redirect(url_for('app_table.get_tables', db_name=db_name))
    except:
        #return redirect(url_for('app_table.get_tables', db_name=db_name))
        return jsonify({'message': 'Unable to remove table'})


@app_table.route('/db/<string:db_name>/tables')
def get_tables(db_name):
    try:
        if not FileReader.check_exists_file(const.resource_path + db_name):
            return jsonify({'message': db_name + ' not exists, check URL!'})

        db_connection = sql.connect(const.resource_path + db_name)

        context_tables = dict()
        context_tables["db"] = db_name
        context_tables["tables"] = DataBaseController.get_tables(db_connection)
        return render_template('get_tables.html', context_tables=context_tables)
    except Exception as ex:
        return jsonify({'message': str(ex)})
