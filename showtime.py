from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# previous parameters
#PORT = 3200
#HOST = '192.168.0.15'

PORT = 3200 # not to be confused with booking's
HOST = '127.0.0.1' # localhost

with open('{}/databases/times.json'.format("."), "r") as jsf:
   times = json.load(jsf)["schedule"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Showtime service!</h1>",200)

# get the full JSON database
@app.route("/showtimes", methods=['GET'])
def get_json():
    res = make_response(jsonify(times), 200)
    return res


# get the schedule by date
@app.route("/showmovies/<date>", methods=['GET'])
def get_schedule_by_date(date):
    for time in times:
        if str(time["date"]) == str(date):
            res = make_response(jsonify(time),200)
            return res
    return make_response(jsonify({"error":"Schedule not found for the given date"}),400)


if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
    #app.run()
    
  
   