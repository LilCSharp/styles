# 3rd-party packages
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    Blueprint,
    session,
    g,
)
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
import io
import base64

# local
from . import bcrypt, product_client
from .forms import (
    SearchForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
    BrandFilterForm,
    TypeFilterForm,
    UpdateProfilePicForm,
)
from .models import User, load_user

main = Blueprint("main", __name__)