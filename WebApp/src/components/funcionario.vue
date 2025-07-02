<template>
  <div class="touch-area">
    <header class="app-header">
      <h1>NavGuide</h1>
    </header>

    <div class="container">
      <template v-if="called">
        <h2>👨‍💼 Um funcionário está a caminho...</h2>
        <button @click="cancel" class="btCancel">Voltar</button>
      </template>

      <template v-else>
        <h2>Quer chamar um funcionário?</h2>
        <div class="buttons">
          <button @click="callEmployee" class="btCall">Chamar Funcionário</button>
          <button @click="cancel" class="btCancel">Cancelar</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      called: false
    };
  },
  mounted() {
    speechSynthesis.cancel();
    this.speak("Quer chamar um funcionário?");
  },
  methods: {
    speak(text) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-PT';
      speechSynthesis.speak(utterance);
    },
    callEmployee() {
      this.called = true;
      speechSynthesis.cancel();
      this.speak("Um funcionário está a caminho.");
    },
    cancel() {
      speechSynthesis.cancel();
      this.speak("Pedido cancelado.");
      setTimeout(() => {
        this.$router.push('/route');
      }, 1500);
    }
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

.touch-area {
  height: 100dvh;
  width: 100dvw;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.app-header {
  background: linear-gradient(135deg, #2c3e50, #3498db);
  padding: 1rem 2rem;
  color: #fff;
  font-weight: 700;
  font-size: 1.8rem;
  width: 100%;
  text-align: center;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.container {
  margin-top: auto;
  margin-bottom: auto;
  text-align: center;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.08);
  background: #fff;
  max-width: 420px;
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
  justify-content: center;
}

h2 {
  color: #2c3e50;
  font-size: 1.4rem;
}

.buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
  min-width: 160px;
}

.btCall {
  background: linear-gradient(135deg, #2980b9, #3498db);
}

.btCall:hover {
  background: linear-gradient(135deg, #1f5f8b, #2b7bb5);
  transform: translateY(-2px);
}

.btCancel {
  background: #888;
}

.btCancel:hover {
  background: #666;
  transform: translateY(-2px);
}
</style>
