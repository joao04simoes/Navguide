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
            <p><strong>Posição:</strong> {{ coordX }}, {{ coordY }} direção {{ heading }}</p>



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
                    <li v-for="(point, index) in visitedSections" :key="index">

                        {{ point[0] }} : {{ point[1] }} — {{ getShoppingSection(point) || 'Sem nome' }}
                    </li>
                </ul>

            </div>

            <div v-if="route?.length && rRoute">
                <h3>🛒 Rota Completa:</h3>
                <ul>
                    <li v-for="(point, index) in route" :key="index">
                        {{ point[0] }} : {{ point[1] }} — {{ getShoppingSection(point) || 'Sem nome' }}
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
let interState = null;

export default {
    data() {
        return {
            route: null,
            coordX: 0.5,
            coordY: 9,
            rRoute: null,
            heading: 1,
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

        handleOrientation(event) {
            if (event.absolute || event.webkitCompassHeading !== undefined) {
                const alpha = event.webkitCompassHeading || event.alpha;
                this.heading = 360 - alpha; // Reverse to match compass rotation

                // Normalizar dentro de 0-360
                this.heading = (this.heading + 360) % 360;

                // Determinar direção simplificada
                if ((this.heading >= 270 && this.heading < 369)) {
                    this.heading = 1; // Norte
                } else if (this.heading >= 0 && this.heading < 90) {
                    this.heading = 2; // Este
                } else if (this.heading >= 90 && this.heading < 180
                ) {
                    this.heading = 3; // Sul
                } else if (this.heading >= 180 && this.heading <= 270) {
                    this.heading = 4; // Oeste
                }
            }
        },

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
            const coordsAreClose = (x1, x2, margin = 5) =>
                Math.abs(x1 - x2) <= margin;


            const targetX = this.Stops[0][0];
            const targetY = this.Stops[0][1];

            let headingTarget;

            // Verifica se está perto na direção X (horizontal)
            if (coordsAreClose(this.coordX, targetX)) {
                if (this.coordY < targetY) {
                    headingTarget = 3; // frente
                    this.speak("seguir em frente");
                } else if (this.coordY > targetY) {
                    headingTarget = 1; // trás
                    this.speak("seguir para trás");
                }
            }
            // Verifica se está perto na direção Y (vertical)
            else if (coordsAreClose(this.coordY, targetY)) {
                if (this.coordX < targetX) {
                    headingTarget = 2; // direita
                    this.speak("virar à direita");
                } else if (this.coordX > targetX) {
                    headingTarget = 4; // esquerda
                    this.speak("virar à esquerda");
                }
            } else {
                // Se não está perto, calcula direção para próxima paragem
                const nextStop = this.Stops?.[0];
                if (!nextStop) return;

                const [nextX, nextY] = nextStop;
                headingTarget = NextHeading([this.coordX, this.coordY], [nextX, nextY]);
                const [dirText] = GiveDirection(this.heading, headingTarget, this.direction);

                if (dirText && dirText !== this.direction) {
                    this.direction = dirText;
                    this.speak(this.direction);
                }
            }



            this.stop = false;
        },

        seestate() {
            if (!this.route?.length || this.stop) return;

            this.getPosition();

            // Atualiza a rota se já passou por novos pontos
            const currentIndex = this.route.findIndex(
                ([x, y]) => x === this.coordX && y === this.coordY
            );

            if (currentIndex !== -1 && currentIndex > this.indicedarota) {
                this.indicedarota = currentIndex;
                this.route = this.route.slice(currentIndex);
                console.log('Rota atualizada a partir do ponto encontrado:', this.coordX, this.coordY);
            }

            if (!this.Stops.length || !this.route[0]) return;

            const [rx, ry] = this.Stops[0];

            // Usa comparação com tolerância para evitar erros de precisão
            const coordsAreClose = (x1, y1, x2, y2, margin = 2) =>
                Math.abs(x1 - x2) <= margin && Math.abs(y1 - y2) <= margin;

            if (coordsAreClose(this.coordX, this.coordY, rx, ry)) {
                const reached = this.Stops[0];
                this.visitedSections.push(reached);
                this.Stops.shift();
                this.stop = true;
                this.direction = null;

                // Fala chegada e aguarda 5s antes de continuar
                this.$nextTick(() => {
                    this.speak(`Chegou a ${this.getShoppingSection(reached) || 'um ponto da rota'}`);
                    setTimeout(() => {
                        this.stop = false;
                    }, 3000);
                });

                // Verifica se foi a última stop
                if (this.Stops.length === 0) {
                    setTimeout(() => {
                        this.speak('Rota completa! Obrigado por usar o NavGuide!');
                        clearInterval(intervalId);
                        clearInterval(interState);

                        // Aguarda mais 5s para deixar terminar a fala
                        setTimeout(() => {
                            this.$router.push('/modo-normal');
                        }, 5000);
                    }, 2000); // espera 6 segundos após chegada
                }
            }
        },




        getShoppingSection(point) {
            const item = this.shoppingList.find(i => i[2] === point[0] && i[3] === point[1]);
            return item ? item[1] : null;
        },

        async getPosition() {
            try {
                const response = await axios.get('http://192.168.13.137:5000/position');
                const position = response.data;
                this.coordX = position.dataX;
                this.coordY = position.dataY;
            } catch (error) {
                console.error('Erro ao obter posição:', error);
            }
        },

        async GetRoute() {
            try {
                this.getPosition();
                // Aguarda 1 segundo para garantir que a posição foi atualizada
                await new Promise(resolve => setTimeout(resolve, 1000));
                const coord = [this.coordX, this.coordY];
                const response = await axios.post('http://192.168.13.137:5000/route', coord);
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
            this.getDirections();
        }, 3000);
        interState = setInterval(() => {
            this.seestate();
        }, 500);

    },



    beforeUnmount() {
        clearInterval(intervalId);
        window.removeEventListener("deviceorientationabsolute", this.handleOrientation);
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