import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for,
    jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    recipes = list(mongo.db.recipes.find())
    categories = list(mongo.db.categories.find())
    return render_template(
        "recipes.html", recipes=recipes, categories=categories
        )


@app.route("/full_recipe/<recipe_id>")
def full_recipe(recipe_id):
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    full_recipe = list(mongo.db.recipes.find(recipe_id))
    steps = recipe_id['steps']
    ingredients = recipe_id['ingredients']
    return render_template(
        "full_recipe.html", recipe=recipe_id, full_recipe=full_recipe,
        steps=steps, ingredients=ingredients
        )


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "name": request.form.get("name"),
            "time_required": request.form.get("time_required"),
            "preheat_oven": request.form.get("preheat_oven"),
            "dietary_info": request.form.get("dietary_info"),
            "description": request.form.get("description"),
            "comments": request.form.get("comments")
        }
        ingredients = {
            "ingredients": request.form.getlist("ingredients[]")
        }
        steps = {
            "steps": request.form.getlist("step[]")
        }
        recipe.update(ingredients)
        recipe.update(steps)
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("recipes"))
    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(
                request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
