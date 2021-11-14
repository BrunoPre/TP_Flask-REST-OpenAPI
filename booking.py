import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

#PORT = 3200
#HOST = '192.168.0.15'

PORT = 3201 # not to be confused with showtime's
HOST = '127.0.0.1' # localhost

# Showtime service's port and host
PORT_SHOWTIME = '3200'
HOST_SHOWTIME = HOST

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   booking = json.load(jsf)["bookings"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>",200)

# get the complete json file
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(booking), 200)
    return res

# get bookings from a user ID
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_byuser(userid):
    for book in booking:
        if str(book["userid"]) == str(userid):
            res = make_response(jsonify(book, discoverability(book)),200) # both booking and discoverability are JSONified
            return res
    return make_response(jsonify({"error": "User ID not found"}),400)
   
# add a booking for a user
@app.route("/bookings/<userid>", methods=["POST"])
def add_booking_byuser(userid):
    timetable = requests.get('http://' + HOST_SHOWTIME + ':' + PORT_SHOWTIME + '/showtimes')
    timetable = timetable.json() # convert the Response object to JSON

    req = request.get_json() # 2 fields : date & movies (array)
    
    # see if date & scheduled movie exists
    for time in timetable: # contains dicts with 2 fields : date & movies (array)
        
        # if right date was found
        if time["date"] == req["date"]:

            # check if all requested movies are scheduled
            check_avail_movies = all(movie in time["movies"] for movie in req["movies"])

            if check_avail_movies:
                for book in booking: # come across all the bookings

                    if str(book["userid"]) == str(userid): # user exists
                        for date in book["dates"]:

                            if date["date"] == req["date"]: # if there's already a booking at the same date
                                date["movies"].extend(req["movies"])
                                return make_response(jsonify(book, discoverability(book)),200)
                        # if there is no booking at the request date, then the full request is added
                        book["dates"].append(req)
                        return make_response(jsonify(book, discoverability(book)),200)

                # user ID does not exist --> add the full request
                new_user_booking = {
                    "userid" : userid,
                    "dates" : [req]
                }
                booking.append(new_user_booking)
                return make_response(jsonify(new_user_booking, discoverability(new_user_booking)),200)

            # if all requested movies are not scheduled
            return make_response(jsonify({'error' : 'The requested movies are not available at this date'}),400)

    # date was not found
    return make_response(jsonify({'error' : 'No schedule found at this date'}),400)                

@app.route("/bookings/showtimes/<date>", methods=["GET"])
def get_MovieByDate(date):
    movies = requests.get('http://' + HOST_SHOWTIME + ':' + PORT_SHOWTIME + '/showmovies/' + date)
    res = movies.json()
    return make_response(jsonify(res), movies.status_code)

# discoverability function to be RESTful, given a booking
def discoverability(book):
    
    head = "/bookings/"
    id = book["userid"]

    return {
        "possible_requests": [
            # GET by user id
            {
                "method" : "GET",
                "uri" : head + id
            },
            # POST by user id
            {
                "method" : "POST",
                "uri" : head + id 
            }
        ]
    }  

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
    #app.run()
    
  
   