from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)
with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>",200)

# get a user info by its ID
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["userid"]) == str(userid):
            res = make_response(jsonify(user, discoverability(user)),200) # both user and discoverability are JSONified
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)
    
# add a new user
@app.route("/users/<userid>", methods=["POST"])
def create_user(userid):
    req = request.get_json()

    for user in users:
        if str(user["userid"]) == str(userid):
            return make_response(jsonify({"error":"user ID already exists"},discoverability(user)),409)

    users.append(req)
    res = make_response(jsonify({"message":"user added"}),200)
    return res


# discoverability function to be RESTful, given a user
def discoverability(user):

    head = "/users/"
    id = user["id"]
    title = user["title"]

    return {
        "possible_requests": [
            # GET by user id
            {
            "method" : "GET",
            "uri" : head + id
            },
            # GET by user title
            {
            "method" : "GET",
            "uri" : "/usersbytitle?title=" + title
            },
            # DELETE by user id
            {
            "method" : "DELETE",
            "uri" : head + id
            },
            # PUT the user rate
            {
            "method" : "PUT",
            "uri" : head + id + "/<rate>"
            }
        ]
    }

if __name__ == "__main__":
    #print("Server running in port %s"%(PORT))
    #app.run(host=HOST, port=PORT)
    app.run()