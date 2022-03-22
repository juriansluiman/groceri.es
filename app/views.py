import logging

from app import app, db
from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from sqlalchemy.sql.expression import func
from slugify import slugify
from forms import LoginForm, RecipeForm, RegisterForm
from models import User, Setting, Category, Tag, Recipe, Ingredient, \
    RecipeIngredient, Meal
from datetime import date, timedelta
from collections import defaultdict

LOGGER = logging.getLogger(__name__)
SETTING_DEFAULTS = {
    "allow_user_registration" :  True,
    "default_servings"        :  2,
    "default_language"        :  "en-us",
    "grocery_day"             :  "sat",
}


@app.route('/')
def home():
    recipes = Recipe.query.order_by(func.random()).limit(4).all()
    meals = Meal.query.filter(Meal.day >= date.today()) \
                      .order_by(Meal.day).all()

    days = defaultdict(list)
    for meal in meals:
        days[str(meal.day)].append(meal)

    return render_template('home.html', recipes=recipes, days=days)


@app.route('/scheduler')
@login_required
def scheduler():
    return render_template('scheduler.html')


@app.route('/recipes')
@login_required
def recipes():
    filter = dict()
    filter['query'] = request.args.get('query')
    filter['categories'] = request.args.getlist('category')
    filter['tags'] = request.args.getlist('tag')

    day = request.args.get('day')

    query = Recipe.query.order_by(func.random())
    if filter['query']:
        query = query.filter(Recipe.name.ilike('%{}%'.format(filter['query'])))
    if filter['categories']:
        query = query.filter(Recipe.category.has(
                    Category.name.in_(filter['categories'])
                ))
    if filter['tags']:
        query = query.filter(Recipe.tags.any(
                    Tag.name.in_(filter['tags'])
                ))

    recipes = query.all()
    categories = Category.query.all()
    tags = Tag.query.all()

    return render_template('recipes.html',
                           recipes=recipes, categories=categories, tags=tags,
                           filter=filter, day=day)

@app.route('/recipes/new', methods=["GET", "POST"])
@login_required
def recipe_new():
    """Create a new recipe."""
    form = RecipeForm()
    LOGGER.debug("New recipe form.")
    if form.validate_on_submit():
        LOGGER.debug("Validating new recipe form.")
        recipe = Recipe(
            cook_time = form.cook_time.data,
            description = form.description.data,
            name = form.name.data,
            prep_time = form.prep_time.data,
            servings = form.servings.data,
            intro = form.intro.data,
        )
        session = db.session
        session.add(recipe)
        session.commit()
        LOGGER.info("Created recipe %s", form.name.data)
        return redirect(url_for('recipe', id=recipe.id))
    else:
        for error in form.errors:
            LOGGER.debug("Error: %s", error)


    return render_template('recipe_new.html', form=form)


@app.route('/recipes/search')
@login_required
def search():
    query = request.args.get('q')
    result = {'results': []}

    if query:
        clauses = [Recipe.name.ilike('%{}%'.format(k)) for k in query.split()]
        recipes = Recipe.query.filter(*clauses).all()
        for recipe in recipes:
            result['results'].append({
                'title': recipe.name,
                'description': recipe.intro,
                'image': '/static/food/example-{}.jpg'.format(recipe.id),
                'link': url_for('recipe', id=recipe.id, name=slugify(recipe.name))
            })

    return jsonify(result)


@app.route('/recipes/<int:id>')
@app.route('/recipes/<int:id>/<name>')
@login_required
def recipe(id, name=None):
    recipe = Recipe.query.get_or_404(id)
    slug = slugify(recipe.name)

    if slug != name:
        return redirect(url_for('recipe', id=recipe.id, name=slug))

    return render_template('recipe.html', recipe=recipe)


@app.route('/recipes/<int:id>', methods=['PATCH'])
@login_required
def recipe_update(id):
    recipe = Recipe.query.get_or_404(id)

    recipe.rating = request.json.get('rating')
    db.session.commit()

    return '', 204


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
    user = current_user

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
    for k, v in SETTING_DEFAULTS.items():
        settings[k] = settings.get(k, v)

    return render_template('settings.html',
                           user=user, count=count, settings=settings)


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

    return render_template('login.html', form=form, register_link=url_for("register"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user:
            LOGGER.info("Username '%s' already taken.", form.username.data)
            flash('Username already taken, please choose another')
            return redirect(url_for('register'))

        user = User(
            email=form.email.data,
            name=form.username.data,
            password=generate_password_hash(form.password.data))

        session = db.session
        session.add(user)
        session.commit()
        LOGGER.info("Created user %s", form.username.data)

        login_user(user, remember=False)
        return redirect(url_for('home'))


    return render_template('register.html', form=form)


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
    Ingredient.query.delete()
    RecipeIngredient.query.delete()
    Meal.query.delete()

    grocery_day             = Setting('grocery_day', 'sat')
    default_servings        = Setting('default_servings', '2')
    allow_user_registration = Setting('allow_user_registration', 'true')
    default_language        = Setting('default_language', 'en')

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
    lactose    = Tag('Lactose free')

    recipe1 = Recipe(
        name='Fish curry', servings=4, prep_time=15, cook_time=30,
        category=main, intro='A delicious but simple curry',
        description="""Wash and cook the rice.\n\nStart with oil and fry the
            paste for 5 minutes. Add the fish and coconut milk. Poach fish until
            tender. Finalize with coriander.""")

    rice = Ingredient('Rice', 'g')
    paste = Ingredient('Curry paste', 'ts')
    fish = Ingredient('White fish', 'g')
    coconut = Ingredient('Coconut milk', 'ml')
    coriander = Ingredient('Coriander', 'g')

    recipe1.ingredients.append(RecipeIngredient(rice, 320))
    recipe1.ingredients.append(RecipeIngredient(paste, 3, 0.75))
    recipe1.ingredients.append(RecipeIngredient(fish, 400))
    recipe1.ingredients.append(RecipeIngredient(coconut, 150))
    recipe1.ingredients.append(RecipeIngredient(coriander, 20))

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

    recipe11 = Recipe(name='Zaalouk', servings=4, prep_time=15, cook_time=0, category=side_dish,
        intro='Moroccan Vegetable side dish',
        description="Cut the eggplants to cubes, if you like you can peel the eggplant not completely you leave some skin on them for the dark look.\n\nCut the tomato to fine slices")

    recipe12 = Recipe(name='A very long title with multiple words', servings=4, prep_time=30, cook_time=60, category=main,
        intro='Something truly the waiting for during a weekend',
        description="Start with bla bla and then\nDo some more steps\n\nEnjoy!")

    session = db.session
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
    session.add(lactose)
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

    recipe1.tags.append(indian)
    recipe1.tags.append(lactose)

    recipe11.tags.append(moroccan)

    session.commit()

    today = Meal(date.today(), recipe1)
    tomorrow = Meal(date.today() + timedelta(days=1), recipe2)
    tomorrow1 = Meal(date.today() + timedelta(days=1), name='Green salad', note='Use rocket salad from yesterday')
    tomorrow2 = Meal(date.today() + timedelta(days=2),
                     name='Rösti with lamb and red cabbage',
                     note='Rösti from freezer, check lamb first!')
    tomorrow3 = Meal(date.today() + timedelta(days=3), recipe3, servings=4)
    tomorrow4 = Meal(date.today() + timedelta(days=4), name='Chicken biryani')
    tomorrow5 = Meal(date.today() + timedelta(days=5), recipe9)
    tomorrow6 = Meal(date.today() + timedelta(days=5), recipe11)

    session.add(today)
    session.add(tomorrow)
    session.add(tomorrow1)
    session.add(tomorrow2)
    session.add(tomorrow3)
    session.add(tomorrow4)
    session.add(tomorrow5)
    session.add(tomorrow6)

    session.commit()

    return redirect(url_for('home'))
