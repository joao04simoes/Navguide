from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Import CORS
import random


from map import initRoute

app = Flask(__name__)
CORS(app)  # Allow all origins

# Initial position of the person
person_position = {"lat": 2.2, "lng": 1.4}


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/route")
def getRoute():
    route = initRoute()
    return jsonify(route)


if __name__ == "__main__":
    app.run(debug=True)
