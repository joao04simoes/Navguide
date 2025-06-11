<template>
  <div>
    <h1>Deseja iniciar a navegação?</h1>
    <p>A lista já foi criada com os produtos selecionados.</p>

    <button @click="goToRoute">Sim, iniciar</button>
    <button @click="goBack">Não, voltar</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToRoute() {
      this.$router.push('/route');
    },
    goBack() {
      this.$router.push('/list');
    }
  }
}
</script>

<style scoped>
div {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  margin: auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

button {
  margin: 1rem;
  background-color: #3498db;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}
</style>
