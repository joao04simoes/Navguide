from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Import CORS
import random


from map import initRoute, FindReRoute


app = Flask(__name__)
CORS(app)  # Allow all origins

walkingPoints = []
route = []


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/route")
def getRoute():
    global route, walkingPoints
    route, walkingPoints = initRoute()
    return jsonify(route)


@app.route("/reRoute", methods=['POST'])
def ReRoute():
    global route, walkingPoints
    try:
        PositionJson = request.get_json()
        print("Received Position:", PositionJson)  # Debug
        Position = (PositionJson["x"], PositionJson["y"])
        Rroute = FindReRoute(route, Position, walkingPoints)
        return jsonify(Rroute)
    except Exception as e:
        print("Error in /reRoute:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
