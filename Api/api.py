from flask import Flask, render_template
from Api.dbApi import app_db
from Api.tableApi import app_table
from Api.rowApi import app_row


app = Flask(__name__, template_folder='../templates', static_url_path="/static", static_folder="../static")
app.config['SECRET_KEY'] = '76721751b9f91e57a792f70f'


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(app_db)
app.register_blueprint(app_table)
app.register_blueprint(app_row)

app.run(port=8000, debug=True)
