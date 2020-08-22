from flask import Blueprint, request, render_template, redirect, url_for
import flask_login
from database import Database as db

auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def auth_login():
	print("login")
	if request.method == 'POST':
		username = request.form['username']
		res = db.get_db().query("select * from users where username='" + username + "'")
		print(res)
		if len(res) == 1 and request.form['password'] == res[0][2]:
			user = User(res[0][0], res[0][1])
			flask_login.login_user(user)
			return redirect(url_for('pages.pages_home'))
	return render_template('auth/login.html')

@auth.route('/logout')
def auth_logout():
	print("logout")
	session.pop('username', None)
	return redirect(url_for('pages.pages_home'))

class User():

	def __init__(self, id=None, username=""):
		self.id = id
		self.username = username
		self.is_authenticated = False

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_anonymous(self):
		return False