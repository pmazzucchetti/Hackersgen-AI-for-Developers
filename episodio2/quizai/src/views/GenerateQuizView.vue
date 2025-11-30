<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { generateQuiz } from '@/service/quiz'

const router = useRouter()

const tema = ref('')
const difficolta = ref('facile')
const numeroDomande = ref(5)
const isLoading = ref(false)
const error = ref<string | null>(null)

const difficoltaOptions = [
  { value: 'facile', label: 'Facile' },
  { value: 'medio', label: 'Medio' },
  { value: 'difficile', label: 'Difficile' }
]

const numeroDomandeOptions = Array.from({ length: 10 }, (_, i) => i + 1)

const handleSubmit = async () => {
  if (!tema.value.trim()) {
    error.value = 'Inserisci un tema per il quiz'
    return
  }

  error.value = null
  isLoading.value = true

  try {
    await generateQuiz({
      tema: tema.value.trim(),
      difficolta: difficolta.value,
      numeroDomande: numeroDomande.value
    })
    
    // Dopo la generazione, torna alla home
    router.push('/')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Errore durante la generazione del quiz'
  } finally {
    isLoading.value = false
  }
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="container">
    <header>
      <button @click="goBack" class="back-btn">← Torna alla Home</button>
      <h1>🤖 Genera Quiz con AI</h1>
      <p class="subtitle">Compila il form per generare un nuovo quiz</p>
    </header>

    <div class="form-container">
      <form @submit.prevent="handleSubmit" class="quiz-form">
        <div class="form-group">
          <label for="tema">Tema del Quiz</label>
          <textarea
            id="tema"
            v-model="tema"
            placeholder="Inserisci il tema o argomento del quiz..."
            rows="4"
            class="form-input"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="difficolta">Difficoltà</label>
          <select
            id="difficolta"
            v-model="difficolta"
            class="form-input"
          >
            <option
              v-for="option in difficoltaOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="numeroDomande">Numero di Domande</label>
          <select
            id="numeroDomande"
            v-model="numeroDomande"
            class="form-input"
          >
            <option
              v-for="num in numeroDomandeOptions"
              :key="num"
              :value="num"
            >
              {{ num }}
            </option>
          </select>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="submit-btn"
        >
          <span v-if="isLoading">Generazione in corso...</span>
          <span v-else>Genera Quiz</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 0;
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #5a6268;
  transform: translateX(-3px);
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.form-container {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.quiz-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  resize: vertical;
}

.form-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.form-input textarea {
  min-height: 100px;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #fcc;
  font-size: 0.9rem;
}

.submit-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(245, 87, 108, 0.5);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .back-btn {
    position: relative;
    margin-bottom: 1rem;
  }
}
</style>

