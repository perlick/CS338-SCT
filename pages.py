from flask import Blueprint, request, jsonify, render_template
from database import Database as db

pages = Blueprint('pages', __name__)

@pages.route('/home')
def pages_home():
	data = {}
	data['title'] = "SCT"
	data['menu'] = True
	return render_template('pages/home.html', data=data)

@pages.route('/locations')
def pages_locations():
	data = {}
	data['title'] = "Locations"
	return render_template('pages/locations.html', data=data)

@pages.route('/test-reports')
def pages_testReports():
	data = {}
	data['title'] = "Test Reports"
	return render_template('pages/test-reports.html', data=data)

@pages.route('/exposure-history')
def pages_exposureHistory():
	data = {}
	data['title'] = "Exposure History"
	return render_template('pages/exposure-history.html', data=data)

@pages.route('/family-manager')
def pages_familyManager():
	data = {}
	data['title'] = "Family Manager"
	return render_template('pages/family-manager.html', data=data)

@pages.route('/community-exposures')
def pages_communityExposures():
	data = {}
	data['title'] = "Community Exposures"
	return render_template('pages/community-exposures.html', data=data)

@pages.route('/settings')
def pages_settings():
	data = {}
	data['title'] = "Settings"
	return render_template('pages/settings.html', data=data)