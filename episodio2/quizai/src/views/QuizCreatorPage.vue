<template>
  <div class="quiz-creator-page">
    <div class="container">
      <div class="page-header">
        <button @click="goBack" class="btn-back">
          ← Torna indietro
        </button>
        <h1>Creatore di Quiz</h1>
        <p class="subtitle">Crea e gestisci i tuoi quiz personalizzati</p>
      </div>

      <!-- Quiz Form -->
      <QuizForm 
        @success="handleSuccess"
        @cancel="handleCancel"
      />

      <!-- Lista dei Quiz Creati -->
      <div v-if="quizStore.quizzes.length > 0" class="quiz-list-section">
        <h2>Quiz Creati</h2>
        <div class="quiz-grid">
          <div 
            v-for="quiz in quizStore.quizzes" 
            :key="quiz.id"
            class="quiz-card"
          >
            <div class="quiz-card-content">
              <h3>{{ quiz.titolo }}</h3>
              <p class="quiz-info">
                {{ quiz.domande.length }} {{ quiz.domande.length === 1 ? 'domanda' : 'domande' }}
              </p>
              <div class="quiz-details">
                <div 
                  v-for="(domanda, index) in quiz.domande" 
                  :key="domanda.id"
                  class="question-preview"
                >
                  <span class="question-number">{{ index + 1 }}.</span>
                  <span class="question-text">{{ domanda.testo }}</span>
                  <span class="options-count">
                    ({{ domanda.opzioni.length }} opzioni)
                  </span>
                </div>
              </div>
            </div>
            <div class="quiz-card-actions">
              <button @click="viewQuiz(quiz.id)" class="btn-view">
                Visualizza
              </button>
              <button @click="deleteQuiz(quiz.id)" class="btn-delete">
                Elimina
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>Nessun quiz creato ancora</h3>
        <p>Inizia creando il tuo primo quiz usando il form sopra!</p>
      </div>
    </div>

    <!-- Modal di conferma eliminazione -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content" @click.stop>
        <h3>Conferma Eliminazione</h3>
        <p>Sei sicuro di voler eliminare questo quiz? Questa azione non può essere annullata.</p>
        <div class="modal-actions">
          <button @click="closeDeleteModal" class="btn-cancel">
            Annulla
          </button>
          <button @click="confirmDelete" class="btn-confirm-delete">
            Elimina
          </button>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div v-if="notification.show" :class="['toast-notification', notification.type]">
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import QuizForm from '@/components/QuizForm.vue'
import { useQuizStore } from '@/stores/quiz'
import type { Quiz } from '@/types/quiz'

const router = useRouter()
const quizStore = useQuizStore()

const showDeleteModal = ref(false)
const quizToDelete = ref<string | null>(null)
const notification = reactive({
  show: false,
  message: '',
  type: 'success' as 'success' | 'error'
})

// Carica i quiz all'avvio
onMounted(async () => {
  try {
    await quizStore.fetchQuizzes()
  } catch (error) {
    console.error('Errore nel caricamento dei quiz:', error)
  }
})

// Gestisci successo creazione quiz
const handleSuccess = (quiz: Quiz) => {
  showNotification('Quiz creato con successo!', 'success')
}

// Gestisci annullamento
const handleCancel = () => {
  console.log('Creazione annullata')
}

// Torna indietro
const goBack = () => {
  router.push('/')
}

// Visualizza quiz
const viewQuiz = (quizId: string) => {
  router.push(`/quiz/${quizId}`)
}

// Elimina quiz
const deleteQuiz = (quizId: string) => {
  quizToDelete.value = quizId
  showDeleteModal.value = true
}

// Conferma eliminazione
const confirmDelete = async () => {
  if (quizToDelete.value) {
    try {
      await quizStore.removeQuiz(quizToDelete.value)
      showNotification('Quiz eliminato con successo', 'success')
    } catch (error) {
      showNotification('Errore nell\'eliminazione del quiz', 'error')
      console.error('Errore nell\'eliminazione:', error)
    }
  }
  closeDeleteModal()
}

// Chiudi modal
const closeDeleteModal = () => {
  showDeleteModal.value = false
  quizToDelete.value = null
}

// Mostra notifica
const showNotification = (message: string, type: 'success' | 'error') => {
  notification.message = message
  notification.type = type
  notification.show = true

  setTimeout(() => {
    notification.show = false
  }, 3000)
}
</script>

<style scoped>
.quiz-creator-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Page Header */
.page-header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
  position: relative;
}

.btn-back {
  position: absolute;
  left: 0;
  top: 0;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(-5px);
}

.page-header h1 {
  font-size: 3rem;
  margin: 0 0 0.5rem 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

/* Quiz List Section */
.quiz-list-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-top: 3rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.quiz-list-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.quiz-card {
  background: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.quiz-card-content h3 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.3rem;
}

.quiz-info {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
}

.quiz-details {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  max-height: 200px;
  overflow-y: auto;
}

.question-preview {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #495057;
}

.question-number {
  font-weight: 600;
  color: #667eea;
}

.question-text {
  flex: 1;
}

.options-count {
  color: #6c757d;
  font-size: 0.85rem;
}

.quiz-card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-view,
.btn-delete {
  flex: 1;
  padding: 0.6rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view {
  background: #007bff;
  color: white;
}

.btn-view:hover {
  background: #0056b3;
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn-delete:hover {
  background: #c82333;
}

/* Empty State */
.empty-state {
  background: white;
  border-radius: 16px;
  padding: 4rem 2rem;
  text-align: center;
  margin-top: 3rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6c757d;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.modal-content p {
  color: #6c757d;
  margin: 0 0 1.5rem 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel,
.btn-confirm-delete {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background: #5a6268;
}

.btn-confirm-delete {
  background: #dc3545;
  color: white;
}

.btn-confirm-delete:hover {
  background: #c82333;
}

/* Toast Notification */
.toast-notification {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  animation: slideIn 0.3s ease-out;
}

.toast-notification.success {
  background: #28a745;
  color: white;
}

.toast-notification.error {
  background: #dc3545;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .btn-back {
    position: static;
    margin-bottom: 1rem;
    width: 100%;
  }

  .quiz-grid {
    grid-template-columns: 1fr;
  }

  .toast-notification {
    left: 1rem;
    right: 1rem;
  }
}
</style>

