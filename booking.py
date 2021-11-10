from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

#PORT = 3200
#HOST = '192.168.0.15'

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
    req = request.get_json()

    # if the booking is already present
    for book in booking:
        if str(book["userid"]) == str(userid): # user exists

            if book["dates"].count(req) == 1: # if booking already exists
                return make_response(jsonify({"error":"booking already exists"},discoverability(book)),409)
            
            book["dates"].append(req) # else : add booking
            return make_response(jsonify(book, discoverability(book)),200)

    return make_response(jsonify({'error' : 'User ID not found'}),400)
    
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
            {
                "method" : "POST",
                "uri" : head + id 
            }
        ]
    }  

if __name__ == "__main__":
    #print("Server running in port %s"%(PORT))
    #app.run(host=HOST, port=PORT)
    app.run()
    
  
   