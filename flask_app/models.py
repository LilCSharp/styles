from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
import io
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField(required=False)
    skin_value = db.FloatField(required=False)
    liked_products = db.ListField(required=False)
    rec_products = db.ListField(required=False)

    def get_id(self):
        return self.username

    def get_b64_img(self):
        bytes_im = io.BytesIO(self.profile_pic.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        return image