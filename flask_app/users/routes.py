from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_mail import Message
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
import io
import base64
import face_recognition
import math
from PIL import Image

from .. import bcrypt, product_client
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("search.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = pass_hash)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title = "Register", form = form)

@users.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("search.index"))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username = form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("search.index"))
        else:
            flash("Login failed. Verify your username and password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title = "Login", form = form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("search.index"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    userForm = UpdateUsernameForm()
    profileForm = UpdateProfilePicForm()

    user = User.objects(username = current_user.get_id()).first()

    if userForm.validate_on_submit():
        try:
            userForm.validate_user(userForm.username.data)

            user.modify(username = userForm.username.data)
            user.save()
        except Exception:
            flash("Username is taken")
    
        return redirect(url_for('users.account'))
    
    if profileForm.validate_on_submit():
        img = profileForm.picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        image = face_recognition.load_image_file(img)
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) > 1:
            flash("Please enter a picture with only you inside")
        else:
            face_location = face_locations[0]
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pix = pil_image.load()
            (x_max, y_max) = pil_image.size
            cumulative = 0

            for i in range(0, x_max):
                for j in range(0, y_max):
                    (x, y, z) = pix[i,j]
                    cumulative += math.sqrt(x**2 + y**2 + z**2)

            average = cumulative / (x_max * y_max)

            recs = product_client.get_best_color(average)

            """if user.skin_value is None:
                user.skin_value = average
            else:
                user.modify(skin_value = average)"""

            user.modify(skin_value = average, rec_products = recs)     

        if user.profile_pic.get() is None:
            user.profile_pic.put(img.stream, content_type = content_type)
        else:
            user.profile_pic.replace(img.stream, content_type = content_type)

        user.save()

        return redirect(url_for('users.account'))

    return render_template("account.html", userForm=userForm, picForm=profileForm, image = get_b64_img(user.username))

@users.route("/add_likes", methods=["GET", "POST"])
@login_required
def add_likes():
    user = User.objects(username = current_user.get_id()).first()

    if request.method == 'POST':
        product_id = request.form.get('LIKE')
        likes = user.liked_products

        if likes is None:
            user.modify(liked_products = [product_id])
        else:
            likes.append(product_id)
            user.modify(liked_products = likes)

    return redirect(url_for("search.index"))

@users.route("/likes", methods=["GET", "POST"])
@login_required
def likes():
    user = User.objects(username = current_user.get_id()).first()
    ids = user.liked_products

    result = product_client.get_by_id(ids = ids)

    return render_template(
        "likes.html", products = result
    )

@users.route("/recommended", methods=["GET", "POST"])
@login_required
def recommended():
    user = User.objects(username = current_user.get_id()).first()
    ids = user.rec_products

    result = product_client.get_by_id(ids = ids)

    return render_template(
        "recommended.html", products = result
    )

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image