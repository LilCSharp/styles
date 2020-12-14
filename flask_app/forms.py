from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectMultipleField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp
)

from .models import User

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators = [InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

class BrandFilterForm(FlaskForm):
    selection = SelectMultipleField(
        choices = [
            ("almay", "almay" ), ("alva", "alva"), ("anna sui", "anna sui"), 
            ("annabelle", "annabelle"), ("benefit", "benefit"), ("boosh", "boosh"),
            ("burt's bees", "burt's bees"), ("butter london", "butter london"),
            ("c'est moi", "c'est moi"), ("cargo cosmetics", "cargo cosmetics"),
            ("china glaze", "china glaze"), ("clinique", "clinique"),
            ("coastal classic creation", "coastal classic creation"),
            ("colourpop", "colourpop"), ("covergirl", "covergirl"),
            ("dalish", "dalish"), ("deciem", "deciem"), ("dior", "dior"),
            ("dr. hauschka", "dr. hauschka"), ("e.l.f", "e.l.f"),
            ("essie", "essie"), ("fenty", "fenty"), ("glossier", "glossier"), 
            ("green people", "green people"), ("iman", "iman"), ("l'oreal", "l'oreal"),
            ("lotus cosmetics usa", "lotus cosmetics usa"),
            ("maia's mineral galaxy", "maia's mineral galaxy"), 
            ("marcelle", "marcelle"), ("marienatie", "marienatie"),
            ("maybelline", "maybelline"), ("milani", "milani"), 
            ("mineral fusion", "mineral fusion"),
            ("misa", "misa"), ("mistura", "mistura"), ("moov", "moov"),
            ("nudus", "nudus"), ("nyx", "nyx"), ("orly", "orly"), ("pacifica", "pacifica"),
            ("penny lane organics", "penny lane organics"),
            ("physicians formula", "physicians formula"),
            ("piggy paint", "piggy paint"), ("pure anada", "pure anada"),
            ("rejuva minerals", "rejuva minerals"),
            ("revlon", "revlon"), ("sally b's skin yummies", "sally b's skin yummies"),
            ("salon perfect", "salon perfect"), ("sante", "sante"), 
            ("sinful colours", "sinful colours"), ("smashbox", "smashbox"),
            ("stila", "stila"), ("suncoat", "suncoat"), 
            ("w3llpeople", "w3llpeople"), ("wet n wild", "wet n wild"),
            ("zorah", "zorah"), ("zorah bioscosmetiques", "zorah bioscosmetiques")
        ]
    )

    submit = SubmitField("Filter Brands")

class TypeFilterForm(FlaskForm):
    selection = SelectMultipleField(
        choices = [
            ("blush", "blush"), ("bronzer", "bronzer"), ("eyebrow", "eyebrow"), 
            ("eyeliner", "eyeliner"), ("eyeshadow", "eyeshadow"), ("foundation", "foundation"),
            ("lip liner", "lip liner"), ("lipstick", "lipstick"), ("mascara", "mascara"), 
            ("nail polish", "nail polish")
        ]
    )

    submit = SubmitField("Filter Categories")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=8, max=32), Regexp("[A-Z]+.*[!\-^#@$&]+.*|[!\-^#@$&]+.*[A-Z]+.*")])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class ConfirmForm(FlaskForm):
    code = StringField("Your code", validators=[InputRequired()])
    submit = SubmitField("Login")

class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")

class UpdateProfilePicForm(FlaskForm):
    picture = FileField("Insert jpg or png", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'])
    ])

    submit = SubmitField("Change profile pic")