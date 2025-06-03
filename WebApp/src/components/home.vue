<template>
  <div @touchstart="startTouch" @touchend="endTouch" class="home">
    <h1>Bem-vindo à Navguide</h1>
    <p>Deslize para a esquerda para começar 🚶‍♂️</p>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      startX: 0,
      voiceSpoken: false // para garantir que só fala uma vez
    }
  },
  methods: {
    startTouch(event) {
      this.startX = event.changedTouches[0].screenX

      // Fala ao primeiro toque
      if (!this.voiceSpoken) {
        this.falarInicio()
        this.voiceSpoken = true
      }
    },
    endTouch(event) {
      const endX = event.changedTouches[0].screenX
      const diffX = this.startX - endX

      if (diffX > 50) {
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
    // Para garantir que as vozes estão carregadas antes de falar
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