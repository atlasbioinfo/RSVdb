from flask import Flask,render_template
from flask import Blueprint
from taolab.blueprints.rsvdb import rsvdb
from taolab.extensions import rdb
from taolab.settings import config
from taolab.models import GSEinfo, Species, SRRinfo,SEARCHlist, DMSTrans, GeneInfo, GeneSearch,Top100,RPKMhist,GiniBox,GiniHist,UTRinfo
from taolab.models import Example
import click

import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app=Flask('taolab')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_errors(app)

    return app

def register_errors(app):
    # @app.errorhandler(400)
    # def bad_request(e):
    #     return render_template('errors/400.html'), 400
    @app.errorhandler(404)
    def pagenotfound(e):
        return render_template('rsvdb/404.html'), 404
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template('errors/404.html'), 404

    # @app.errorhandler(500)
    # def internal_server_error(e):
    #     return render_template('errors/500.html'), 500


def register_blueprints(app):
    app.register_blueprint(rsvdb,url_prefix='/')

def register_extensions(app):
    rdb.init_app(app)

def register_commands(app):      
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="Creat after drop")
    def initdb(drop):
        if drop:
            rdb.drop_all()
        rdb.create_all()
        click.echo("Initialized db")
