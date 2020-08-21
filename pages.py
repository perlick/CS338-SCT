from flask import Blueprint, request, jsonify, render_template
from database import Database as db

pages = Blueprint('pages', __name__)

@pages.route('/home')
def pages_home():
	return render_template('pages/home.html')

@pages.route('/locations')
def pages_locations():
	return render_template('pages/locations.html')

@pages.route('/test-reports')
def pages_testReports():
	return render_template('pages/test-reports.html')

@pages.route('/exposure-history')
def pages_exposureHistory():
	return render_template('pages/exposure-history.html')

@pages.route('/family-manager')
def pages_familyManager():
	return render_template('pages/family-manager.html')

@pages.route('/community-exposures')
def pages_communityExposures():
	return render_template('pages/community-exposures.html')

@pages.route('/settings')
def pages_settings():
	return render_template('pages/settings.html')