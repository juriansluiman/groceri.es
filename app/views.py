from app import app, db
from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from sqlalchemy.sql.expression import func
from models import User, Setting, Category, Tag, Recipe, Ingredient
from forms import LoginForm


@app.route('/')
def home():
    recipes = Recipe.query.order_by(func.random()).limit(4).all()

    return render_template('home.html', recipes=recipes)


@app.route('/scheduler')
@login_required
def scheduler():
    return render_template('scheduler.html')


@app.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.order_by('id', Recipe.id.asc()).all()

    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/search')
@login_required
def search():
    query = request.args.get('q')

    result = {'results': [
        {'title':'Naan delicious', 'description':'Some delicious tajine with naan', 'image':'/static/food/example-1.jpg', 'url':'/recipes/1/naan'},
        {'title':'Pasta something', 'description':'A pasta with a smooth sauce', 'image':'/static/food/example-2.jpg', 'url':'/recipes/2/pasta'},
        {'title':'Fish curry', 'description':'Simple comfort food', 'image':'/static/food/example-3.jpg', 'url':'/recipes/3/curry'}
    ]}

    return jsonify(result)


@app.route('/recipes/<int:id>/<title>')
@login_required
def recipe(id, title=None):
    return render_template('recipe.html')


@app.route('/groceries')
@login_required
def groceries():
    return render_template('groceries.html')


@app.route('/pantry')
@login_required
def pantry():
    return render_template('pantry.html')


@app.route('/settings')
@login_required
def settings():
    user = User.query.first()

    count = {
      'recipes': Recipe.query.count(),
      'ingredients': Ingredient.query.count(),
      'tags': Tag.query.count(),
      'categories': Category.query.count()
    }

    # Query all settings and create a dict with the setting's name as key
    settings = Setting.query.all()
    settings = dict([(s.name, s) for s in settings])

    settings['available_languages'] = app.config['LANGUAGES']

    return render_template('settings.html', user=user, count=count, settings=settings)


@app.route('/settings/ingredients')
@login_required
def ingredients():
    ingredients = Ingredient.query.all()

    return render_template('ingredients.html', ingredients=ingredients)


@app.route('/settings/tags')
@login_required
def tags():
    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/settings/categories')
@login_required
def categories():
    categories = Category.query.all()

    return render_template('categories.html', categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    # Clear up database first
    User.query.delete()
    Setting.query.delete()
    Category.query.delete()
    Tag.query.delete()
    Recipe.query.delete()

    jurian = User(name='jurian', email='jurian@slui.mn', password=generate_password_hash('password'))

    grocery_day             = Setting('grocery_day', 'sat')
    default_servings        = Setting('default_servings', '2')
    allow_user_registration = Setting('allow_user_registration', 'true')
    default_language        = Setting('default_language', 'nl')

    starter   = Category('Starter')
    main      = Category('Main')
    side_dish = Category('Side dish')
    desert    = Category('Desert')
    breakfast = Category('Breakfast')
    lunch     = Category('Lunch')

    vegetarian = Tag('Vegetarian')
    indian     = Tag('Indian')
    italian    = Tag('Italian')
    moroccan   = Tag('Moroccan')

    recipe1 = Recipe(name='Fish curry', servings=4, prep_time=15, cook_time=30, category=main,
        intro='A delicious but simple curry',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe2 = Recipe(name='Pasta something', servings=4, prep_time=20, cook_time=15, category=main,
        intro='Quick pasta for a working day meal',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe3 = Recipe(name='Weekend tajine', servings=4, prep_time=30, cook_time=60, category=main,
        intro='Something truly the waiting for during a weekend',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe4 = Recipe(name='Fish curry', servings=4, prep_time=15, cook_time=30, category=main,
        intro='A delicious but simple curry',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe5 = Recipe(name='Pasta something', servings=4, prep_time=20, cook_time=15, category=main,
        intro='Quick pasta for a working day meal',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe6 = Recipe(name='Weekend tajine', servings=4, prep_time=30, cook_time=60, category=main,
        intro='Something truly the waiting for during a weekend',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe7 = Recipe(name='Fish curry', servings=4, prep_time=15, cook_time=30, category=main,
        intro='A delicious but simple curry',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe8 = Recipe(name='Pasta something', servings=4, prep_time=20, cook_time=15, category=main,
        intro='Quick pasta for a working day meal',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe9 = Recipe(name='Weekend tajine', servings=4, prep_time=30, cook_time=60, category=main,
        intro='Something truly the waiting for during a weekend',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe10 = Recipe(name='Fish curry', servings=4, prep_time=15, cook_time=30, category=main,
        intro='A delicious but simple curry',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe11 = Recipe(name='Pasta something', servings=4, prep_time=20, cook_time=15, category=main,
        intro='Quick pasta for a working day meal',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    recipe12 = Recipe(name='Weekend tajine', servings=4, prep_time=30, cook_time=60, category=main,
        intro='Something truly the waiting for during a weekend',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    session = db.session
    session.add(jurian)
    session.add(grocery_day)
    session.add(default_servings)
    session.add(allow_user_registration)
    session.add(default_language)
    session.add(starter)
    session.add(main)
    session.add(side_dish)
    session.add(desert)
    session.add(breakfast)
    session.add(lunch)
    session.add(vegetarian)
    session.add(indian)
    session.add(italian)
    session.add(moroccan)
    session.add(recipe1)
    session.add(recipe2)
    session.add(recipe3)
    session.add(recipe4)
    session.add(recipe5)
    session.add(recipe6)
    session.add(recipe7)
    session.add(recipe8)
    session.add(recipe9)
    session.add(recipe10)
    session.add(recipe11)
    session.add(recipe12)
    session.commit()

    return redirect(url_for('home'))
