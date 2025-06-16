<template>
  <div 
    class="touch-area" 
    @click="handleSingleTap" 
    @dblclick="handleDoubleTap"
  >
    <div class="container">
      <h2>Quer chamar um funcionário?</h2>
      <p>Clique curto: Não</p>
      <p>Duplo clique: Sim</p>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    speechSynthesis.cancel();
    this.speak(
      "Quer chamar um funcionário? Clique curto: não. Duplo clique: sim."
    );
  },
  methods: {
    speak(text) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-PT';
      speechSynthesis.speak(utterance);
    },
    handleSingleTap() {
      speechSynthesis.cancel();
      this.speak("Pedido cancelado.");
      setTimeout(() => {
        this.$router.push('/route');
      }, 1500);
    },
    handleDoubleTap() {
      speechSynthesis.cancel();
      this.speak("A chamar funcionário.");
      setTimeout(() => {
        this.$router.push('/route');
      }, 2000);
    }
  }
}
</script>

<style>
.touch-area {
  height: 100dvh;
  width: 100dvw;
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  -webkit-user-select: none;
  cursor: pointer;
  background: #fff;
}

.container {
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0,0,0,0.1);
  max-width: 400px;
}

h2 {
  margin-bottom: 1rem;
  color: #333;
}

p {
  margin: 0.4rem 0;
  font-size: 1.1rem;
  color: #555;
}
</style>
