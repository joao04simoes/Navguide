from dataBase import getSectionsFromDataBase
from map import initRoute, FindReRoute, InitMap
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # Import CORS
import random
import re
import time
import threading
from threading import Lock

distances_lock = Lock()


app = Flask(__name__)
CORS(app)  # Allow all origins

walkingPoints = []
route = []
sectionsLines = {}
sectionsPoints = []
shoppingList = []


# Dicionário para guardar as distâncias por mac_address
distances = {
    '0x0001': [],
    '0x0002': []
}

# Dicionário para guardar as médias por segundo
current_average = {
    '0x0001': None,
    '0x0002': None
}

# Função para calcular a média por segundo
message_buffer = ""


def average_worker():

    while True:
        time.sleep(1)
        # print("Calculando médias...")
        with distances_lock:
            # print("distances")
            for mac in distances:
                # print("mac")
                values = distances[mac]
                print(values)
                if values:
                    media = sum(values) / len(values)
                    current_average[mac] = media
                    print(f"Média de {mac}: {media:.2f} cm")
                    distances[mac].clear()


# Iniciar a thread de média
threading.Thread(target=average_worker, daemon=True).start()


def run_on_start():
    global sectionsLines
    sectionsLines = InitMap()


@app.route("/map")
def index():
    return jsonify(map)


@app.route("/receive_distance", methods=['POST'])
@app.route("/receive_distance", methods=['POST'])
def receiveDistance():
    global message_buffer

    # Receber fragmento da mensagem
    fragment = request.form.get('raw_message')
    if not fragment:
        return "No raw_message", 400

    # print("Fragmento recebido:", fragment)
    message_buffer += fragment

    # Tenta extrair mensagens completas do buffer
    matches = re.findall(
        r'\[mac_address=(0x[0-9a-fA-F]+), status="SUCCESS", distance\[cm\]=(\d+)\]',
        message_buffer
    )

    with distances_lock:
        for mac, dist_str in matches:
            dist = int(dist_str)
            if mac not in distances:
                distances[mac] = []
            distances[mac].append(dist)
            # print(f"→ Distância registada para {mac}: {dist} cm")

    # Limpa as partes já processadas do buffer
    message_buffer = re.sub(
        r'\[mac_address=(0x[0-9a-fA-F]+), status="SUCCESS", distance\[cm\]=(\d+)\]',
        '',
        message_buffer
    )

    return "Fragmento processado", 200


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
    app.run(host='0.0.0.0', port=5000, debug=True)
