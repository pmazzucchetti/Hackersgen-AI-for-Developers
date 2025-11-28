import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Quiz } from '@/types/quiz'
import { 
  getAllQuiz, 
  createQuiz as createQuizService, 
  deleteQuiz as deleteQuizService,
  getQuizById as getQuizByIdService,
  updateQuiz as updateQuizService
} from '@/service/quiz'

export const useQuizStore = defineStore('quiz', () => {
  const quizzes = ref<Quiz[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Computed: numero totale di quiz
   */
  const totalQuizzes = computed(() => quizzes.value.length)

  /**
   * Computed: trova un quiz per ID
   */
  const getQuizById = computed(() => {
    return (id: string) => quizzes.value.find(q => q.id === id)
  })

  /**
   * Recupera tutti i quiz
   */
  const fetchQuizzes = async () => {
    loading.value = true
    error.value = null
    try {
      const quizzesData = await getAllQuiz()
      quizzes.value = quizzesData
    } catch (err) {
      error.value = 'Errore nel caricamento dei quiz'
      console.error('Errore fetchQuizzes:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crea un nuovo quiz
   * @param quizData - I dati del quiz da creare
   */
  const createQuiz = async (quizData: Quiz) => {
    loading.value = true
    error.value = null
    try {
      const newQuiz = await createQuizService(quizData)
      
      // Verifica se il quiz esiste già (aggiornamento)
      const existingIndex = quizzes.value.findIndex(q => q.id === newQuiz.id)
      if (existingIndex !== -1) {
        quizzes.value[existingIndex] = newQuiz
      } else {
        quizzes.value.push(newQuiz)
      }
      
      return newQuiz
    } catch (err) {
      error.value = 'Errore nella creazione del quiz'
      console.error('Errore createQuiz:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Rimuove un quiz
   * @param id - L'ID del quiz da rimuovere
   */
  const removeQuiz = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      const success = await deleteQuizService(id)
      
      if (success) {
        const index = quizzes.value.findIndex(q => q.id === id)
        if (index !== -1) {
          quizzes.value.splice(index, 1)
        }
      } else {
        throw new Error('Quiz non trovato')
      }
      
      return success
    } catch (err) {
      error.value = 'Errore nell\'eliminazione del quiz'
      console.error('Errore removeQuiz:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Recupera un singolo quiz per ID (dal service)
   * @param id - L'ID del quiz da recuperare
   */
  const fetchQuizById = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      const quiz = await getQuizByIdService(id)
      
      if (quiz) {
        // Aggiorna anche nello state se esiste
        const existingIndex = quizzes.value.findIndex(q => q.id === id)
        if (existingIndex !== -1) {
          quizzes.value[existingIndex] = quiz
        } else {
          quizzes.value.push(quiz)
        }
      }
      
      return quiz
    } catch (err) {
      error.value = 'Errore nel caricamento del quiz'
      console.error('Errore fetchQuizById:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Aggiorna un quiz esistente
   * @param id - L'ID del quiz da aggiornare
   * @param updatedData - I dati aggiornati
   */
  const updateQuiz = async (id: string, updatedData: Partial<Quiz>) => {
    loading.value = true
    error.value = null
    try {
      const updatedQuiz = await updateQuizService(id, updatedData)
      
      if (updatedQuiz) {
        const index = quizzes.value.findIndex(q => q.id === id)
        if (index !== -1) {
          quizzes.value[index] = updatedQuiz
        }
      }
      
      return updatedQuiz
    } catch (err) {
      error.value = 'Errore nell\'aggiornamento del quiz'
      console.error('Errore updateQuiz:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Reset dello stato di errore
   */
  const clearError = () => {
    error.value = null
  }

  return { 
    // State
    quizzes, 
    loading, 
    error,
    
    // Computed
    totalQuizzes,
    getQuizById,
    
    // Actions
    fetchQuizzes,
    createQuiz,
    removeQuiz,
    fetchQuizById,
    updateQuiz,
    clearError
  }
})