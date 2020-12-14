from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import product_client
from ..forms import BrandFilterForm, SearchForm, TypeFilterForm
from ..models import User

search = Blueprint('search', __name__)

@search.route("/", methods=["GET", "POST"])
def index():

    query = SearchForm()
    brandForm = BrandFilterForm()
    typeForm = TypeFilterForm()

    if query.validate_on_submit():
        product_client.search(query.search_query.data.lower())

    return render_template(
        "index.html", query = query, brandForm = brandForm, 
        typeForm = typeForm, products = product_client.data
    )

@search.route("/filter", methods=["GET", "POST"])
def filter():
    brandForm = BrandFilterForm()
    typeForm = TypeFilterForm()
    
    if brandForm.validate_on_submit():
        brand = brandForm.selection.data
        product_type = []

        product_client.filter(brand, product_type)

    if typeForm.validate_on_submit():
        brand = []
        product_type = typeForm.selection.data

        product_client.filter(brand, product_type)

    return redirect(url_for("search.index"))

@search.route("/show_all", methods=["GET", "POST"])
def show_all():
    product_client.get_all()

    return redirect(url_for("search.index"))

@search.route("/description", methods=["GET", "POST"])
def description():
    return render_template("description.html")