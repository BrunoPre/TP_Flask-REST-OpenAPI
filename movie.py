from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# define custom host and port to make the app public
# if commented (and the last lines of the script), open provided URL or localhost
#PORT = 3200
#HOST = '192.168.0.15'

PORT = 3202
HOST = '127.0.0.1' # localhost

PORT_BOOKING = '3201'
HOST_BOOKING = HOST

PORT_SHOWTIME = '3200'
HOST_SHOWTIME = HOST

with open('{}/databases/movies.json'.format("."), "r") as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

# to test templates of Flask
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

# get the complete json file
@app.route("/movies", methods=['GET'])
def get_json():
    #res = make_response(jsonify(INFO), 200)
    res = make_response(jsonify(movies), 200)
    return res

# get a movie info by its ID
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie, discoverability(movie)),200) # both movie and discoverability are JSONified
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)
    
# add a new movie
@app.route("/movies/<movieid>", methods=["POST"])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"},discoverability(movie)),409)

    movies.append(req)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

# delete a movie
@app.route("/movies/<movieid>", methods=["DELETE"])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res


# delete movies whose rate is lower than a given rate
# SYNTAX : URL/moviesbyrate?rate=...
@app.route("/moviesbyrate", methods=["DELETE"])
def del_movie_byLowerRate():
    if request.args:
        req = request.args
        rate = float(req["rate"]) # all request's args are strings
        for movie in movies:
            if movie["rating"] <= rate:
                movies.remove(movie)

    return make_response(jsonify(movies),200)


# get movies by a director's name
# through a query
# SYNTAX : URL/moviesbydirector?director=...
@app.route("/moviesbydirector", methods=['GET'])
def get_movie_moviesbydirector():
    json = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                json.append(movie)

    if not json:
        res = make_response(jsonify({"error" : "movie title not found"}),400)
    else:
        res = make_response(jsonify(json,discoverability(json[0])),200)
    return res



# get a movie info by its name
# through a query
# SYNTAX : URL/moviesbytitle?title=...
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:        
            if str(movie["title"]) == str(req["title"]):
                json = movie
                
    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json,discoverability(json)),200)
    return res

# change a movie rating
@app.route("/movies/<movieid>/<rate>", methods=["PUT"])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie,discoverability(movie)),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res


# discoverability function to be RESTful, given a movie
def discoverability(movie):

    head = "/movies/"
    id = movie["id"]
    title = movie["title"]

    return {
        "possible_requests": [
            # GET by movie id
            {
            "method" : "GET",
            "uri" : head + id
            },
            # GET by movie title
            {
            "method" : "GET",
            "uri" : "/moviesbytitle?title=" + title
            },
            # DELETE by movie id
            {
            "method" : "DELETE",
            "uri" : head + id
            },
            # PUT the movie rate
            {
            "method" : "PUT",
            "uri" : head + id + "/<rate>"
            }
        ]
    }

if __name__ == "__main__":
    #print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
    #app.run()
