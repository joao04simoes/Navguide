<template>
  <div
  @click="handleClick"
  @touchstart.prevent
  @touchmove.prevent
></div>
  <div @click="irParaList" class="home">
    <h1>Bem-vindo à Navguide</h1>
    <p>Clique em qualquer parte para começar 🚶‍♂️</p>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      voiceSpoken: false
    }
  },
  methods: {
    irParaList() {
      // Fala apenas na primeira vez antes de navegar
      if (!this.voiceSpoken) {
        this.falarInicio()
        this.voiceSpoken = true

        // Aguardar a fala terminar antes de mudar de página (opcional)
        const delay = 1500 // ajustável
        setTimeout(() => {
          this.$router.push('/list')
        }, delay)
      } else {
        this.$router.push('/list')
      }
    },
    falarInicio() {
      const msg = new SpeechSynthesisUtterance('Página inicial')
      msg.lang = 'pt-PT'

      const voices = window.speechSynthesis.getVoices()
      const voice = voices.find(v => v.lang === 'pt-PT') || voices[0]
      msg.voice = voice

      window.speechSynthesis.speak(msg)
    }
  },
  mounted() {
    // Garante que a voz é carregada (e fala) no carregamento inicial
    window.speechSynthesis.onvoiceschanged = () => {
      if (!this.voiceSpoken) {
        this.falarInicio()
        this.voiceSpoken = true
      }
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #5299d6;
  color: white;
  flex-direction: column;
  text-align: center;
  font-size: 24px;
}
</style>