from flask import Blueprint
import os
import click

translate_blueprint = Blueprint('translate', __name__)

@translate_blueprint.cli.command('update')
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate_blueprint.cli.command('compile')
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d translations'):
        raise RuntimeError('compile command failed')


@translate_blueprint.cli.command('init')
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
