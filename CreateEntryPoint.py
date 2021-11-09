from flask import Flask, render_template, make_response, jsonify, request
import json

# Créa° et lecture des données JSON
app = Flask(__name__)
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


## Création d'un point d'entrée à la racine
@app.route('/', methods=['GET'])  # décorateur de GET
def index():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>"
                         , 200)


## Point d'entrée : Utilisation de templates dans Flask
@app.route("/template", methods=['GET'])
def template():
    # cf 'body_text' dans index.html
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


### POINTS D'ENTREE POUR OBTENIR DES DONNEES

## GET JSON en entier (fichier JSON entier)
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


## GET info d'un film à partir de son ID
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:  # itéra° sur l'array 'movies'
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)

## GET info à partir du titre avec un arg dans la requete
# SYNTAXE : URL/moviesbytitle?title=...
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie
    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res

### Points d'entrée pour modifier, ajt, suppr des données

## POST pour ajt un nv film
@app.route("/movies/<movieid>", methods=["POST"])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res

## PUT pour modifier la note d'un film
@app.route("/movies/<movieid>/<rate>", methods=["PUT"])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res

## DELETE un film
@app.route("/movies/<movieid>", methods=["DELETE"])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
        return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res




if __name__ == "__main__":
    app.run()
