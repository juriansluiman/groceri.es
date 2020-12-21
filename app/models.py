from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

recipe_tag = db.Table(
    'recipe_tag',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Set the password to given value"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Validate given password to the user's password"""
        return check_password_hash(self.password, password)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    value = db.Column(db.String(128), nullable=True)

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)

    servings = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', back_populates='recipes')

    ingredients = db.relationship('RecipeIngredient', back_populates='recipe')

    tags = db.relationship('Tag', secondary=recipe_tag, back_populates='recipes')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    recipes = db.relationship('Recipe', back_populates='category')

    def __init__(self, name):
        self.name = name


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    unit = db.Column(db.String(128), nullable=False)

    # shopping_category = db.Column()

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)
    scaling = db.Column(db.Float, default=1)

    recipe = db.relationship("Recipe", back_populates='ingredients')
    ingredient = db.relationship("Ingredient")

    def __init__(self, ingredient, amount, scaling=None):
        self.ingredient = ingredient
        self.amount = amount

        if scaling is not None:
            self.scaling = scaling


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(128), nullable=True)
    note = db.Column(db.Text, nullable=True)
    servings = db.Column(db.Integer, nullable=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe')

    def __init__(self, day, recipe=None, name=None, note=None, servings=None):
        self.day = day

        if recipe is not None:
            self.recipe = recipe
        if name is not None:
            self.name = name
        if note is not None:
            self.note = note
        if servings is not None:
            self.servings = servings


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ingredient_id = db.Column()
    name = db.Column(db.String(128), nullable=True)
    #meal_id = db.Column() # Verwijderen meal zorgt voor verwijderen boodschappen


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    recipes = db.relationship('Recipe', secondary=recipe_tag, back_populates='tags')

    def __init__(self, name):
        self.name = name
