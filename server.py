from flask import Flask, render_template, request, redirect
import utils
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "OkT81%Y}y7ihQcjZ5HkN"


@app.route("/")
def index():
	return render_template('main.html')


@app.route("/desmos", methods=['GET', 'POST'])
def desmos():
	equations = []
	shape = (10, 10)
	if request.method == 'POST':
		_type = request.form['options']
		file = request.files['file']
		if file.filename == '' or not allowed_file(file.filename):
			return redirect('/')
		if _type == 'bezier':
			equations, shape = utils.get_bezier_formula(file)
		elif _type == 'conic':
			equations, shape = utils.get_bezier_formula(file)
		else:
			return redirect('/')
	return render_template('desmos.html', equations=json.dumps(equations).replace('\\', '\\\\'), width=str(shape[1]), height=str(shape[0]))


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.run(host='0.0.0.0', port=8080, debug=True)

# TODO: Add conic equations
