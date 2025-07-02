<template>
  <header class="app-header">
    <h1>NavGuide</h1>
  </header>
  <div class="sections-container">
    <h1 class="page-title">Selecione os produtos e siga o melhor percurso</h1>
    <p class="instruction-text">Selecione os itens para sua lista de compras:</p>

    <div class="button-group">
      <button class="btn primary" @click="makeShoppingList" aria-label="Criar lista de compras e navegar">
        Criar Lista e Navegar
      </button>
      <button class="btn secondary" @click="goHome" aria-label="Voltar para página inicial">
        Voltar
      </button>
    </div>

    <div class="grid" role="list" aria-label="Lista de produtos disponíveis">
      <div class="item-card" v-for="(point, index) in sectionsPoints" :key="index"
        :class="{ selected: shoppingListIds.includes(point[0]) }" @click="toggleItem(point[0])" role="listitem"
        tabindex="0" @keyup.enter="toggleItem(point[0])"
        :aria-pressed="shoppingListIds.includes(point[0]) ? 'true' : 'false'">
        <input type="checkbox" :value="point[0]" v-model="shoppingListIds"
          :aria-label="`Selecionar item ${point[1]}`" />
        <span class="item-name">{{ point[1] }}</span>
      </div>
    </div>



    <div v-if="shoppingList && shoppingList.length" class="shopping-list" aria-live="polite">
      <h2>Lista de Compras</h2>
      <ul>
        <li v-for="(point, index) in shoppingList" :key="index">
          {{ point[1] }} - Local: {{ point[2] }} - Categoria: {{ point[3] }}
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
      sectionsPoints: [],
      shoppingListIds: [],
      shoppingList: [],
    };
  },

  methods: {
    goHome() {
      this.$router.push('/home');
    },

    async GetSections() {
      try {
        const response = await axios.get('http://192.168.1.64:5000/sections');
        this.sectionsPoints = response.data;
      } catch (error) {
        console.error('Erro ao carregar seções:', error);
      }
    },

    async postList() {
      try {
        await axios.post('http://192.168.1.64:5000/list', this.shoppingList);
      } catch (error) {
        console.error('Erro ao enviar lista:', error);
      }
    },

    makeShoppingList() {
      if (!this.shoppingListIds.length) {
        alert('A lista está vazia. Selecione itens primeiro.');
        return;
      }

      // Monta a lista filtrando os itens selecionados
      this.shoppingList = this.sectionsPoints.filter(point =>
        this.shoppingListIds.includes(point[0])
      );

      this.postList();

      // Salva a lista no sessionStorage para persistência temporária
      sessionStorage.setItem('savedShoppingListIds', JSON.stringify(this.shoppingListIds));

      // Navega para a rota de percurso
      this.$router.push('/route');
    },

    toggleItem(id) {
      const index = this.shoppingListIds.indexOf(id);
      if (index === -1) {
        this.shoppingListIds.push(id);
      } else {
        this.shoppingListIds.splice(index, 1);
      }
    }

  },

  mounted() {
    // Cancela qualquer síntese de voz ativa
    speechSynthesis.cancel();

    // Busca os produtos do backend
    this.GetSections();

    // Recupera a lista salva, caso exista
    const savedIds = sessionStorage.getItem('savedShoppingListIds');
    if (savedIds) {
      this.shoppingListIds = JSON.parse(savedIds);
    }

    // Armazena página atual para navegação posterior
    localStorage.setItem('ultimaPagina', 'modo-normal');
  }
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

.app-header {
  background: linear-gradient(135deg, #2c3e50, #3498db);
  padding: 1.2rem;
  text-align: center;
  color: #fff;
  font-weight: 400;
  font-size: 1rem;
  user-select: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.app-header h1 {
  margin: 0;
}

.sections-container {
  max-width: 960px;
  margin: 0rem auto;
  padding: 2rem;
  background: #ffffff;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  color: #2c3e50;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  text-align: center;
  color: #2c3e50;
}

.instruction-text {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #666;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

.item-card {
  background: #fafafa;
  border: 2px solid transparent;
  padding: 1.4rem;
  border-radius: 14px;
  cursor: pointer;
  user-select: none;
  text-align: center;
  position: relative;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.item-card:hover,
.item-card:focus {
  border-color: #27ae60;
  background-color: #eafbe8;
  box-shadow: 0 0 15px rgba(39, 174, 96, 0.25);
}

.item-card.selected {
  border-color: #27ae60;
  background-color: #d4f5d8;
  box-shadow: 0 0 15px rgba(39, 174, 96, 0.3);
}

.item-name {
  display: block;
  margin-top: 1rem;
  font-weight: 600;
  font-size: 1.1rem;
  color: #2c3e50;
}

input[type="checkbox"] {
  position: absolute;
  top: 1rem;
  right: 1rem;
  transform: scale(1.4);
  cursor: pointer;
  accent-color: #27ae60;
}

.button-group {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.btn {
  padding: 1rem 2.2rem;
  font-size: 1.1rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
  min-width: 180px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn.primary {
  background-color: #3498db;
  color: white;
}

.btn.primary:hover,
.btn.primary:focus {
  background-color: #2c3e50;
  box-shadow: 0 6px 16px rgba(39, 174, 96, 0.5);
  transform: translateY(-2px);
}

.btn.secondary {
  background-color: #d7dfe2;
  color: #2c3e50;
}

.btn.secondary:hover,
.btn.secondary:focus {
  background-color: #b3c0c3;
  box-shadow: 0 6px 16px rgba(44, 62, 80, 0.15);
  transform: translateY(-2px);
}

.shopping-list {
  background: #fcfcfc;
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid #ddd;
  max-width: 800px;
  margin: 0 auto 3rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.shopping-list h2 {
  margin-bottom: 1.5rem;
  font-size: 1.9rem;
  font-weight: 700;
  color: #27ae60;
  text-align: center;
}

.shopping-list ul {
  list-style: none;
  padding-left: 0;
}

.shopping-list li {
  font-size: 1.15rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  color: #34495e;
}
</style>
