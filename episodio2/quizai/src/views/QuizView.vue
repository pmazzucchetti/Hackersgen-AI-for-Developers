<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import type { Quiz, Domanda } from '@/types/quiz'

const route = useRoute()
const router = useRouter()
const quizStore = useQuizStore()

const quiz = ref<Quiz | null>(null)
const currentQuestionIndex = ref(0)
const selectedAnswers = ref<Map<string, string>>(new Map())
const showResults = ref(false)

onMounted(async () => {
  if (quizStore.quizzes.length === 0) {
    await quizStore.fetchQuizzes()
  }
  
  const quizId = route.params.id as string
  quiz.value = quizStore.quizzes.find(q => q.id === quizId) || null
  
  if (!quiz.value) {
    router.push('/')
  }
})

const currentQuestion = computed(() => {
  if (!quiz.value) return null
  return quiz.value.domande[currentQuestionIndex.value]
})

const progress = computed(() => {
  if (!quiz.value) return 0
  return ((currentQuestionIndex.value + 1) / quiz.value.domande.length) * 100
})

const selectAnswer = (questionId: string, answerId: string) => {
  selectedAnswers.value.set(questionId, answerId)
}

const nextQuestion = () => {
  if (!quiz.value) return
  
  if (currentQuestionIndex.value < quiz.value.domande.length - 1) {
    currentQuestionIndex.value++
  } else {
    showResults.value = true
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const canProceed = computed(() => {
  if (!currentQuestion.value) return false
  return selectedAnswers.value.has(currentQuestion.value.id)
})

const calculateScore = computed(() => {
  if (!quiz.value) return { correct: 0, total: 0, percentage: 0 }
  
  let correct = 0
  quiz.value.domande.forEach(domanda => {
    const selectedAnswerId = selectedAnswers.value.get(domanda.id)
    const correctOption = domanda.opzioni.find(o => o.corretta)
    
    if (selectedAnswerId === correctOption?.id) {
      correct++
    }
  })
  
  const total = quiz.value.domande.length
  const percentage = Math.round((correct / total) * 100)
  
  return { correct, total, percentage }
})

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  selectedAnswers.value.clear()
  showResults.value = false
}

const goHome = () => {
  router.push('/')
}

const getScoreMessage = (percentage: number) => {
  if (percentage === 100) return '🎉 Perfetto! Hai risposto correttamente a tutte le domande!'
  if (percentage >= 80) return '🌟 Ottimo lavoro! Hai una buona conoscenza dell\'argomento!'
  if (percentage >= 60) return '👍 Buono! C\'è ancora margine di miglioramento!'
  if (percentage >= 40) return '📚 Continua a studiare, sei sulla strada giusta!'
  return '💪 Non mollare! Riprova e migliorerai!'
}
</script>

<template>
  <div class="quiz-container">
    <div v-if="!quiz" class="loading">
      <div class="spinner"></div>
      <p>Caricamento quiz...</p>
    </div>

    <div v-else-if="!showResults" class="quiz-content">
      <header class="quiz-header">
        <button @click="goHome" class="back-btn">← Indietro</button>
        <h1>{{ quiz.titolo }}</h1>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <p class="question-counter">
          Domanda {{ currentQuestionIndex + 1 }} di {{ quiz.domande.length }}
        </p>
      </header>

      <div v-if="currentQuestion" class="question-card">
        <h2 class="question-text">{{ currentQuestion.testo }}</h2>
        
        <div class="options-container">
          <div 
            v-for="option in currentQuestion.opzioni" 
            :key="option.id"
            class="option-card"
            :class="{ 
              'selected': selectedAnswers.get(currentQuestion.id) === option.id 
            }"
            @click="selectAnswer(currentQuestion.id, option.id)"
          >
            <div class="option-radio">
              <div class="radio-inner"></div>
            </div>
            <span class="option-text">{{ option.testo }}</span>
          </div>
        </div>

        <div class="navigation-buttons">
          <button 
            v-if="currentQuestionIndex > 0"
            @click="previousQuestion" 
            class="nav-btn secondary"
          >
            ← Precedente
          </button>
          <button 
            @click="nextQuestion" 
            class="nav-btn primary"
            :disabled="!canProceed"
          >
            {{ currentQuestionIndex < quiz.domande.length - 1 ? 'Successiva →' : 'Vedi Risultati' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="results-container">
      <div class="results-card">
        <div class="score-circle" :class="{ 
          'excellent': calculateScore.percentage >= 80,
          'good': calculateScore.percentage >= 60 && calculateScore.percentage < 80,
          'fair': calculateScore.percentage >= 40 && calculateScore.percentage < 60,
          'poor': calculateScore.percentage < 40
        }">
          <div class="score-value">{{ calculateScore.percentage }}%</div>
          <div class="score-label">Punteggio</div>
        </div>

        <h2 class="results-title">Quiz Completato!</h2>
        <p class="score-message">{{ getScoreMessage(calculateScore.percentage) }}</p>
        
        <div class="score-details">
          <div class="detail-item">
            <span class="detail-label">Risposte Corrette</span>
            <span class="detail-value">{{ calculateScore.correct }} / {{ calculateScore.total }}</span>
          </div>
        </div>

        <div class="results-buttons">
          <button @click="restartQuiz" class="nav-btn secondary">
            🔄 Riprova
          </button>
          <button @click="goHome" class="nav-btn primary">
            🏠 Torna ai Quiz
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem;
  color: #7f8c8d;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b983;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.quiz-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.quiz-header {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: #42b983;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
  font-weight: 600;
  transition: opacity 0.2s;
}

.back-btn:hover {
  opacity: 0.7;
}

.quiz-header h1 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #42b983 0%, #35a372 100%);
  transition: width 0.3s ease;
}

.question-counter {
  text-align: center;
  color: #7f8c8d;
  font-weight: 600;
}

.question-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.question-text {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-weight: 600;
  line-height: 1.5;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.option-card:hover {
  border-color: #42b983;
  background: #f8fff8;
  transform: translateX(4px);
}

.option-card.selected {
  border-color: #42b983;
  background: #e8f5e9;
}

.option-radio {
  width: 24px;
  height: 24px;
  border: 2px solid #7f8c8d;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.option-card:hover .option-radio,
.option-card.selected .option-radio {
  border-color: #42b983;
}

.option-card.selected .option-radio {
  background: #42b983;
}

.option-card.selected .option-radio .radio-inner {
  width: 10px;
  height: 10px;
  background: white;
  border-radius: 50%;
}

.option-text {
  font-size: 1.1rem;
  color: #2c3e50;
  flex: 1;
}

.navigation-buttons {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.nav-btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.nav-btn.primary {
  background: linear-gradient(135deg, #42b983 0%, #35a372 100%);
  color: white;
}

.nav-btn.primary:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
}

.nav-btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-btn.secondary {
  background: #e0e0e0;
  color: #2c3e50;
}

.nav-btn.secondary:hover {
  background: #d0d0d0;
}

.results-container {
  animation: fadeIn 0.5s ease-in;
}

.results-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  text-align: center;
}

.score-circle {
  width: 200px;
  height: 200px;
  margin: 0 auto 2rem;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.score-circle.excellent {
  background: linear-gradient(135deg, #42b983 0%, #35a372 100%);
}

.score-circle.good {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
}

.score-circle.fair {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
}

.score-circle.poor {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
}

.score-value {
  font-size: 3rem;
  font-weight: 700;
  color: white;
}

.score-label {
  font-size: 1rem;
  color: white;
  opacity: 0.9;
}

.results-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 700;
}

.score-message {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.score-details {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.detail-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #42b983;
}

.results-buttons {
  display: flex;
  gap: 1rem;
}

@media (max-width: 768px) {
  .quiz-container {
    padding: 1rem;
  }

  .quiz-header {
    padding: 1.5rem;
  }

  .quiz-header h1 {
    font-size: 1.5rem;
  }

  .question-card {
    padding: 1.5rem;
  }

  .question-text {
    font-size: 1.25rem;
  }

  .option-text {
    font-size: 1rem;
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .results-card {
    padding: 2rem;
  }

  .score-circle {
    width: 150px;
    height: 150px;
  }

  .score-value {
    font-size: 2.5rem;
  }

  .results-buttons {
    flex-direction: column;
  }
}
</style>

