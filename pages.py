from flask import Blueprint, request, jsonify, render_template
import flask_login
from database import Database as db
from datetime import datetime

pages = Blueprint('pages', __name__)

@pages.route('/home')
@flask_login.login_required
def pages_home():
	data = {}
	data['title'] = "SCT"
	data['menu'] = True
	data['id'] = flask_login.current_user.get_id()
	data['username'] = flask_login.current_user.username
	return render_template('pages/home.html', data=data)

@pages.route('/locations')
@flask_login.login_required
def pages_locations():
	data = {}
	data['title'] = "Locations"
	uid = flask_login.current_user.get_id()
	data['members'] = db.get_db().query("select * from people where user_id=" + str(uid))
	data['locations'] = db.get_db().query("select * from locations")
	visits = db.get_db().query("""
		select * from people 
		join visits 
			on people.id = person_id 
		join locations 
			on location_id = locations.id 
		where user_id=""" + str(uid))
	data['visits'] = []
	j = 0
	for visit in visits:
		data['visits'].append([])
		i = 0
		for item in visit:
			if i == 7:
				timestamp = datetime.fromtimestamp(visit[7])
				data['visits'][j].append(str(timestamp.date()))
				data['visits'][j].append(str(timestamp.time()))
			else:
				data['visits'][j].append(item)
			i = i + 1
		j = j + 1
	return render_template('pages/locations.html', data=data)

@pages.route('/test-reports')
@flask_login.login_required
def pages_testReports():
	data = {}
	data['title'] = "Test Reports"
	uid = flask_login.current_user.get_id()
	data['members'] = db.get_db().query("select * from people where user_id=" + str(uid))
	tests = db.get_db().query("""
		select * from people
		join tests
			on people.id = tests.person_id
		where user_id=""" + str(uid))
	data['tests'] = []
	j = 0
	for test in tests:
		data['tests'].append([])
		i = 0
		for item in test:
			if i == 6:
				timestamp = datetime.fromtimestamp(item)
				data['tests'][j].append(str(timestamp.date()))
				data['tests'][j].append(str(timestamp.time()))
			else:
				data['tests'][j].append(item)
			i = i + 1
		j = j + 1
	return render_template('pages/test-reports.html', data=data)

@pages.route('/exposure-history')
@flask_login.login_required
def pages_exposureHistory():
	data = {}
	data['title'] = "Exposure History"
	return render_template('pages/exposure-history.html', data=data)

@pages.route('/family-manager')
@flask_login.login_required
def pages_familyManager():
	data = {}
	data['title'] = "Family Manager"
	uid = flask_login.current_user.get_id()
	data['members'] = db.get_db().query("select * from people where user_id=" + str(uid))
	return render_template('pages/family-manager.html', data=data)

@pages.route('/community-exposures')
@flask_login.login_required
def pages_communityExposures():
	data = {}
	data['title'] = "Community Exposures"
	return render_template('pages/community-exposures.html', data=data)