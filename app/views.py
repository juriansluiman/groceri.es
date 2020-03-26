from app import app
from flask import request, jsonify, render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scheduler')
def scheduler():
    return render_template('scheduler.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/recipes/search')
def search():
	query = request.args.get('q')

	result = {'results': [
		{'title':'Naan delicious', 'description':'Some delicious tajine with naan', 'image':'/static/food/example-1.jpg', 'url':'/recipes/1/naan'},
		{'title':'Pasta something', 'description':'A pasta with a smooth sauce', 'image':'/static/food/example-2.jpg', 'url':'/recipes/2/pasta'},
		{'title':'Fish curry', 'description':'Simple comfort food', 'image':'/static/food/example-3.jpg', 'url':'/recipes/3/curry'}
	]}

	return jsonify(result)

@app.route('/recipes/<int:id>/<title>')
def recipe_detail(id, title=None):
	return render_template('recipe_detail.html')

@app.route('/groceries')
def groceries():
    return render_template('groceries.html')

@app.route('/pantry')
def pantry():
    return render_template('pantry.html')

@app.route('/settings')
def settings():	
    return render_template('settings.html')

@app.route('/settings/ingredients')
def ingredients():
	return render_template('ingredients.html')

@app.route('/settings/tags')
def tags():
	return render_template('tags.html')

@app.route('/login', methods=['GET','POST'])
def login():
	pass