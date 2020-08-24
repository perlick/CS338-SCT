from flask import Blueprint, request, jsonify, redirect, url_for
import flask_login
from database import Database as db
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/add-test', methods=['POST'])
@flask_login.login_required
def api_add_test():
	uid = flask_login.current_user.get_id()
	pid = request.form.get('person')
	result = request.form.get('result')
	date = request.form.get('date').split("-")
	time = request.form.get('time').split(":")
	timestamp = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1])).timestamp()
	db.get_db().query(f"""
		insert into tests
			(person_id, timestamp, result)
		values
			({pid},{timestamp},{result})
		""")
	# tid = db.get_db().query("select id from tests order by id desc limit 1;")[0][1]
	# if result == 1:
	# 	# positive test
	# else if result == 0:
	# 	# negetive test
	# 	db.get_db().query(f"""
	# 		insert into statuses
	# 			(person_id, test_id, visit_id, timestamp, level)
	# 		values
	# 			({pid},{tid},Null,{timestamp}, 0)""")
	return redirect(url_for('pages.pages_testReports'))

@api.route('/delete-test', methods=['POST'])
@flask_login.login_required
def api_delete_test():
	uid = flask_login.current_user.get_id()
	tid = request.form.get('id')
	db.get_db().query("delete from tests where id=" + str(tid) + " limit 1;")
	return redirect(url_for('pages.pages_testReports'))

@api.route('/add-visit', methods=['POST'])
@flask_login.login_required
def api_add_visit():
	uid = flask_login.current_user.get_id()
	pid = request.form.get('person')
	lid = request.form.get('location')
	date = request.form.get('date').split("-")
	time = request.form.get('time').split(":")
	hours = request.form.get('hours')
	minutes = request.form.get('minutes')
	timestamp = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1])).timestamp()
	duration = (int(hours)*60) + int(minutes)
	db.get_db().query(f"""
		insert into visits 
			(person_id, location_id, timestamp, duration_minutes)
		values
			({pid},{lid},{timestamp},{duration})
		""")
	return redirect(url_for('pages.pages_locations'))

@api.route('/delete-visit', methods=['POST'])
@flask_login.login_required
def api_delete_visit():
	uid = flask_login.current_user.get_id()
	vid = request.form.get('id')
	db.get_db().query("delete from visits where id=" + str(vid) + " limit 1;")
	return redirect(url_for('pages.pages_locations'))

@api.route('/add-member', methods=['POST'])
@flask_login.login_required
def api_add_member():
	uid = flask_login.current_user.get_id()
	first = request.form.get('first')
	last = request.form.get('last')
	db.get_db().query("insert into people (user_id, first, last) values ("+ str(uid) +",'"+ first +"','"+ last +"');")
	return redirect(url_for('pages.pages_familyManager'))

@api.route('/delete-member', methods=['POST'])
@flask_login.login_required
def api_delete_member():
	uid = flask_login.current_user.get_id()
	pid = request.form.get('id')
	db.get_db().query("delete from people where id=" + str(pid) + " limit 1;")
	return redirect(url_for('pages.pages_familyManager'))
