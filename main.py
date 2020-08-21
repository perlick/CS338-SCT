from flask import Flask, render_template
from api import api
from pages import pages

app = Flask(__name__, static_folder='public', static_url_path='')

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pages, url_prefix='/')

@app.route('/')
def index():
	return render_template('pages/home.html')

@app.teardown_appcontext
def close_connection(exception):
	try:
		db = getattr(g, '_database', None)
		db.close()
	except NameError:
		pass

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8080, debug=True)