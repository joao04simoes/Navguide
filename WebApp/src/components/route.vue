<template>


    <header class="app-header">
        <h1>NavGuide</h1>
    </header>
    <div class="buttons-wrapper">

        <div class="buttons">

            <button @click="handleDoubleTap" class="btList" aria-label="Voltar ao modo normal"> Editar
                Lista</button>
            <button @click="startLongPress" @mouseup="cancelLongPress" class="btEmployee"
                aria-label="Acessar modo funcionário">Chamar Funcionário</button>
        </div>
    </div>

    <div class="controller">
        <div class="status">
            <h2>🗺️ Estado da Navegação</h2>
            <p v-if="direction">➡️ <strong>Direção:</strong> {{ direction }}</p>
            <p v-if="stop">🛑 <strong>Paragem</strong></p>
        </div>

        <div class="routes">
            <div v-if="route?.length && !rRoute">
                <h3>🛒 Próxima Secção:</h3>
                <p class="next-section">
                    <template v-if="Stops.length && Stops[0] && getShoppingSection(Stops[0])">
                        {{ Stops[0][0] }} : {{ Stops[0][1] }} — <strong>{{ getShoppingSection(Stops[0]) }}</strong>
                    </template>


                </p>
                <h3>✅ Visitadas:</h3>
                <ul>
                    <li v-for="(point, index) in visitedSections" :key="index"
                        v-if="Array.isArray(point) && point.length === 2">
                        {{ point[0] }} : {{ point[1] }} — {{ getShoppingSection(point) || 'Sem nome' }}
                    </li>
                </ul>

            </div>

            <div v-else-if="rRoute">
                <h3>🛒 Rota Completa:</h3>
                <ul>
                    <li v-for="(point, index) in rRoute" :key="index">
                        {{ point[0] }} : {{ point[1] }} — {{ getShoppingSection(point) || 'Sem nome' }}
                    </li>
                </ul>
            </div>
            <div v-else>
                <p>🕐 A aguardar informação da rota...</p>
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
            coordX: 0.5,
            coordY: 9,
            rRoute: null,
            heading: 3,
            direction: null,
            shoppingList: [],
            Stops: [],
            stop: false,
            longPressTimer: null,
            visitedSections: [],
            indicedarota: -1,
        };
    },
    methods: {
        handleSingleTap() {
            this.getDirections();
        },

        handleDoubleTap() {
            this.$router.push('/modo-normal');
        },

        startLongPress() {

            this.$router.push('/funcionario');

        },

        cancelLongPress() {
            clearTimeout(this.longPressTimer);
        },

        speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'pt-PT';
            speechSynthesis.speak(utterance);
        },

        getDirections() {
            if (!this.route?.length || this.indicedarota >= this.route.length - 1) return;

            this.indicedarota++;
            const [x, y] = this.route[this.indicedarota];
            this.coordX = x;
            this.coordY = y;

            const [rx, ry] = this.Stops[0];

            if (x === rx && y === ry) {
                const reached = this.route[this.indicedarota];
                this.visitedSections.push(reached);
                this.Stops.shift(); // remove a secção atual
                this.stop = true;
                this.direction = null;
                this.$nextTick(() => {
                    this.speak(`Chegou a ${this.getShoppingSection(reached) || 'um ponto da rota'}`);
                    setTimeout(() => {
                        this.stop = false;
                    }, 5000);
                });
                // limpa direção ao parar



            } else {
                const headingTarget = NextHeading([x, y], this.route[this.indicedarota + 1]);
                const [dirText] = GiveDirection(this.heading, headingTarget, this.direction);
                this.direction = dirText; // atualiza texto visível
                this.speak(this.direction); // fala a mesma direção
                this.heading = headingTarget;
                this.stop = false;
            }
        },




        getShoppingSection(point) {
            const item = this.shoppingList.find(i => i[2] === point[0] && i[3] === point[1]);
            return item ? item[1] : null;
        },

        async GetRoute() {
            try {
                const coord = [this.coordX, this.coordY];
                const response = await axios.post('http://192.168.1.64:5000/route', coord);
                const alldata = response.data;
                this.route = alldata.route;
                this.shoppingList = alldata.shoppingList;
                this.Stops = alldata.Stops;
            } catch (error) {
                console.error(error);
            }
        },
    },

    mounted() {
        this.GetRoute();
        intervalId = setInterval(() => {
            this.getDirections();
        }, 1000);
    },

    beforeUnmount() {
        clearInterval(intervalId);
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.buttons-wrapper {
    padding: 0rem 1rem;
}


.buttons {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
    max-width: 420px;
    padding: 1 0rem;
    margin-bottom: 1.5 rem;
}

/* Estilo base dos botões */
.buttons button {
    flex: 1 1 auto;
    padding: 0.75rem 1.2rem;
    border: none;
    border-radius: 10px;
    background: linear-gradient(135deg, #2980b9, #3498db);
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

/* Efeitos de hover */
.buttons button:hover {
    background: linear-gradient(135deg, #1f5f8b, #2980b9);
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

/* Efeitos ao clicar */
.buttons button:active {
    transform: scale(0.98);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}


body {
    background-color: #ffffff;
    /* fundo branco */
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 2rem 1rem;
}


.app-header {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    padding: 1.2rem 2rem;
    color: #fff;
    font-weight: 700;
    font-size: 1rem;
    text-align: center;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.controller {
    background: #ffffff;
    padding: 1.5rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.status,
.routes {
    background: #f9f9f9;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.status h2,
.routes h3 {
    margin-bottom: 0.8rem;
    color: #2c3e50;
    font-size: 1.1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status p,
.routes li,
.routes p {
    font-size: 1rem;
    color: #333;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.routes h3 {
    color: #27ae60;
}

.next-section {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
}

.routes ul {
    padding-left: 1rem;
    list-style: none;
}

.routes li::before {
    content: "✅ ";
    margin-right: 0.3rem;
    color: #2ecc71;
}
</style>