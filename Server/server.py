from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Import CORS
import random


from map import initRoute, FindReRoute, InitMap
from dataBase import getSectionsFromDataBase


app = Flask(__name__)
CORS(app)  # Allow all origins

walkingPoints = []
route = []
sectionsLines = {}
sectionsPoints = {}


def run_on_start():
    global sectionsLines
    sectionsLines = InitMap()


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/route")
def getRoute():
    global route, walkingPoints
    route, walkingPoints = initRoute(sectionsLines)
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


@app.route("/sections", methods=['GET'])
def getSectionsPoints():
    global sectionsPoints
    sectionsPoints = getSectionsFromDataBase()
    return jsonify(sectionsPoints)


if __name__ == "__main__":
    run_on_start()
    app.run(debug=True)
