import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

import grpc
import booking_pb2
import booking_pb2_grpc
import movie_pb2
import movie_pb2_grpc


app = Flask(__name__)

PORT = 3004 # not to be confused with others' port
HOST = '127.0.0.1' # localhost

PORT_BOOKING = '3003'
HOST_BOOKING = HOST

PORT_MOVIE = '3001'
HOST_MOVIE = HOST

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>",200)

# get the full JSON database
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
    json = []
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        allmovies = stub.GetListMovies(movie_pb2.Empty())

        for movie in allmovies:
            json.append({'title' : movie.title, 'rating' : movie.rating, 'director' : movie.director, 'id' : movie.id})
    return make_response(jsonify(json), 200)

# get a user's bookings
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_bookings(userid):
    json = []
    user = booking_pb2.UserID(id = userid)
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        bookings = stub.GetUsersBook(user) # Book array
        for book in bookings:
            json.append({'userid' : book.userid, 'dates' : [{'date' : book.date.date, 'movies' : book.date.scheduled_movies}] })
    return make_response(jsonify(json), 200)


# get the movies scheduled on a given date
@app.route("/users/movies/<date>", methods=['GET'])
def get_moviesByDate(date):

    user = booking_pb2.BookingDate(date = date)
    
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        movies = stub.GetMoviesByDate(date)
        json = {'Date' : movies.date, 'movies' : movies.scheduled_movies}

        return make_response(jsonify(json), 200)


# add a new user
@app.route("/users/<userid>", methods=["POST"])
def create_user(userid):
    req = request.get_json()

    # check the integrity of the request
    if userid != req["id"]:
        return make_response(jsonify({'error' : 'URL argument and body does not match proprely'}), 409)

    # check if the user already exists in the database
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error":"user ID already exists"},discoverability(user)),409)

    users.append(req)
    return make_response(jsonify({"message":"user added"},200))

# add a booking to a user
@app.route("/users/<userid>/bookings", methods=['POST'])
def add_booking(userid):
    req = request.get_json()
    
    date_book = booking_pb2.BookingDateAndMovieID(date=req['date'],scheduled_movies=req['movies'] )
    book = booking_pb2.Book(userid= userid, date=date_book)

    user = booking_pb2.BookingUserID(user = userid)
    
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        movies = stub.AddBook(book)
        json = {'Date' : movies.date, 'movies' : movies.scheduled_movies}

        return make_response(jsonify(json), 200)



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
            "uri" : head + id + '/bookings'
            },
            # GET the movies scheduled on a given date
            {
            "method" : "GET",
            "uri" : head + 'movies/<date>'
            }
        ]
    }

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
    #app.run()