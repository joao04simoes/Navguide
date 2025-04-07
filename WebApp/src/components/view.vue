<template>
    <div class="view">
        <button @click="GetRoute">ROUTE</button>
        <button @click="MovePerson('Y', 1)">W</button>
        <div>
            <button @click="MovePerson('X', -1)">A</button>
            <button @click="MovePerson('Y', -1)">S</button>
            <button @click="MovePerson('X', 1)">D</button>
        </div>
        {{ coordX }}:{{ coordY }}
        <div class="routes">
            <div v-if="route">
                <h2>Route:</h2>
                <ul>
                    <li v-for="(point, index) in route" :key="index">
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

        </div>
    </div>
    <div>
        <button @click="GetSections">Get sections</button>
        <div v-if="sectionsPoints">
            <h2>Sections:</h2>
            <ul>
                <li v-for="(point, index) in sectionsPoints" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            route: null,
            coordX: 0,
            coordY: 0,
            rRoute: null,
            sectionsPoints: null,
        }
    },
    methods: {
        async GetRoute() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/route')
                this.route = response.data;
            } catch (error) {
                console.error(error);
            }
        },

        async GetSections() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/sections')
                this.sectionsPoints = response.data;
            } catch (error) {
                console.error(error);
            }

        },
        MovePerson(coord, direction) {
            if (coord === 'X') {
                if (this.coordX === 0 && direction === -1)
                    return
                if (this.coordX === 10 && direction === 1)
                    return
                this.coordX += direction;
            } else if (coord === 'Y') {
                if (this.coordY === 0 && direction === -1)
                    return
                if (this.coordY === 10 && direction === 1)
                    return
                this.coordY += direction;
            }
            this.IsInRoute();
        },
        async GetLineToRoute(x, y) {

            await axios.post('http://127.0.0.1:5000/reRoute', { x, y })
                .then(response => {
                    this.rRoute = response.data
                })
                .catch(error => {
                    console.error('Error sending coordinates:', error);
                });
        },

        IsInRoute() {
            if (this.route) {
                for (let i = 0; i < this.route.length; i++) {
                    if (this.route[i][0] === this.coordX && this.route[i][1] === this.coordY) {
                        console.log("In route");
                        this.rRoute = null;
                        return;
                    }
                }
                this.GetLineToRoute(this.coordX, this.coordY)
            }

        },


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