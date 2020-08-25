from flask import Blueprint, request, jsonify, render_template
import flask_login
from database import Database as db
from datetime import datetime, timedelta

pages = Blueprint('pages', __name__)

@pages.route('/home')
@flask_login.login_required
def pages_home():
	data = {}
	data['title'] = "SCT"
	data['menu'] = True
	uid = flask_login.current_user.get_id()
	data['username'] = flask_login.current_user.username
	data['status'] = []
	people = db.get_db().query(f"select id, first, last from people where user_id={uid}") #get all people for this user
	for person in people:
		clear = 0
		infected = 0
		#get most recent test from this person
		status = db.get_db().query(f"""
			select result from tests 
			where person_id={person[0]} 
			and timestamp<{datetime.now().timestamp()}
			order by timestamp DESC limit 1""")
		if len(status) == 0:
			status = 0
		else:
			status = status[0][0]
		#for each person in group, find all the places that person has visited in teh last 14 days
		visits = db.get_db().query(f"""
			select location_id, timestamp, end_timestamp from visits 
			where person_id={person[0]} 
				and timestamp>{(datetime.now()-timedelta(days=14)).timestamp()}""")
		for visit in visits:
			#for each place that person visited, find the people with overlapping visits
			o_people = db.get_db().query(f"""
				select person_id from visits 
				where location_id={visit[0]}
				and end_timestamp>{visit[1]}
				and timestamp<{visit[2]}
				and person_id!={person[0]}""")
			for o_person in o_people:
				#for each person, find the most recent clear of infected test
				stat = db.get_db().query(f"""
					select result from tests 
					where person_id={o_person[0]} 
					and timestamp<{visit[1]}
					order by timestamp DESC limit 1""")
				if stat[0][0]==1:
					infected = infected + 1
				else:
					clear = clear + 1
		data['status'].append({"name": f"{person[1]} {person[2]}", "status": status,"num_infected": infected, "num_other": clear, "num_visits": len(visits)})
	locations = db.get_db().query(f"""
		select first, last, name, timestamp, end_timestamp from people 
		join visits 
			on person_id = people.id
		join locations 
			on location_id = locations.id
		where user_id={uid}
		and timestamp>{(datetime.now()-timedelta(days=1)).timestamp()}
		order by timestamp DESC""")
	loc_list = []
	for loc in locations:
		loc_list.append(list(loc))
		loc_list[-1][3] = str(datetime.fromtimestamp(loc[3]).time())[0:-3]
	data['locations'] = loc_list
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
			elif i == 8:
				end_timestamp = datetime.fromtimestamp(visit[8])
				data['visits'][j].append(int((end_timestamp - timestamp).total_seconds()//60))
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
	data['status'] = []
	uid = flask_login.current_user.get_id()
	people = db.get_db().query(f"select id, first, last from people where user_id={uid}") #get all people for this user
	for person in people:
		infected = 0
		clear = 0
		#get most recent test from this person
		status = db.get_db().query(f"""
			select result from tests 
			where person_id={person[0]} 
			and timestamp<{datetime.now().timestamp()}
			order by timestamp DESC limit 1""")
		if len(status) == 0:
			status = 0
		else:
			status = status[0][0]
		#for each person in group, find all the places that person has visited in teh last 14 days
		visits = db.get_db().query(f"""
			select location_id, timestamp, end_timestamp from visits 
			where person_id={person[0]} 
				and timestamp>{(datetime.now()-timedelta(days=14)).timestamp()}""")
		for visit in visits:
			#for each place that person visited, find the people with overlapping visits
			o_people = db.get_db().query(f"""
				select person_id from visits 
				where location_id={visit[0]}
				and end_timestamp>{visit[1]}
				and timestamp<{visit[2]}
				and person_id!={person[0]}""")
			for o_person in o_people:
				#for each person, find the most recent clear or infected test
				stat = db.get_db().query(f"""
					select result from tests 
					where person_id={o_person[0]} 
					and timestamp<{visit[1]}
					order by timestamp DESC limit 1""")
				if stat[0][0]==1:
					infected = infected + 1
				else:
					clear = clear + 1
		data['status'].append({"name": f"{person[1]} {person[2]}", "status": status,"num_infected": infected, "num_other": clear, "num_visits": len(visits)})
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
	data['statuses'] = db.get_db().query(f"""
		select * from (
			select id, person_id, result, max(timestamp)
				from tests 
				group by person_id)
		join people 
			on person_id = people.id
		where result=1""")
	return render_template('pages/community-exposures.html', data=data)