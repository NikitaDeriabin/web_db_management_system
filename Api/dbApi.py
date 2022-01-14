from flask import Blueprint, jsonify, request, render_template, redirect, url_for

from Controller.DataBaseController import DataBaseController
from Controller.FileReader import FileReader
import constants as const
from forms.DB_form import DbForm

app_db = Blueprint('app_db', __name__)


@app_db.route('/db/delete', methods=['GET', 'DELETE'])
def delete_db():
    try:
        db_name = request.args.get('name')
        FileReader.delete_db_file(const.resource_path + db_name)
        return redirect(url_for('app_db.get_db_files'))
    except:
        return jsonify({'message': 'Unable to remove file'})


@app_db.route('/db')
def get_db_files():
    context_db = dict()
    context_db["db"] = FileReader.get_db_file_names()
    if context_db:
        return render_template('get_dbs.html', context_db=context_db)
    return jsonify({'message': 'db files not found'})


@app_db.route('/db/create', methods=['GET', 'POST'])
def create_db_form():
    form = DbForm()
    if form.is_submitted():
        try:
            if len(form.db_name.data) != 0:
                db_name = form.db_name.data
                DataBaseController.create_db(db_name)
            return redirect(url_for('app_db.get_db_files'))
        except:
            return jsonify({"message": "Unable to create db file"})

    return render_template('create_db.html', form=form)