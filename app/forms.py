from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RecipeForm(FlaskForm):
    cook_time = IntegerField('Cook Time',
        validators=[DataRequired(), NumberRange(min=1, max=60*24*7)])
    description = StringField('Description', validators=[DataRequired()])
    intro = StringField('Intro', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    prep_time = IntegerField('Prep Time',
        validators=[DataRequired(), NumberRange(min=1, max=60*24*7)])
    servings = IntegerField('Servings',
        validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Create')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
