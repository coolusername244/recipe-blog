import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
    return render_template("recipes.html", recipes=recipes)


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
            "name": request.form.get("name"),
            "time_required": request.form.get("time_required"),
            "preheat_oven": request.form.get("preheat_oven"),
            "ingredients": request.form.get("ingredients"),
            "allergy_info": request.form.get("allergy_info"),
            "description": request.form.get("description"),
            "step_one": request.form.get("step_one"),
            "step_two": request.form.get("step_two"),
            "step_three": request.form.get("step_three"),
            "step_four": request.form.get("step_four"),
            "step_five": request.form.get("step_five"),
            "step_six": request.form.get("step_six"),
            "step_seven": request.form.get("step_seven"),
            "step_eight": request.form.get("step_eight"),
            "step_nine": request.form.get("step_nine"),
            "step_ten": request.form.get("step_ten"),
            "step_eleven": request.form.get("step_eleven"),
            "step_twelve": request.form.get("step_twelve"),
            "step_thirteen": request.form.get("step_thirteen"),
            "step_fourteen": request.form.get("step_fourteen"),
            "step_fifteen": request.form.get("step_fifteen"),
            "comments": request.form.get("comments")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("recipes"))
    return render_template("add_recipe.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
