import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for,
    jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    return render_template("recipes.html", recipes=recipes, categories=categories)


@app.route("/full_recipe/<recipe_id>")
def full_recipe(recipe_id):
    recipe_id = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    full_recipe = list(mongo.db.recipes.find(recipe_id))
    return render_template(
        "full_recipe.html", recipe=recipe_id, full_recipe=full_recipe
        )


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "name": request.form.get("name"),
            "time_required": request.form.get("time_required"),
            "preheat_oven": request.form.get("preheat_oven"),
            "ingredients": request.form.get("ingredients"),
            "allergy_info": request.form.get("allergy_info"),
            "description": request.form.get("description"),
            "comments": request.form.get("comments")
        }
        steps = {
            "steps": request.form.getlist("step[]")
        }
        recipe.update(steps)
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("recipes"))
    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
