    <template>
        <div class="view">
            <button @click="GetRoute">ROUTE</button>
            <button @click="MovePerson('Y', 0.5)">W</button>
            <div>
                <button @click="MovePerson('X', -0.5)">A</button>
                <button @click="MovePerson('Y', -0.5)">S</button>
                <button @click="MovePerson('X', 0.5)">D</button>

            </div>
            <div>
                <button @click="changeHeading(1)">1</button>
                <button @click="changeHeading(2)">2</button>
                <button @click="changeHeading(3)">3</button>
                <button @click="changeHeading(4)">4</button>
            </div>
            {{ coordX }}:{{ coordY }}

            <p>Compass Heading: {{ heading }}°</p>

            <div class="routes">
                <div v-if="route">
                    <h2>Route:</h2>
                    <ul>
                        <li v-for="(point, index) in route" :key="index">
                            <span v-if="isShoppingPoint(point)">🛒</span>
                            {{ point[0] }}:{{ point[1] }}
                        </li>
                    </ul>
                </div>
                <div v-if="rRoute">
                    <h2>rRoute:</h2>
                    <ul>
                        <li v-for="(point, index) in rRoute" :key="index">
                            {{ point[0] }}:{{ point[1] }}
                        </li>
                    </ul>
                </div>
                <div v-else>In Route</div>

                <div>
                    <button @click="getDirections">directions</button>
                    {{ direction }}
                </div>
            </div>

        </div>

    </template>
<script>
import axios from 'axios';

import { NextHeading, GiveDirection } from '@/utils/utils';

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
        async GetLineToRoute(x, y) {

            if (this.route) {
                await axios.post('http://127.0.0.1:5000/reRoute', { x, y })
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
                        this.route.splice(i, 1);
                        this.rRoute = null;
                        return;
                    } else if (this.rRoute) {
                        for (let i = 0; i < this.rRoute.length; i++) {
                            console.log(i)
                            if (this.rRoute[i][0] === this.coordX && this.rRoute[i][1] === this.coordY) {
                                console.log("In Rroute");
                                this.rRoute.splice(i, 1);
                                if (this.rRoute.length === 0) {
                                    this.rRoute = null;
                                }
                                return;
                            }
                        }
                    }

                }
                this.GetLineToRoute(this.coordX, this.coordY)
            }

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
    },

    beforeUnmount() {
        window.removeEventListener("deviceorientationabsolute", this.handleOrientation);
    },

};
</script>

<style>
.view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #5299d6;
}

.routes {
    display: flex;
    flex-direction: row;
    align-items: top;
    justify-content: center;
    background-color: #5299d6;
}
</style>