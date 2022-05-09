from flask import Flask, render_template, request, Response
import numpy as np
import pandas as pd
from my_model import model
import pickle


app = Flask(__name__)


@app.route("/contactus", methods=["GET"])
def contact():
    return render_template("contactus.html")


@app.route("/team", methods=["GET"])
def team():
    return render_template("team.html")


@app.route("/", methods=["GET", "POST"])
def results():
    try:
        movie_name = request.form["myInput"]
        movies = pickle.load(open("movie_list.pkl", "rb"))
        name_list = []
        for item in movies["title"]:
            name_list.append(item)
        recommender_model = model()
        name, posters, code = recommender_model.recommend(movie_name)
        data = zip(name, posters, code)
        return render_template("index.html", data=data, movie_names=name_list)

    except:
        movies = pickle.load(open("movie_list.pkl", "rb"))
        name_list = []
        for item in movies["title"]:
            name_list.append(item)
        return render_template("index.html", movie_names=name_list)


if __name__ == "__main__":
    app.run(debug=False, port=8080)
    # app.run(host="0.0.0.0")
