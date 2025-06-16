<template>
  <div class="sections-container">
    <p class="instruction-text">
      Modo normal
    </p>

    <ul>
      <li v-for="(point, index) in sectionsPoints" :key="index">
        <label>
          <input type="checkbox" v-model="shoppingListIds" :value="point[0]" />
          {{ point[1] }}
        </label>
      </li>
    </ul>

    <button @click="makeShoppingList">Criar Lista e Navegar</button>
    <button @click="goHome" style="margin-left: 1rem;">Voltar</button>

    <div v-if="shoppingList" class="shopping-list">
      <h2>Lista de Compras</h2>
      <ul>
        <li v-for="(point, index) in shoppingList" :key="index">
          {{ point[1] }}: {{ point[2] }} : {{ point[3] }}
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
      sectionsPoints: null,
      shoppingListIds: [],
      shoppingList: null,
    };
  },

  methods: {
    goHome() {
      this.$router.push('/home');
    },

    async GetSections() {
      try {
        const response = await axios.get('http://192.168.1.2:5000/sections');
        this.sectionsPoints = response.data;
      } catch (error) {
        console.error(error);
      }
    },

    async postList() {
      try {
        await axios.post('http://192.168.1.2:5000/list', this.shoppingList);
      } catch (error) {
        console.error(error);
      }
    },

    makeShoppingList() {
      if (!this.shoppingListIds.length) {
        alert('A lista está vazia. Selecione itens primeiro.');
        return;
      }

      this.shoppingList = this.sectionsPoints.filter(point =>
        this.shoppingListIds.includes(point[0])
      );

      this.postList();

      sessionStorage.setItem('savedShoppingListIds', JSON.stringify(this.shoppingListIds));

      // Redireciona para rota de navegação
      this.$router.push('/route');
    }
  },

  mounted() {
    speechSynthesis.cancel();
    this.GetSections();

    const savedIds = sessionStorage.getItem('savedShoppingListIds');
    if (savedIds) {
      this.shoppingListIds = JSON.parse(savedIds);
    }

    localStorage.setItem('ultimaPagina', 'modo-normal');
  }
};
</script>

<style scoped>
.sections-container, .shopping-list {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  margin: 1rem auto;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

.instruction-text {
  font-weight: bold;
  margin-bottom: 1rem;
}

ul {
  padding: 0;
  list-style: none;
}

li {
  padding: 0.5rem 0;
}

button {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
  font-size: 1rem;
}

button:hover {
  background-color: #2ecc71;
}
</style>
