import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3204 # not to be confused with others' port
HOST = '127.0.0.1' # localhost

PORT_BOOKING = '3201'
HOST_BOOKING = HOST

PORT_MOVIE = '3202'
HOST_MOVIE = HOST

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>",200)

# TODO : GET /users --> get the full JSON database
@app.route("/users", methods=['GET'])
def get_users():
    return make_response(jsonify(users),200)

# get a user info by its ID
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user, discoverability(user)),200) # both user and discoverability are JSONified
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

# get all the movies
@app.route("/users/movies", methods=['GET'])
def get_movies():
    movies = requests.get('http://' + HOST_MOVIE + ':' + PORT_MOVIE + '/movies')
    movies = movies.json()
    res = make_response(jsonify(movies), 200)
    return res

# get a user's bookings
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_bookings(userid):
    bookings = requests.get('http://' + HOST_BOOKING + ':' + PORT_BOOKING + '/bookings/' + userid)
    bookings = bookings.json()
    res = make_response(jsonify(bookings), 200)
    return res

# get the movies scheduled on a given date
@app.route("/users/movies/<date>", methods=['GET'])
def get_moviesByDate(date):
    movies = requests.get('http://' + HOST_BOOKING + ':' + PORT_BOOKING + '/bookings/showtimes/' + date)
    movies = movies.json()
    res = make_response(jsonify(movies), 200)
    return res


# add a new user
@app.route("/users/<userid>", methods=["POST"])
def create_user(userid):
    req = request.get_json()

    # check if the user already exists in the database
    for user in users:
        if str(user["userid"]) == str(userid):
            return make_response(jsonify({"error":"user ID already exists"},discoverability(user)),409)

    users.append(req)
    res = make_response(jsonify({"message":"user added"}),200)
    return res

#POST  add a booking to a user
@app.route("/users/<userid>/bookings", methods=['POST'])
def get_bookings(userid):
    bookings = requests.post('http://' + HOST_BOOKING + ':' + PORT_BOOKING + '/bookings/' + userid)
    bookings = bookings.json()
    res = make_response(jsonify(bookings), 200)
    return res

    

# discoverability function to be RESTful, given a user
def discoverability(user):

    head = "/users/"
    id = user["id"]

    return {
        "possible_requests": [
            # GET by user id
            {
            "method" : "GET",
            "uri" : head + id
            },
            # GET a user's bookings
            {
            "method" : "GET",
            "uri" : head + id + '/bookings'
            },
            # POST a booking
            {
            "method" : "POST",
            "uri" : head + 'booking'
            }
        ]
    }

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
    #app.run()