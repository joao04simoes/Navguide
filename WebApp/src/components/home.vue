<template>
  <div
    @click="handleClick"
    @touchstart.prevent
    @touchmove.prevent
    class="home"
  >
    <img :src="logo" alt="Logo" style="width: 150px; margin-bottom: 20px;" />
    <h1>Bem-vindo à Navguide</h1>
    <p class="instruction-text">Clique para começar em modo invisual</p>
    <p class="instruction-text">Duplo clique para começar em modo normal</p>
  </div>
</template>

<script>
import logo from '@/assets/logo.svg';

export default {
  name: 'Home',
  data() {
    return {
      voiceSpoken: false,
      logo,
      clickCount: 0,
      clickTimeout: null,
    };
  },
  methods: {
    handleClick() {
      this.clickCount++;

      if (this.clickTimeout) {
        clearTimeout(this.clickTimeout);
      }

      this.clickTimeout = setTimeout(() => {
        if (this.clickCount === 1) {
          this.irParaList();
        } else if (this.clickCount === 2) {
          this.$router.push('/modo-normal');
        }
        this.clickCount = 0;
      }, 300);
    },

    irParaList() {
      if (!this.voiceSpoken) {
        this.falarInicio();
        this.voiceSpoken = true;
        const delay = 1500;
        setTimeout(() => {
          this.$router.push('/list');
        }, delay);
      } else {
        this.$router.push('/list');
      }
    },

    falarInicio() {
      const msg = new SpeechSynthesisUtterance('Bem vindo à Navgaide. Se for invisual, clique no ecrã para começar. Se não, duplo-clique.');
      msg.lang = 'pt-PT';
      const voices = window.speechSynthesis.getVoices();
      const voice = voices.find(v => v.lang === 'pt-PT') || voices[0];
      msg.voice = voice;
      window.speechSynthesis.speak(msg);
    },
  },
  
  mounted() {
    speechSynthesis.cancel();
    if (!this.voiceSpoken) {
      this.falarInicio();
      this.voiceSpoken = true;
    }
    window.speechSynthesis.onvoiceschanged = () => {
      if (!this.voiceSpoken) {
        this.falarInicio();
        this.voiceSpoken = true;
      }
    };
  },

};
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
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.instruction-text {
  font-size: 18px;
  margin-top: 8px;
  font-weight: 500;
  opacity: 0.85;
}
</style>
