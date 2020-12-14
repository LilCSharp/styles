# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import ProductClient

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
product_client = ProductClient()

from .routes import main
from flask_app.users.routes import users
from flask_app.search.routes import search

def page_not_found(e):
    return render_template("404.html")

def create_app(test_config=None):
    app = Flask(__name__)

    SELF = "'self'"
    Talisman(app,
        content_security_policy = {
            'default-src': [SELF, 'bootstrap', 'ajax'],
            'img-src': '*',
            'script-src': [
                'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js', 
                'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js',
                'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js',
                SELF
            ],
            'style-src': [
                'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
                '//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css',
                'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
                SELF
            ]
        }
    )

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(search)
    app.register_blueprint(users)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app