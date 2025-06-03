<template>

    <div @touchstart="startTouch" @touchend="endTouch">
    <!-- resto do conteúdo -->
    </div>
    <button @click="startVoiceRecognition">Selecionar por voz</button>
    <p v-if="voiceResult">Último comando: "{{ voiceResult }}"</p>
    <div>
        <button @click="GetSections">Getsections</button>
        <button @click="makeShoppingList">make list</button>
        <div v-if="sectionsPoints">
            <h2>Sections:</h2>

            <input type="text" v-model="searchQuery" placeholder="Search..." />
            <ul>
                <li v-for="(point, index) in filteredSections" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                    <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
                </li>
            </ul>
            <h2>ALL sections:</h2>

            <ul>
                <li v-for="(point, index) in sectionsPoints" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                    <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
                </li>
            </ul>

        </div>
        <div v-if="shoppingList">
            <router-link to="/route">
                <button>Iniciar a navegação</button>
            </router-link>
            <ul>
                <li v-for="(point, index) in shoppingList" :key="index">
                    {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
                </li>
            </ul>

        </div>
    </div>
</template>


<script>
import axios from 'axios';
import { useRoute } from 'vue-router'


export default {
    data() {
        return {
            startX: 0,
            sectionsPoints: null,
            shoppingListIds: [],
            shoppingList: null,
            searchQuery: '',
            voiceResult: '',
            recognition: null,

        }
    },

    computed: {
        filteredSections() {
            if (!this.searchQuery) {
                return ""
            }
            return this.sectionsPoints.filter(point =>
                point[1].toLowerCase().includes(this.searchQuery.toLowerCase()))
        }

    },

    methods: {

        startVoiceRecognition() {
            // Verifica se o navegador suporta a Web Speech API
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert('Reconhecimento de voz não suportado neste navegador.');
                return;
            }

            this.recognition = new SpeechRecognition();
            this.recognition.lang = 'pt-PT'; // ou 'en-US', conforme sua aplicação
            this.recognition.interimResults = false;
            this.recognition.maxAlternatives = 1;

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript.trim();
                this.voiceResult = transcript;
                this.selectItemByVoice(transcript);
            };

            this.recognition.onerror = (event) => {
                console.error('Erro no reconhecimento de voz:', event.error);
            };

            this.recognition.start();
        },

        selectItemByVoice(transcript) {
            if (!this.sectionsPoints) return;

            const match = this.sectionsPoints.find(point => {
                const name = point[1].toLowerCase();
                return name.includes(transcript.toLowerCase());
            });

            if (match && !this.shoppingListIds.includes(match[0])) {
                this.shoppingListIds.push(match[0]);
            // ✅ Fala feedback ao utilizador
            const mensagem = new SpeechSynthesisUtterance(`Adicionado: ${match[1]}`);
            mensagem.lang = 'pt-PT';
            const vozes = window.speechSynthesis.getVoices();
            const vozPT = vozes.find(v => v.lang === 'pt-PT') || vozes[0];
            mensagem.voice = vozPT;
            window.speechSynthesis.speak(mensagem);

            } else {
            // ✅ Feedback se nada for encontrado
            const mensagem = new SpeechSynthesisUtterance(`Item não encontrado`);
            mensagem.lang = 'pt-PT';
            window.speechSynthesis.speak(mensagem);

            }
        },

        
        async postList() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/list', this.shoppingList)
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

        startTouch(event) {
            this.startX = event.changedTouches[0].screenX
        },
        endTouch(event) {
            const endX = event.changedTouches[0].screenX
            const diffX = this.startX - endX

            if (diffX < -50) {
                this.$router.push('/home')
            }
        },


        makeShoppingList() {
            const rawIds = [...this.shoppingListIds];
            this.shoppingList = this.sectionsPoints.filter(point => rawIds.includes(point[0]));
            this.postList();
            this.sectionsPoints = null;

        }
    },

    mounted() {
        this.GetSections();
    }
}
</script>

<style scoped>
div {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 600px;
    margin: auto;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-top: 1rem;
    color: #2c3e50;
}

ul {
    padding: 0;
    list-style-type: none;
}

li {
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.3rem 0;
    border-bottom: 1px solid #eee;
    color: #333;
}

button {
    margin-top: 1rem;
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

button:hover {
    background-color: #2ecc71;
}
</style>
