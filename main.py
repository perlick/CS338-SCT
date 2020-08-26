from flask import Flask, session, redirect, url_for
import flask_login
from auth import User
from database import Database as db
from api import api
from pages import pages
from auth import auth


app = Flask(__name__, static_folder='public', static_url_path='')

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pages, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth')

app.secret_key = b'\x97\x81\x85\xf2\xcan\n\x0b\x9c\x99\x08S\x8e:\xfc\t'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
	return redirect(url_for('pages.pages_home'))

@app.teardown_appcontext
def close_connection(exception):
	try:
		db = getattr(g, '_database', None)
		db.close()
	except NameError:
		pass

@login_manager.user_loader
def load_user(id):
	res = db.get_db().query("select * from users where id='" + str(id) + "'")
	if len(res) == 1:
		user = User(res[0][0], res[0][1]) 
		user.is_authenticated = True
		return user
	else:
		return None

@login_manager.request_loader
def request_loader(request):
	username = request.form.get('username')
	res = db.get_db().query("select * from users where username='" + str(username) + "'")
	if len(res) == 1:
		user = User(res[0][0], res[0][1])
		return user
	else:
		return None

@login_manager.unauthorized_handler
def unauthorized_handler():
	return redirect(url_for('auth.auth_login'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)