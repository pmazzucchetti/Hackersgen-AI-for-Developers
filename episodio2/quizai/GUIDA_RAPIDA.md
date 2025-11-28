# 🚀 Guida Rapida - Quiz Creator

## ✨ Cosa è stato creato

È stato implementato un sistema completo per creare e gestire quiz, composto da:

### 📁 File Creati/Modificati

1. **`src/components/QuizForm.vue`** ✨ NUOVO
   - Componente form completo per creare quiz
   - Gestione dinamica domande e opzioni
   - Validazione completa

2. **`src/views/QuizCreatorPage.vue`** ✨ NUOVO
   - Pagina completa con form integrato
   - Lista quiz creati
   - Sistema di eliminazione con conferma

3. **`src/service/quiz.ts`** 🔄 ESTESO
   - Aggiunto database in memoria
   - Funzioni: `createQuiz()`, `deleteQuiz()`, `getQuizById()`, `updateQuiz()`
   - Simulazione ritardi API

4. **`src/stores/quiz.ts`** 🔄 ESTESO
   - Actions: `createQuiz()`, `removeQuiz()`, `updateQuiz()`
   - State management completo
   - Gestione loading ed errori

5. **`src/views/HomeView.vue`** 🔄 AGGIORNATO
   - Aggiunto pulsante "Crea Nuovo Quiz"

6. **`src/router/index.ts`** 🔄 AGGIORNATO
   - Aggiunta route `/create`

## 🎯 Come Iniziare

### 1. Avvia l'applicazione
```bash
npm run dev
```

### 2. Naviga su `/create` o clicca "Crea Nuovo Quiz" dalla home

### 3. Crea il tuo primo quiz!

## 💡 Funzionalità Principali

### ✅ Nel Form
- **Titolo Quiz**: Campo obbligatorio
- **Domande**: Minimo 1, aggiungi/rimuovi liberamente
- **Opzioni**: Minimo 2 per domanda
- **Risposta Corretta**: Seleziona con radio button
- **Validazione**: Automatica con messaggi di errore
- **Submit**: Salva nel database in memoria

### ✅ Nella Pagina Creator
- **Lista Quiz**: Visualizza tutti i quiz creati
- **Anteprima**: Vedi domande e opzioni
- **Elimina**: Con modal di conferma
- **Visualizza**: Vai al quiz completo
- **Notifiche**: Toast per successo/errore

## 📋 Esempio di Utilizzo

### Creare un Quiz Programmaticamente

```typescript
import { useQuizStore } from '@/stores/quiz'

const quizStore = useQuizStore()

// Crea un nuovo quiz
await quizStore.createQuiz({
  id: 'quiz-123',
  titolo: 'Quiz di JavaScript',
  domande: [
    {
      id: 'q1',
      testo: 'Cos\'è JavaScript?',
      opzioni: [
        { id: 'o1', testo: 'Un linguaggio di programmazione', corretta: true },
        { id: 'o2', testo: 'Un caffè', corretta: false }
      ]
    }
  ]
})
```

### Recuperare tutti i Quiz

```typescript
// Carica tutti i quiz
await quizStore.fetchQuizzes()

// Accedi ai quiz
console.log(quizStore.quizzes)
console.log(quizStore.totalQuizzes) // computed
```

### Eliminare un Quiz

```typescript
await quizStore.removeQuiz('quiz-123')
```

## 🎨 Personalizzazione

### Cambiare i Colori
Modifica i file `.vue` nella sezione `<style scoped>`:
- Primary: `#42b983` (verde)
- Secondary: `#667eea` (viola)
- Error: `#dc3545` (rosso)

### Modificare i Delay API
In `src/service/quiz.ts`:
```typescript
await delay(1000) // Cambia il valore in millisecondi
```

### Aggiungere Campi Custom
1. Aggiungi il campo in `src/types/quiz.ts`
2. Modifica `QuizForm.vue` per includere l'input
3. Aggiorna la validazione

## 🔍 Validazione

Il form valida automaticamente:
- ✓ Titolo non vuoto
- ✓ Almeno 1 domanda
- ✓ Testo domanda non vuoto
- ✓ Almeno 2 opzioni per domanda
- ✓ Almeno 1 risposta corretta
- ✓ Testo opzioni non vuoto

## 🐛 Troubleshooting

### Il quiz non viene salvato
- Controlla la console per errori
- Verifica che tutti i campi siano compilati
- Assicurati di aver selezionato una risposta corretta

### Errori di validazione
- Leggi i messaggi di errore rossi sotto i campi
- Ogni campo ha indicazioni specifiche

### Quiz non appare nella lista
- Ricarica la pagina
- Controlla che `fetchQuizzes()` sia stato chiamato

## 📱 Responsive

Il sistema funziona perfettamente su:
- 🖥️ Desktop (1200px+)
- 💻 Laptop (768px - 1200px)
- 📱 Tablet (480px - 768px)
- 📱 Mobile (< 480px)

## 🚀 Pronto per l'Uso

Il codice è:
- ✅ Completo e funzionante
- ✅ Type-safe (TypeScript)
- ✅ Ben strutturato (architettura a layer)
- ✅ Documentato
- ✅ Responsive
- ✅ Pronto da incollare nel progetto

## 📞 Struttura delle Routes

```
/ (home)
  └── Visualizza tutti i quiz + pulsante "Crea Nuovo Quiz"

/create
  └── Form per creare quiz + lista quiz esistenti

/quiz/:id
  └── Visualizza e svolgi il quiz
```

## 🎓 Best Practices Implementate

1. **Separation of Concerns**: UI → Store → Service
2. **Type Safety**: TypeScript ovunque
3. **Reactive State**: Pinia per gestione stato
4. **User Feedback**: Loading, errori, successo
5. **Validation**: Completa e user-friendly
6. **Clean Code**: Commentato e ben organizzato

## 🎉 Inizia Subito!

Tutto è pronto. Basta:
1. Avviare l'app
2. Cliccare "Crea Nuovo Quiz"
3. Compilare il form
4. Vedere il quiz nella lista!

---

**Nota**: Il database è in memoria, quindi i quiz creati verranno persi al reload della pagina (a meno che non siano nel file `quiz-it.json` iniziale). Per persistenza reale, implementa un backend.

