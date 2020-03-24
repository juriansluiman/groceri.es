from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scheduler')
def scheduler():
    return render_template('scheduler.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

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

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
