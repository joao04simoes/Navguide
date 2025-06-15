<template>
  <div
    @click="handleClick"
    @touchstart.prevent
    @touchmove.prevent
  ></div>
  <div @click="irParaList" class="home">
    <img :src="logo" alt="Logo" style="width: 150px; margin-bottom: 20px;" />
    <h1>Bem-vindo à Navguide</h1>
    <p>Clique em qualquer parte para começar 🚶‍♂️</p>
  </div>
</template>



<script>
import logo from '@/assets/logo.svg';

export default {
  name: 'Home',
  data() {
    return {
      voiceSpoken: false,
      logo
    }
  },
  methods: {
    irParaList() {
      if (!this.voiceSpoken) {
        this.falarInicio()
        this.voiceSpoken = true
        const delay = 1500
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