import type { Quiz } from '@/types/quiz';

const API_BASE_URL = 'http://127.0.0.1:5000';

/**
 * Cache in memoria per i quiz (sincronizzata con il backend)
 */
let quizzesInMemory: Quiz[] = [];

/**
 * Funzione helper per creare un delay
 * @param ms - millisecondi di attesa
 */
const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Recupera tutti i quiz dal backend
 * @returns Promise che risolve con un array di Quiz
 */
export const getAllQuiz = async (): Promise<Quiz[]> => {
  const response = await fetch(`${API_BASE_URL}/api/quiz`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error('Errore durante il recupero dei quiz');
  }

  const quizzes = await response.json();

  // Aggiorna la cache in memoria con i dati del backend
  quizzesInMemory = [...quizzes];

  return quizzes;
};

/**
 * Crea un nuovo quiz e lo salva nel database in memoria
 * @param quiz - Il quiz da creare
 * @returns Promise che risolve con il quiz creato
 */
export const createQuiz = async (quiz: Quiz): Promise<Quiz> => {
  const response = await fetch(`${API_BASE_URL}/api/quiz`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(quiz)
  });

  if (!response.ok) {
    throw new Error('Errore durante la creazione del quiz');
  }

  // Il backend risponde con un messaggio e l'ID del quiz,
  // ma per coerenza con la funzione originale, restituiamo l'oggetto quiz completo.
  // In un'applicazione reale, la risposta del backend potrebbe essere più completa.
  const result = await response.json();
  console.log('Quiz salvato con successo:', result);

  // Dato che il backend non restituisce il quiz completo,
  // lo aggiungiamo manualmente alla nostra cache in memoria per mantenere la UI aggiornata.
  quizzesInMemory.push(quiz);

  return quiz;
};

/**
 * Elimina un quiz dal database in memoria
 * @param id - L'ID del quiz da eliminare
 * @returns Promise che risolve con true se eliminato, false altrimenti
 */
export const deleteQuiz = async (id: string): Promise<boolean> => {
  // Delay di 500ms per simulare chiamata API
  await delay(500);
  
  const index = quizzesInMemory.findIndex(q => q.id === id);
  
  if (index === -1) {
    return false;
  }
  
  quizzesInMemory.splice(index, 1);
  return true;
};

/**
 * Recupera un singolo quiz per ID
 * @param id - L'ID del quiz da recuperare
 * @returns Promise che risolve con il quiz o undefined se non trovato
 */
export const getQuizById = async (id: string): Promise<Quiz | undefined> => {
  // Delay di 500ms per simulare chiamata API
  await delay(500);
  
  const quiz = quizzesInMemory.find(q => q.id === id);
  return quiz ? { ...quiz } : undefined;
};

/**
 * Aggiorna un quiz esistente
 * @param id - L'ID del quiz da aggiornare
 * @param updatedQuiz - I dati aggiornati del quiz
 * @returns Promise che risolve con il quiz aggiornato o undefined se non trovato
 */
export const updateQuiz = async (id: string, updatedQuiz: Partial<Quiz>): Promise<Quiz | undefined> => {
  // Delay di 800ms per simulare chiamata API
  await delay(800);
  
  const index = quizzesInMemory.findIndex(q => q.id === id);
  
  if (index === -1) {
    return undefined;
  }
  
  quizzesInMemory[index] = { ...quizzesInMemory[index], ...updatedQuiz } as Quiz;
  return { ...quizzesInMemory[index] } as Quiz;
};

