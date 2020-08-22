from flask import Blueprint, request, jsonify, render_template
import flask_login
from database import Database as db

pages = Blueprint('pages', __name__)

@pages.route('/home')
@flask_login.login_required
def pages_home():
	data = {}
	data['title'] = "SCT"
	data['menu'] = True
	return render_template('pages/home.html', data=data)

@pages.route('/locations')
@flask_login.login_required
def pages_locations():
	data = {}
	data['title'] = "Locations"
	return render_template('pages/locations.html', data=data)

@pages.route('/test-reports')
@flask_login.login_required
def pages_testReports():
	data = {}
	data['title'] = "Test Reports"
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
	return render_template('pages/family-manager.html', data=data)

@pages.route('/community-exposures')
@flask_login.login_required
def pages_communityExposures():
	data = {}
	data['title'] = "Community Exposures"
	return render_template('pages/community-exposures.html', data=data)

@pages.route('/settings')
@flask_login.login_required
def pages_settings():
	data = {}
	data['title'] = "Settings"
	return render_template('pages/settings.html', data=data)