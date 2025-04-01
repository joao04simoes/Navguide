from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Import CORS
import random

from route import shortest_path

app = Flask(__name__)
CORS(app)  # Allow all origins

# Initial position of the person
person_position = {"lat": 2.2, "lng": 1.4}

map = {
    "bounds": [[0, 0], [10, 0], [10, 10], [0, 10]],
    "stations": [
        {"name": "Entrada", "coords": [1, 1]},
        {"name": "Saída", "coords": [9, 1]},
        {"name": "Caixa 1", "coords": [8, 2]},
        {"name": "Caixa 2", "coords": [8, 3]},
        {"name": "Padaria", "coords": [2, 8]},
        {"name": "Frutas e Legumes", "coords": [3, 8]},
        {"name": "Carnes", "coords": [5, 8]},
        {"name": "Peixaria", "coords": [7, 8]},
        {"name": "Laticínios", "coords": [6, 6]},
        {"name": "Bebidas", "coords": [8, 6]},
        {"name": "Bedas", "coords": [3, 6]},

    ],
    "aisles": [
        {"name": "Corredor 1", "start": [2, 7], "end": [8, 7]},
        {"name": "Corredor 2", "start": [2, 5], "end": [8, 5]},
        {"name": "Corredor 3", "start": [2, 3], "end": [8, 3]}
    ],
    "shelves": [
        {"id": "P1", "coords": [2, 6]},
        {"id": "P2", "coords": [4, 6]},
        {"id": "P3", "coords": [6, 6]},
        {"id": "P4", "coords": [2, 4]},
        {"id": "P5", "coords": [4, 4]},
        {"id": "P6", "coords": [6, 4]}
    ]
}


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/route")
def getRoute():
    path, dist = shortest_path(map)
    print("Melhor caminho:", path)
    print("Distância mínima:", dist)
    return jsonify(path)


@app.route("/stop")
def addStop():
    print("adding stop")


@app.route("/location")
def get_location():
    """Simulate movement by slightly changing coordinates."""
    person_position["lat"] += (random.uniform(-0.001, 0.001))
    person_position["lng"] += (random.uniform(-0.001, 0.001))
    return jsonify(person_position)

    # buscar a localização do uwb


if __name__ == "__main__":
    app.run(debug=True)
