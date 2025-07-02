<template>
  <div class="home">
    
    <h1 class="title">Navguide</h1>

    <button class="btn invisual-btn" @click="iniciarInvisual">
      Entrar em modo Invisual
    </button>

    <button class="btn normal-btn" @click="iniciarNormal">
      Entrar em modo Normal
    </button>
  </div>
</template>

<script>
import logo from '@/assets/logo.svg';

export default {
  name: 'Home',
  data() {
    return {
      voiceSpoken: false,
    };
  },
  methods: {
    iniciarInvisual() {
      this.$router.push('/list');
    },

    iniciarNormal() {
      this.$router.push('/modo-normal');
    },

    falarInicio(callback) {
      const msg = new SpeechSynthesisUtterance(
        'Bem-vindo à Navguide. Toque no botão para modo invisual, ou modo normal.'
      );
      msg.lang = 'pt-PT';

      const setVoiceAndSpeak = () => {
        const voices = speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang === 'pt-PT') || voices[0];
        msg.voice = voice;
        speechSynthesis.speak(msg);
        if (callback) msg.onend = callback;
      };

      if (speechSynthesis.getVoices().length === 0) {
        speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
      } else {
        setVoiceAndSpeak();
      }
    },
  },

  mounted() {
    speechSynthesis.cancel();
    if (!this.voiceSpoken) {
      this.falarInicio();
      this.voiceSpoken = true;
    }
  },

  computed: {
    logo() {
      return logo;
    },
  },
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #5299d6, #367bb5);
  color: white;
  text-align: center;
  padding: 20px;
  box-sizing: border-box;
  user-select: none;
  animation: fadeIn 1s ease-in-out;
}

.logo {
  width: 120px;
  height: auto;
  margin-bottom: 20px;
}

.title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 32px;
}

.btn {
  font-size: 20px;
  padding: 16px 24px;
  margin: 12px 0;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  width: 80%;
  max-width: 300px;
  transition: background 0.3s ease;
  font-weight: 600;
}

.invisual-btn {
  background-color: #ffffff;
  color: #367bb5;
}

.invisual-btn:hover {
  background-color: #f0f0f0;
}

.normal-btn {
  background-color: #367bb5;
  color: white;
  border: 2px solid white;
}

.normal-btn:hover {
  background-color: #2e6ea1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

