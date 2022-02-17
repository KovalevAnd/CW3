from flask import Flask, render_template
from flask_restx import Api

from project.config import DevelopmentConfig
from project.setup_db import db
from project.views.genres import genres_ns
from project.views.directors import directors_ns
from project.views.movies import movies_ns

api = Api(title="Flask Course Project 3", doc="/docs")


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    @app.route('/')
    def index():
        return render_template('index.html')

    db.init_app(app)
    api.init_app(app)

    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)

    return app
