import type { Quiz } from '@/types/quiz';
import quizData from '../../quiz-it.json';

/**
 * Database in memoria per i quiz creati
 */
let quizzesInMemory: Quiz[] = [...(quizData as Quiz[])];

/**
 * Funzione helper per creare un delay
 * @param ms - millisecondi di attesa
 */
const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Recupera tutti i quiz dal database in memoria con un delay di 1 secondo
 * @returns Promise che risolve con un array di Quiz
 */
export const getAllQuiz = async (): Promise<Quiz[]> => {
  // Delay di 1 secondo per simulare chiamata API
  await delay(1000);
  
  // Restituisce una copia dei dati
  return [...quizzesInMemory];
};

/**
 * Crea un nuovo quiz e lo salva nel database in memoria
 * @param quiz - Il quiz da creare
 * @returns Promise che risolve con il quiz creato
 */
export const createQuiz = async (quiz: Quiz): Promise<Quiz> => {
  // Delay di 800ms per simulare chiamata API
  await delay(800);
  
  // Verifica che il quiz non esista già
  const exists = quizzesInMemory.some(q => q.id === quiz.id);
  if (exists) {
    // Se esiste, aggiorna invece di creare
    const index = quizzesInMemory.findIndex(q => q.id === quiz.id);
    quizzesInMemory[index] = { ...quiz };
    return { ...quiz };
  }
  
  // Aggiungi il nuovo quiz al database
  const newQuiz = { ...quiz };
  quizzesInMemory.push(newQuiz);
  
  return newQuiz;
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

