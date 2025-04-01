from flask import Flask, jsonify, render_template
from flask_cors import CORS  # Import CORS
import random

app = Flask(__name__)
CORS(app)  # Allow all origins

# Initial position of the person
person_position = {"lat": 3, "lng": 3}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/location")
def get_location():
    """Simulate movement by slightly changing coordinates."""
    global person_position
    person_position["lat"] += (random.uniform(-0.001, 0.001))
    person_position["lng"] += (random.uniform(-0.001, 0.001))
    return jsonify(person_position)


if __name__ == "__main__":
    app.run(debug=True)
