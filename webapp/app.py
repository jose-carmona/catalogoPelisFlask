import logging

from flask import Flask
from flask_assistant import Assistant, ask
from cat import get_config, read_google_sheet, q, compose_answer, Sheet

from injector import Injector, inject, Module, provider, singleton

from flask_injector import FlaskInjector

class AppModule(Module):
    @provider
    @singleton
    def provide_sheet(self) -> Sheet:
        
        return read_google_sheet(get_config())

def configure_views(app):
    @app.route('/', methods=['GET'])
    def homepage():
        app.logger.info('route: /')
        return 'Hi!'

    @app.route('/test/q/<any>', methods=['GET'])
    def test_q(sh: Sheet, any):
        app.logger.info(f'route: /test/q/{any}')
        
        sel = q(sh, any.split())
        return compose_answer(any, sel)

def configure_assistant(assistant):

    @assistant.action('Buscar Peli')
    @inject
    def query(sh: Sheet, any):
        sel = q(sh, any.split())
        return ask(compose_answer(any, sel))

    @assistant.action('Testear')
    def answer():
        return ask('Yes you can!')

def init(module = AppModule()):
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    injector = Injector([module])

    configure_views(app)
    FlaskInjector(app=app, injector=injector)

    assistant = Assistant(app, route='/wh/', project_id='YOUR_PROJECT_ID', injector=injector)
    configure_assistant(assistant)

    return app
