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
        "recipes.html",
        recipes=recipes,
        categories=categories
        )


@app.route("/full_recipe/<recipe_id>")
def full_recipe(recipe_id):
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    full_recipe = list(mongo.db.recipes.find(recipe_id))
    steps = recipe_id['steps']
    ingredients = recipe_id['ingredients']
    return render_template(
        "full_recipe.html",
        recipe=recipe_id,
        full_recipe=full_recipe,
        steps=steps,
        ingredients=ingredients
        )


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
                request.form.get("password")),
            "is_admin": False
        }
        mongo.db.users.insert_one(register)
        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")
        return redirect(url_for(
            "my_recipes",
            username=session["user"]
            ))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get(
                    "password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_recipes",
                    username=session["user"]
                    ))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesnt exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    recipes = list(mongo.db.recipes.find())
    categories = list(mongo.db.categories.find())

    if session["user"]:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template(
            "my_recipes.html",
            username=username,
            recipes=recipes,
            categories=categories
            )

    return render_template(url_for("login"))


@app.route("/logout")
def logout():
    # remove use from session cookies
    flash("You have been logged out!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        recipe = {
            "category_name": request.form.get("category_name"),
            "name": request.form.get("name"),
            "time_required": request.form.get("time_required"),
            "preheat_oven": request.form.get("preheat_oven"),
            "dietary_info": request.form.get("dietary_info"),
            "description": request.form.get("description"),
            "comments": request.form.get("comments"),
            "created_by": username
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
    return render_template(
        "add_recipe.html",
        categories=categories
        )


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Deleted!")
    return redirect(url_for("my_recipes"))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        updated_recipe = {
            "category_name": request.form.get("category_name"),
            "name": request.form.get("name"),
            "time_required": request.form.get("time_required"),
            "preheat_oven": request.form.get("preheat_oven"),
            "dietary_info": request.form.get("dietary_info"),
            "description": request.form.get("description"),
            "comments": request.form.get("comments"),
            "created_by": session["user"]
        }
        ingredients = {
            "ingredients": request.form.getlist("ingredients[]")
        }
        steps = {
            "steps": request.form.getlist("step[]")
        }
        updated_recipe.update(ingredients)
        updated_recipe.update(steps)
        mongo.db.recipes.update({"_id": ObjectId}, updated_recipe)
        flash("Recipe updated!")

    categories = mongo.db.categories.find()
    steps = mongo.db.recipes.find_one("steps[]")
    ingredients = mongo.db.recipes.find_one("ingredients[]")
    return render_template(
        "edit_recipe.html",
        categories=categories,
        steps=steps,
        ingredients=ingredients
        )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
