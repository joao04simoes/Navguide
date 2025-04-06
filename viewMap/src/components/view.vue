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
        MovePerson(coord, direction) {
            if (coord === 'X') {
                this.coordX += direction;
            } else if (coord === 'Y') {
                this.coordY += direction;
            }
            this.IsInRoute();
        },

        IsInRoute() {
            if (this.route) {
                for (let i = 0; i < this.route.length; i++) {
                    if (this.route[i][0] === this.coordX && this.route[i][1] === this.coordY) {
                        console.log("In route");
                    }
                }
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
</style>