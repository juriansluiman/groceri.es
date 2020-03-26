from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), nullable=False)
  password = db.Column(db.String(128), nullable=False)

class Setting(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(16), nullable=False)
  value = db.Column(db.String(128), nullable=True)

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  
  prep_time = db.Column(db.Integer)
  cook_time = db.Column(db.Integer)

  servings = db.Column(db.Integer, nullable=False)
  intro = db.Column(db.Text)
  description = db.Column(db.Text, nullable=False)
  rating = db.Column(db.Integer)

  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  category = db.relationship('Category', back_populates='recipes')
  
  #ingredients = db.Column()

class Category(db.Model):
  id      = db.Column(db.Integer, primary_key=True)
  name    = db.Column(db.String(128), nullable=False)

  recipes = db.relationship('Recipe', back_populates='category')

class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  unit = db.Column(db.String(128), nullable=False)

  # shopping_category = db.Column()

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  day = db.Column(db.DateTime, nullable=False)
  name = db.Column(db.String(128), nullable=True)
  note = db.Column(db.Text, nullable=True)

  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
  recipe = db.relationship('Recipe')

class Grocery(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  #ingredient_id = db.Column()
  name = db.Column(db.String(128), nullable=True)
  #meal_id = db.Column() # Verwijderen meal zorgt voor verwijderen boodschappen

class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)