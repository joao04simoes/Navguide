<template>
  <div
    @click="handleClick"
    class="click-area"
  >
    <p>Clique uma vez para voltar. Clique duas vezes para iniciar a navegação.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      clickCount: 0,
      clickTimeout: null,
    };
  },
  methods: {
    handleClick() {
      this.clickCount++;

      if (this.clickCount === 1) {
        this.clickTimeout = setTimeout(() => {
          // Clique único: voltar para a lista
          this.$router.push('/list');
          this.clickCount = 0;
        }, 300);
      } else if (this.clickCount === 2) {
        clearTimeout(this.clickTimeout);
        // Duplo clique: ir para rota de navegação
        this.$router.push('/route');
        this.clickCount = 0;
      }
    },
  },
};
</script>

<style scoped>
.click-area {
  background: white;
  padding: 2rem;
  margin: 2rem auto;
  border-radius: 12px;
  max-width: 500px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
