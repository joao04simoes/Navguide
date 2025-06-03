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
sectionsPoints = []
shoppingList = []


def run_on_start():
    global sectionsLines
    sectionsLines = InitMap()


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/route", methods=['POST'])
def getRoute():
    try:
        global route, walkingPoints
        coord = request.get_json()
        print("Received Coordinates:", coord)
        route, walkingPoints, stops = initRoute(
            sectionsLines, shoppingList, coord)
        return jsonify({"route": route, "shoppingList": shoppingList, "Stops": stops})
    except Exception as e:
        print("Error in /route:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/reRoute", methods=['POST'])
def ReRoute():
    global route, walkingPoints
    try:
        PositionJson = request.get_json()
        print("Received Position:", PositionJson)  # Debug
        Position = (PositionJson["x"], PositionJson["y"])
        if "Ns" in PositionJson:
            NextStop = PositionJson["Ns"]
        else:
            NextStop = route[-1]
        print("Next Stop:", NextStop)  # Debug
        print("Current Position:", Position)  # Debug
        print("Walking Points:", walkingPoints)  # Debug
        Rroute = FindReRoute(NextStop, Position, walkingPoints)
        return jsonify(Rroute)
    except Exception as e:
        print("Error in /reRoute:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/sections", methods=['GET'])
def getSectionsPoints():
    global sectionsPoints
    sectionsPoints = getSectionsFromDataBase()
    return jsonify(sectionsPoints)


@app.route("/list", methods=['POST'])
def SaveShoppingList():
    global shoppingList
    try:
        shoppingList = request.get_json()
        print("Received Shopping List:", shoppingList)  # Debug
        return jsonify({"message": "Shopping list saved successfully!"})
    except Exception as e:
        print("Error in /list:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    run_on_start()
    app.run(host= '0.0.0.0', port=5000 ,debug=True)
