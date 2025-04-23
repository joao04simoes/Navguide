    <template>
        <div class="controller">
            <div class="actions">
                <button @click="GetRoute">🧭 Route</button>
                <div class="movement-grid">
                    <div class="arrow-up"><button @click="MovePerson('Y', 0.5)">⬆️</button></div>
                    <div class="arrow-left"><button @click="MovePerson('X', -0.5)">⬅️</button></div>
                    <div class="arrow-down"><button @click="MovePerson('Y', -0.5)">⬇️</button></div>
                    <div class="arrow-right"><button @click="MovePerson('X', 0.5)">➡️</button></div>
                </div>
                <div class="heading">
                    <span>Heading:</span>
                    <button @click="changeHeading(1)">1</button>
                    <button @click="changeHeading(2)">2</button>
                    <button @click="changeHeading(3)">3</button>
                    <button @click="changeHeading(4)">4</button>
                </div>
            </div>

            <div class="status">
                <p>📍 Position: {{ coordX }} : {{ coordY }}</p>
                <p>🧭 Compass Heading: {{ heading }}°</p>
                <button @click="getDirections">🧭 Get Directions</button>
                <p v-if="direction">➡️ {{ direction }}</p>
            </div>

            <div class="routes">
                <div v-if="route?.length">
                    <h3>📌 Route:</h3>
                    <ul>
                        <li v-for="(point, index) in route" :key="index">
                            <span v-if="isShoppingPoint(point)">🛒</span> {{ point[0] }} : {{ point[1] }}
                        </li>
                    </ul>
                </div>
                <div v-else>
                    <p>🕐 Awaiting route info...</p>
                </div>
                <div v-if="rRoute?.length">
                    <h3>🔄 Re-Route:</h3>
                    <ul>
                        <li v-for="(point, index) in rRoute" :key="index">
                            {{ point[0] }} : {{ point[1] }}
                        </li>
                    </ul>
                </div>

            </div>
        </div>


    </template>
<script>
import axios from 'axios';

import { NextHeading, GiveDirection } from '@/utils/utils';
let intervalId = null;

export default {
    data() {
        return {
            route: null,
            coordX: 5,
            coordY: 9.5,
            rRoute: null,
            sectionsPoints: null,
            heading: 0,
            direction: null,
            shoppingList: [],
            Stops: [],

        }
    },
    methods: {
        async GetRoute() {
            try {
                const coord = [this.coordX, this.coordY];
                const response = await axios.post('http://127.0.0.1:5000/route', coord)
                const alldata = response.data;
                this.route = alldata.route;
                this.shoppingList = alldata.shoppingList
                this.Stops = alldata.Stops

            } catch (error) {

                console.error(error);
            }
        },


        getDirections() {
            let NextHeadingValue;
            if (this.rRoute) {
                NextHeadingValue = NextHeading([this.coordX, this.coordY], this.rRoute[1]);
            } else {
                NextHeadingValue = NextHeading([this.coordX, this.coordY], this.route[0]);
            }
            console.log(NextHeadingValue);
            this.direction = GiveDirection(this.heading, NextHeadingValue);
        },


        MovePerson(coord, direction) {
            if (coord === 'X') {
                if (this.coordX === 0 && direction === -0.5)
                    return
                if (this.coordX === 10 && direction === 0.5)
                    return
                this.coordX += direction;
            } else if (coord === 'Y') {
                if (this.coordY === 0 && direction === -0.5)
                    return
                if (this.coordY === 10 && direction === 0.5)
                    return
                this.coordY += direction;
            }
            this.IsInRoute();
        },
        changeHeading(x) {
            this.heading = x;
        },
        async GetLineToRoute(x, y, Ns) {

            if (this.route) {
                await axios.post('http://127.0.0.1:5000/reRoute', { x, y, Ns })
                    .then(response => {
                        this.rRoute = response.data
                    })
                    .catch(error => {
                        console.error('Error sending coordinates:', error);
                    });
            }
        },

        IsInRoute() {
            if (this.route) {
                for (let i = 0; i < this.route.length; i++) {
                    if (this.route[i][0] === this.coordX && this.route[i][1] === this.coordY) {
                        console.log("In route");
                        this.route = this.route.slice(i);
                        this.rRoute = null;
                        return { success: true, index: i };
                    } else if (this.rRoute) {
                        for (let i = 0; i < this.rRoute.length; i++) {
                            console.log(i)
                            if (this.rRoute[i][0] === this.coordX && this.rRoute[i][1] === this.coordY) {
                                console.log("In Rroute");
                                this.rRoute.splice(i, 1);
                                if (this.rRoute.length === 0) {
                                    this.rRoute = null;
                                }
                                return { success: true, index: i };
                            }
                        }
                    }

                }
                this.GetLineToRoute(this.coordX, this.coordY, this.Stops[0])
            }


        },
        IstheStop() {
            if (this.Stops.length === 0) {
                return false;
            }
            if (this.Stops[0][0] === this.coordX && this.Stops[0][1] === this.coordY) {
                return true;
            }

            return false;
        },


        isShoppingPoint(point) {
            return this.shoppingList.some(item => item[2] === point[0] && item[3] === point[1]);
        },


        handleOrientation(event) {
            if (event.absolute || event.webkitCompassHeading !== undefined) {
                const alpha = event.webkitCompassHeading || event.alpha;
                this.heading = 360 - alpha; // Reverse to match compass rotation
                this.heading = Math.round(this.heading);
                if (this.heading > 315 || this.heading < 45) {
                    this.heading = 1;
                } else if (this.heading >= 45 && this.heading < 135) {
                    this.heading = 2;
                } else if (this.heading >= 135 && this.heading < 225) {
                    this.heading = 3;
                } else if (this.heading >= 225 && this.heading < 315) {
                    this.heading = 4;
                }

            }
        },

        MainFunc() {
            const result = this.IsInRoute()
            if (result && result.success) {
                if (this.IstheStop()) {
                    this.Stops.splice(0, 1);
                    this.route = this.route.slice(result.index);
                }
            }
        }



    },
    mounted() {
        // iOS requires user interaction before allowing access
        if (
            typeof DeviceOrientationEvent !== "undefined" &&
            typeof DeviceOrientationEvent.requestPermission === "function"
        ) {
            DeviceOrientationEvent.requestPermission()
                .then((response) => {
                    if (response === "granted") {
                        window.addEventListener("deviceorientationabsolute", this.handleOrientation, true);
                    }
                })
                .catch(console.error);
        } else {
            // For Android or older devices
            window.addEventListener("deviceorientationabsolute", this.handleOrientation, true);
        }
        this.GetRoute();
        intervalId = setInterval(() => {
            this.MainFunc()
        }, 1000)

    },

    beforeUnmount() {
        window.removeEventListener("deviceorientationabsolute", this.handleOrientation);
    },

};
</script>

<style>
.controller {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 600px;
    margin: auto;
    font-family: 'Segoe UI', sans-serif;
}

.actions {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
}

.movement-grid {
    display: grid;
    grid-template-columns: repeat(3, 60px);
    grid-template-rows: repeat(3, 60px);
    gap: 0.5rem;
    justify-content: center;
    align-items: center;
}

.arrow-up {
    grid-column: 2;
    grid-row: 1;
}

.arrow-left {
    grid-column: 1;
    grid-row: 2;
}

.arrow-down {
    grid-column: 2;
    grid-row: 2;
}

.arrow-right {
    grid-column: 3;
    grid-row: 2;
}


.heading {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    font-size: 1rem;
}

.heading span {
    font-weight: bold;
    margin-right: 0.5rem;
    color: #333;
}

button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #2980b9;
}

.routes,
.status {
    background: #f9f9f9;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    width: 100%;
    margin-top: 1rem;
    border: 1px solid #ddd;
    color: #333;
}

.routes h3,
.status p {
    margin: 0.5rem 0;
    color: #333;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

li {
    padding: 0.4rem 0;
    border-bottom: 1px solid #eee;
    font-size: 0.95rem;
}
</style>