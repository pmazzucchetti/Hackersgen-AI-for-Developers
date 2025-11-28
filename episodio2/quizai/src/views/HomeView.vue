<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'

const router = useRouter()
const quizStore = useQuizStore()

onMounted(async () => {
  await quizStore.fetchQuizzes()
})

const startQuiz = (quizId: string) => {
  router.push(`/quiz/${quizId}`)
}

const createNewQuiz = () => {
  router.push('/create')
}
</script>

<template>
  <div class="container">
    <header>
      <h1>📚 I Miei Quiz</h1>
      <p class="subtitle">Scegli un quiz per iniziare</p>
      <button @click="createNewQuiz" class="create-btn">
        ➕ Crea Nuovo Quiz
      </button>
    </header>

    <div v-if="quizStore.quizzes.length === 0" class="loading">
      <div class="spinner"></div>
      <p>Caricamento quiz...</p>
    </div>

    <div v-else class="quiz-grid">
      <div 
        v-for="quiz in quizStore.quizzes" 
        :key="quiz.id" 
        class="quiz-card"
      >
        <div class="quiz-icon">🎯</div>
        <h2>{{ quiz.titolo }}</h2>
        <div class="quiz-info">
          <span class="badge">{{ quiz.domande.length }} domande</span>
        </div>
        <button @click="startQuiz(quiz.id)" class="start-btn">Inizia Quiz</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.create-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.create-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.create-btn:active {
  transform: translateY(-1px);
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

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.quiz-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 2px solid transparent;
}

.quiz-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  border-color: #42b983;
}

.quiz-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.quiz-card h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.quiz-info {
  margin-bottom: 1.5rem;
}

.badge {
  background: #e8f5e9;
  color: #42b983;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.start-btn {
  background: linear-gradient(135deg, #42b983 0%, #35a372 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.start-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
}

.start-btn:active {
  transform: scale(0.98);
}
</style>

