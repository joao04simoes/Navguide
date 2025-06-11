<template>
  <div
    @click="handleClick"
    @touchstart.prevent
    @touchmove.prevent
  ></div>

  <!-- Botão explícito para voltar -->
  <button @click="goHome">Voltar</button>

  <div>
    <button @click.stop="startVoiceRecognition">Selecionar por voz</button>
    <p v-if="voiceResult">Último comando: "{{ voiceResult }}"</p>

    <div>
      <button @click.stop="GetSections">Getsections</button>
      <button @click.stop="makeShoppingList">make list</button>

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
        <button @click.stop="goToRoute">Iniciar a navegação</button>
        <ul>
          <li v-for="(point, index) in shoppingList" :key="index">
            {{ point[1] }}:{{ point[2] }} : {{ point[3] }}
          </li>
        </ul>
      </div>
    </div>
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
      searchQuery: '',
      voiceResult: '',
      recognition: null,
      clickCount: 0,
      clickTimeout: null,
    }
  },

  computed: {
    filteredSections() {
      if (!this.searchQuery) return "";
      return this.sectionsPoints.filter(point =>
        point[1].toLowerCase().includes(this.searchQuery.toLowerCase()));
    }
  },

  methods: {
    goHome() {
      this.$router.push('/home');
    },

    goToRoute() {
      this.$router.push('/route');
    },

/*
    awaitNavigationClick() {
      let clicks = 0;
      const handler = () => {
        clicks++;
        if (clicks === 1) {
          this.clickTimeout = setTimeout(() => {
            if (clicks === 1) {
              // Apenas um clique → ignora ou faz algo leve
              this.voiceResult = "Clique único ignorado. Use duplo clique para navegar.";
            } else if (clicks === 2) {
              // Duplo clique → navega corretamente
              this.$router.push('/route');
            }
            document.removeEventListener('click', handler);
          }, 300);
        }
      };
      document.addEventListener('click', handler);
    },
*/
    startVoiceRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert('Reconhecimento de voz não suportado neste navegador.');
        return;
      }

      this.recognition = new SpeechRecognition();
      this.recognition.lang = 'pt-PT';
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

      const normalized = transcript.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, '').trim();

      // Verifica se o comando é para criar a lista
      const isCreateListCommand = normalized.includes("criar lista") || normalized.includes("fazer lista");

      if (isCreateListCommand) {
                if (this.shoppingListIds.length > 0) {
                this.makeShoppingList();
                this.voiceResult = "Lista criada com os produtos selecionados. duplo clique para começar navegação. um clique para voltar atras.";
                const confirmacao = new SpeechSynthesisUtterance(this.voiceResult);
                confirmacao.lang = 'pt-PT';
                confirmacao.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
                window.speechSynthesis.speak(confirmacao);

                this.awaitNavigationClick();


              } else {
                this.voiceResult = "Nenhum produto selecionado para criar a lista.";
                const aviso = new SpeechSynthesisUtterance(this.voiceResult);
                aviso.lang = 'pt-PT';
                aviso.voice = window.speechSynthesis.getVoices().find(v => v.lang === 'pt-PT') || null;
                window.speechSynthesis.speak(aviso);
              }
              return;
            }


      // Processa comandos de adicionar/remover produtos
      const isRemoveCommand = normalized.startsWith("remover ") || normalized.startsWith("tirar ") || normalized.startsWith("retirar ") || normalized.startsWith("apagar ");
      const rawItems = normalized
        .replace(/^remover |^tirar |^retirar |^apagar/, '')
        .split(/,| e /).map(s => s.trim()).filter(Boolean);

      const results = [];

      rawItems.forEach(item => {
        const match = this.sectionsPoints.find(point => {
          const name = point[1].toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, '').trim();
          return name === item || name.includes(item) || item.includes(name);
        });

        if (match) {
          const alreadySelected = this.shoppingListIds.includes(match[0]);

          if (isRemoveCommand) {
            if (alreadySelected) {
              this.shoppingListIds = this.shoppingListIds.filter(id => id !== match[0]);
              results.push(`Removido: ${match[1]}`);
            }
          } else {
            if (!alreadySelected) {
              this.shoppingListIds.push(match[0]);
            }
            results.push(`Adicionado: ${match[1]}`);
          }
        } else {
          if (item !== "") results.push(`Não encontrado: ${item}`);
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
        await axios.post('http://127.0.0.1:5000/list', this.shoppingList);
      } catch (error) {
        console.error(error);
      }
    },

    async GetSections() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/sections');
        this.sectionsPoints = response.data;
      } catch (error) {
        console.error(error);
      }
    },

    makeShoppingList() {
      const rawIds = [...this.shoppingListIds];
      this.shoppingList = this.sectionsPoints.filter(point => rawIds.includes(point[0]));
      this.postList();
      this.sectionsPoints = null;
       // Guarda os IDs no sessionStorage
      sessionStorage.setItem('savedShoppingListIds', JSON.stringify(this.shoppingListIds));
    }
  },

  mounted() {
    this.GetSections();

    const savedIds = sessionStorage.getItem('savedShoppingListIds');
    if (savedIds) {
    this.shoppingListIds = JSON.parse(savedIds);
    }
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