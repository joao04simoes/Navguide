<template>
  <!-- Área sensível ao toque -->
  <div class="voice-touch-zone" @mousedown.prevent="handleMouseDown" @mouseup.prevent="handleMouseUp"
    @touchstart.prevent="handleMouseDown" @touchend.prevent="handleMouseUp">
    <p v-if="isListening">🎤 A ouvir... Fale agora.</p>


  </div>

  <div v-if="sectionsPoints" class="sections-container">
    <p class="instruction-text">
      Prima no ecrã para dizer onde quer ir. Clique para voltar para trás. Duplo clique para criar lista e começar a
      navegar.
    </p>

    <p v-if="voiceResult" class="voice-result">
      🗣️ Último comando: "{{ voiceResult }}"
    </p>

    <ul>
      <li v-for="(point, index) in sectionsPoints" :key="index">
        {{ point[1] }}
        <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
      </li>
    </ul>
  </div>


  <div v-if="shoppingList" class="shopping-list">

    <ul>
      <li v-for="(point, index) in shoppingList" :key="index">
        {{ point[1] }}: {{ point[2] }} : {{ point[3] }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sectionsPoints: null,
      shoppingListIds: [],
      shoppingList: null,
      voiceResult: '',
      recognition: null,
      clickCount: 0,
      clickTimeout: null,
      isListening: false,
    };
  },

  computed: {

  },

  methods: {
    goHome() {
      this.$router.push('/home');
    },

    goToRoute() {
      if (!this.shoppingListIds.length) {
        const mensagem = new SpeechSynthesisUtterance("A lista ainda está vazia");
        mensagem.lang = 'pt-PT';
        mensagem.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
        window.speechSynthesis.speak(mensagem);
        return;
      }

      this.$router.push('/route');
    },


    handleMouseDown() {
      this.touchStartTime = new Date().getTime();
      this.touchTimer = setTimeout(() => {
        this.startTouchVoice();
        this.touchTimer = null;
      }, 500);
    },

    handleMouseUp() {
      const elapsed = new Date().getTime() - this.touchStartTime;

      if (this.touchTimer) {
        clearTimeout(this.touchTimer);
        this.touchTimer = null;

        this.clickCount++;
        if (this.clickTimeout) clearTimeout(this.clickTimeout);

        this.clickTimeout = setTimeout(() => {
          if (this.clickCount === 1) {
            this.goHome();
          } else if (this.clickCount === 2) {
            this.makeShoppingList();
            this.goToRoute();
          }
          this.clickCount = 0;
        }, 300);
      } else {
        this.stopTouchVoice();
      }
    },

    startTouchVoice() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert('Reconhecimento de voz não suportado.');
        return;
      }

      if (this.recognition) this.recognition.abort();

      this.recognition = new SpeechRecognition();
      this.recognition.lang = 'pt-PT';
      this.recognition.interimResults = false;

      this.recognition.onstart = () => {
        this.isListening = true;
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.trim();
        this.voiceResult = transcript;
        this.selectItemByVoice(transcript);
      };

      this.recognition.onerror = (event) => {
        console.error('Erro no reconhecimento de voz:', event.error);
      };

      this.recognition.onend = () => {
        this.isListening = false;
      };

      this.recognition.start();
    },

    stopTouchVoice() {
      if (this.recognition) {
        this.recognition.stop();
      }
      this.isListening = false;
    },

    selectItemByVoice(transcript) {
      if (!this.sectionsPoints) return;

      const normalized = transcript.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, '').trim();
      const isRemoveCommand = normalized.startsWith("remover ") || normalized.startsWith("tirar ") || normalized.startsWith("retirar ") || normalized.startsWith("apagar ");
      const rawItems = normalized.replace(/^remover |^tirar |^retirar |^apagar/, '').split(/,| e /).map(s => s.trim()).filter(Boolean);

      const results = [];

      rawItems.forEach(item => {
        const match = this.sectionsPoints.find(point => {
          const name = point[1].toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, '').trim();
          return (
            name === item ||
            name.includes(item) ||
            item.includes(name) ||
            name.startsWith(item.slice(0, -1)) ||
            item.startsWith(name.slice(0, -1))
          );
        });

        if (match) {
          const alreadySelected = this.shoppingListIds.includes(match[0]);

          if (isRemoveCommand && alreadySelected) {
            this.shoppingListIds = this.shoppingListIds.filter(id => id !== match[0]);
            results.push(`Removido: ${match[1]}`);
          } else if (!isRemoveCommand && !alreadySelected) {
            this.shoppingListIds.push(match[0]);
            results.push(`Adicionado: ${match[1]}`);
          }
        } else if (item !== "") {
          results.push(`Não encontrado: ${item}`);
        }
      });

      if (results.length > 0) {
        const mensagem = new SpeechSynthesisUtterance(results.join('. '));
        mensagem.lang = 'pt-PT';
        mensagem.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
        window.speechSynthesis.speak(mensagem);
        this.voiceResult = results.join('. ');
      }
    },

    async postList() {
      try {
        await axios.post('http://192.168.1.64:5000/list', this.shoppingList);
      } catch (error) {
        console.error(error);
      }
    },

    async GetSections() {
      try {
        const response = await axios.get('http://192.168.1.64:5000/sections');
        this.sectionsPoints = response.data;
      } catch (error) {
        console.error(error);
      }
    },

    makeShoppingList() {
      const rawIds = [...this.shoppingListIds];

      if (!rawIds.length) {
        // opcional: feedback de voz
        const mensagem = new SpeechSynthesisUtterance("A lista está vazia. Selecione itens primeiro.");
        mensagem.lang = 'pt-PT';
        mensagem.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
        window.speechSynthesis.speak(mensagem);
        return;
      }

      this.shoppingList = this.sectionsPoints.filter(point => rawIds.includes(point[0]));
      this.postList();
      sessionStorage.setItem('savedShoppingListIds', JSON.stringify(this.shoppingListIds));
    }

  },

  mounted() {
    speechSynthesis.cancel();

    this.GetSections();
    const savedIds = sessionStorage.getItem('savedShoppingListIds');
    if (savedIds) {
      this.shoppingListIds = JSON.parse(savedIds);
    }

    const instrucoes = "Prima no ecrã para dizer onde quer ir. Clique para voltar para trás. Duplo clique para criar lista e começar a navegar.";
    const mensagem = new SpeechSynthesisUtterance(instrucoes);
    mensagem.lang = 'pt-PT';
    mensagem.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
    window.speechSynthesis.speak(mensagem);

    localStorage.setItem('ultimaPagina', 'list');
  },




};
</script>

<style scoped>
.sections-container,
.shopping-list {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  margin: 1rem auto;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

input[type="text"] {
  padding: 0.5rem;
  width: 100%;
  margin-bottom: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

ul {
  padding: 0;
  list-style: none;
}

li {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0;
  border-bottom: 1px solid #eee;
}

button {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

button:hover {
  background-color: #2ecc71;
}

.voice-touch-zone {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  background-color: transparent;
}

.voice-touch-zone:active {
  background-color: #e0ffe0;
  transition: background-color 0.3s;
}

.voice-result {
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.instruction-text {
  font-weight: bold;
}
</style>
