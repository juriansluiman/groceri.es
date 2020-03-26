import os

class Config:
	SECRET_KEY = 'C&Q7dWjosuKSPTKhLEo&6Q828N^QQD'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///db/app.db' # mysql://username:password@server/databasename
	SQLALCHEMY_TRACK_MODIFICATIONS = False # Suppress warning
	LANGUAGES = ['en', 'nl']