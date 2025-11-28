<template>
  <div class="quiz-form">
    <h2>{{ isEditing ? 'Modifica Quiz' : 'Crea Nuovo Quiz' }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <!-- Titolo del Quiz -->
      <div class="form-group">
        <label for="quiz-title">Titolo del Quiz *</label>
        <input 
          id="quiz-title"
          v-model="formData.titolo"
          type="text"
          placeholder="Inserisci il titolo del quiz"
          :class="{ 'error': errors.titolo }"
        />
        <span v-if="errors.titolo" class="error-message">{{ errors.titolo }}</span>
      </div>

      <!-- Lista Domande -->
      <div class="questions-section">
        <div class="section-header">
          <h3>Domande</h3>
          <button type="button" @click="addQuestion" class="btn-add">
            + Aggiungi Domanda
          </button>
        </div>

        <div 
          v-for="(domanda, dIndex) in formData.domande" 
          :key="domanda.id"
          class="question-card"
        >
          <div class="question-header">
            <h4>Domanda {{ dIndex + 1 }}</h4>
            <button 
              type="button" 
              @click="removeQuestion(dIndex)"
              class="btn-remove"
              :disabled="formData.domande.length === 1"
            >
              Rimuovi
            </button>
          </div>

          <div class="form-group">
            <label :for="`question-${dIndex}`">Testo della domanda *</label>
            <input 
              :id="`question-${dIndex}`"
              v-model="domanda.testo"
              type="text"
              placeholder="Inserisci la domanda"
              :class="{ 'error': errors[`domanda-${dIndex}`] }"
            />
            <span v-if="errors[`domanda-${dIndex}`]" class="error-message">
              {{ errors[`domanda-${dIndex}`] }}
            </span>
          </div>

          <!-- Opzioni -->
          <div class="options-section">
            <div class="options-header">
              <label>Opzioni *</label>
              <button 
                type="button" 
                @click="addOption(dIndex)"
                class="btn-add-small"
              >
                + Aggiungi Opzione
              </button>
            </div>

            <div 
              v-for="(opzione, oIndex) in domanda.opzioni"
              :key="opzione.id"
              class="option-item"
            >
              <div class="option-content">
                <input 
                  type="radio"
                  :name="`correct-${dIndex}`"
                  :id="`option-${dIndex}-${oIndex}`"
                  :checked="opzione.corretta"
                  @change="setCorrectOption(dIndex, oIndex)"
                />
                <input 
                  type="text"
                  v-model="opzione.testo"
                  placeholder="Testo opzione"
                  :class="{ 'error': errors[`opzione-${dIndex}-${oIndex}`] }"
                />
                <button 
                  type="button"
                  @click="removeOption(dIndex, oIndex)"
                  class="btn-remove-small"
                  :disabled="domanda.opzioni.length === 2"
                >
                  ×
                </button>
              </div>
              <span v-if="errors[`opzione-${dIndex}-${oIndex}`]" class="error-message">
                {{ errors[`opzione-${dIndex}-${oIndex}`] }}
              </span>
            </div>

            <span v-if="errors[`opzioni-${dIndex}`]" class="error-message">
              {{ errors[`opzioni-${dIndex}`] }}
            </span>
          </div>
        </div>

        <span v-if="errors.domande" class="error-message">{{ errors.domande }}</span>
      </div>

      <!-- Pulsanti di Submit -->
      <div class="form-actions">
        <button type="button" @click="resetForm" class="btn-secondary">
          Annulla
        </button>
        <button type="submit" class="btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Salvataggio...' : 'Salva Quiz' }}
        </button>
      </div>

      <!-- Messaggio di successo -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useQuizStore } from '@/stores/quiz'
import type { Quiz, Domanda, Opzione } from '@/types/quiz'
import { createQuiz as createQuizService } from '@/service/quiz'

interface Props {
  initialQuiz?: Quiz
}

const props = defineProps<Props>()
const emit = defineEmits<{
  success: [quiz: Quiz]
  cancel: []
}>()

const quizStore = useQuizStore()

const isEditing = ref(!!props.initialQuiz)
const isSubmitting = ref(false)
const successMessage = ref('')
const errors = reactive<Record<string, string>>({})

// Funzione per generare ID unici
const generateId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

// Crea una nuova opzione vuota
const createEmptyOption = (corretta: boolean = false): Opzione => ({
  id: generateId(),
  testo: '',
  corretta
})

// Crea una nuova domanda vuota
const createEmptyQuestion = (): Domanda => ({
  id: generateId(),
  testo: '',
  opzioni: [
    createEmptyOption(true),
    createEmptyOption(false)
  ]
})

// Inizializza il form
const formData = reactive<Quiz>(
  props.initialQuiz 
    ? JSON.parse(JSON.stringify(props.initialQuiz))
    : {
        id: generateId(),
        titolo: '',
        domande: [createEmptyQuestion()]
      }
)

// Aggiungi domanda
const addQuestion = () => {
  formData.domande.push(createEmptyQuestion())
}

// Rimuovi domanda
const removeQuestion = (index: number) => {
  if (formData.domande.length > 1) {
    formData.domande.splice(index, 1)
  }
}

// Aggiungi opzione
const addOption = (questionIndex: number) => {
  formData.domande[questionIndex].opzioni.push(createEmptyOption())
}

// Rimuovi opzione
const removeOption = (questionIndex: number, optionIndex: number) => {
  const opzioni = formData.domande[questionIndex].opzioni
  if (opzioni.length > 2) {
    // Se l'opzione rimossa era quella corretta, imposta la prima come corretta
    if (opzioni[optionIndex].corretta && opzioni.length > 1) {
      const newCorrectIndex = optionIndex === 0 ? 1 : 0
      opzioni[newCorrectIndex].corretta = true
    }
    opzioni.splice(optionIndex, 1)
  }
}

// Imposta l'opzione corretta
const setCorrectOption = (questionIndex: number, optionIndex: number) => {
  formData.domande[questionIndex].opzioni.forEach((opt, idx) => {
    opt.corretta = idx === optionIndex
  })
}

// Validazione
const validate = (): boolean => {
  // Reset errors
  Object.keys(errors).forEach(key => delete errors[key])
  let isValid = true

  // Valida titolo
  if (!formData.titolo.trim()) {
    errors.titolo = 'Il titolo è obbligatorio'
    isValid = false
  }

  // Valida che ci sia almeno una domanda
  if (formData.domande.length === 0) {
    errors.domande = 'Aggiungi almeno una domanda'
    isValid = false
  }

  // Valida ogni domanda
  formData.domande.forEach((domanda, dIndex) => {
    // Valida testo domanda
    if (!domanda.testo.trim()) {
      errors[`domanda-${dIndex}`] = 'Il testo della domanda è obbligatorio'
      isValid = false
    }

    // Valida che ci siano almeno 2 opzioni
    if (domanda.opzioni.length < 2) {
      errors[`opzioni-${dIndex}`] = 'Ogni domanda deve avere almeno 2 opzioni'
      isValid = false
    }

    // Valida che ci sia almeno una risposta corretta
    const hasCorrect = domanda.opzioni.some(opt => opt.corretta)
    if (!hasCorrect) {
      errors[`opzioni-${dIndex}`] = 'Seleziona una risposta corretta'
      isValid = false
    }

    // Valida ogni opzione
    domanda.opzioni.forEach((opzione, oIndex) => {
      if (!opzione.testo.trim()) {
        errors[`opzione-${dIndex}-${oIndex}`] = 'Il testo dell\'opzione è obbligatorio'
        isValid = false
      }
    })
  })

  return isValid
}

// Submit del form
const handleSubmit = async () => {
  if (!validate()) {
    return
  }

  isSubmitting.value = true
  successMessage.value = ''

  try {
    // await quizStore.createQuiz(formData)
    await createQuizService(formData) // Direct call for debugging
    
    // Manually add to the store for UI update
    quizStore.quizzes.push(formData)

    successMessage.value = 'Quiz salvato con successo!'
    
    // Emetti evento di successo
    emit('success', formData)

    // Reset form dopo 2 secondi
    setTimeout(() => {
      resetForm()
      successMessage.value = ''
    }, 2000)
  } catch (error) {
    console.error('Errore nel salvataggio del quiz:', error)
    errors.submit = 'Errore nel salvataggio del quiz. Riprova.'
  } finally {
    isSubmitting.value = false
  }
}

// Reset del form
const resetForm = () => {
  if (props.initialQuiz) {
    emit('cancel')
  } else {
    formData.id = generateId()
    formData.titolo = ''
    formData.domande = [createEmptyQuestion()]
    Object.keys(errors).forEach(key => delete errors[key])
    successMessage.value = ''
  }
}
</script>

<style scoped>
.quiz-form {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input[type="text"]:focus {
  outline: none;
  border-color: #42b983;
}

input[type="text"].error {
  border-color: #e74c3c;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.success-message {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}

/* Questions Section */
.questions-section {
  margin-top: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h3 {
  color: #2c3e50;
  margin: 0;
}

.question-card {
  background: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-header h4 {
  color: #2c3e50;
  margin: 0;
}

/* Options Section */
.options-section {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.options-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.option-item {
  margin-bottom: 0.75rem;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.option-content input[type="radio"] {
  width: auto;
  cursor: pointer;
}

.option-content input[type="text"] {
  flex: 1;
}

/* Buttons */
button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #42b983;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #38a173;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
}

.btn-primary:disabled {
  background: #95d5b2;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-add {
  background: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn-add:hover {
  background: #0056b3;
}

.btn-add-small {
  background: #28a745;
  color: white;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.btn-add-small:hover {
  background: #218838;
}

.btn-remove {
  background: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn-remove:hover:not(:disabled) {
  background: #c82333;
}

.btn-remove:disabled {
  background: #e9a5ab;
  cursor: not-allowed;
}

.btn-remove-small {
  background: #dc3545;
  color: white;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  min-width: 32px;
}

.btn-remove-small:hover:not(:disabled) {
  background: #c82333;
}

.btn-remove-small:disabled {
  background: #e9a5ab;
  cursor: not-allowed;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e0e0e0;
}

/* Responsive */
@media (max-width: 768px) {
  .quiz-form {
    padding: 1rem;
  }

  .section-header,
  .question-header,
  .options-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  button {
    width: 100%;
  }
}
</style>

