# Quiz Creator System - Documentazione

## 📋 Panoramica

Il sistema Quiz Creator è una soluzione completa per la creazione, gestione e visualizzazione di quiz interattivi. È stato costruito con Vue 3, TypeScript, Pinia per la gestione dello stato e include un sistema di service layer che simula chiamate API REST.

## 🏗️ Architettura

### 1. **Componenti Vue**

#### `QuizForm.vue`
Componente principale per la creazione e modifica dei quiz.

**Funzionalità:**
- ✅ Aggiunta/rimozione dinamica di domande
- ✅ Aggiunta/rimozione dinamica di opzioni per ogni domanda
- ✅ Selezione della risposta corretta tramite radio button
- ✅ Validazione completa di tutti i campi
- ✅ Gestione degli errori con messaggi user-friendly
- ✅ UI responsive e moderna
- ✅ Messaggi di successo dopo il salvataggio

**Props:**
```typescript
interface Props {
  initialQuiz?: Quiz  // Opzionale, per modalità editing
}
```

**Eventi emessi:**
```typescript
emit('success', quiz: Quiz)  // Quando il quiz viene salvato con successo
emit('cancel')               // Quando l'utente annulla
```

**Utilizzo:**
```vue
<QuizForm 
  @success="handleSuccess"
  @cancel="handleCancel"
/>
```

#### `QuizCreatorPage.vue`
Pagina completa che integra il `QuizForm` con funzionalità aggiuntive.

**Funzionalità:**
- 📝 Visualizza il form per creare nuovi quiz
- 📊 Lista di tutti i quiz creati con anteprima
- 🗑️ Eliminazione quiz con modal di conferma
- 👁️ Visualizzazione dettagli quiz
- 🔔 Sistema di notifiche toast
- ↩️ Navigazione back alla home

### 2. **Pinia Store** (`stores/quiz.ts`)

Store centralizzato per la gestione dello stato dei quiz.

#### State
```typescript
{
  quizzes: Quiz[],      // Array di tutti i quiz
  loading: boolean,     // Stato di caricamento
  error: string | null  // Messaggio di errore
}
```

#### Computed
- `totalQuizzes`: Numero totale di quiz
- `getQuizById`: Funzione per trovare un quiz per ID

#### Actions

##### `fetchQuizzes()`
Recupera tutti i quiz dal service layer.
```typescript
await quizStore.fetchQuizzes()
```

##### `createQuiz(quizData: Quiz)`
Crea un nuovo quiz o aggiorna uno esistente.
```typescript
const newQuiz = await quizStore.createQuiz({
  id: '123',
  titolo: 'Il mio quiz',
  domande: [...]
})
```

##### `removeQuiz(id: string)`
Rimuove un quiz per ID.
```typescript
await quizStore.removeQuiz('123')
```

##### `fetchQuizById(id: string)`
Recupera un singolo quiz per ID.
```typescript
const quiz = await quizStore.fetchQuizById('123')
```

##### `updateQuiz(id: string, updatedData: Partial<Quiz>)`
Aggiorna un quiz esistente.
```typescript
await quizStore.updateQuiz('123', { titolo: 'Nuovo titolo' })
```

##### `clearError()`
Reset del messaggio di errore.
```typescript
quizStore.clearError()
```

### 3. **Service Layer** (`service/quiz.ts`)

Simula una REST API con un database in memoria.

#### Caratteristiche
- 💾 Database in memoria (array)
- ⏱️ Simulazione ritardi realistici
- 🔄 Gestione completa CRUD
- 📦 Promise-based

#### Funzioni disponibili

##### `getAllQuiz(): Promise<Quiz[]>`
Recupera tutti i quiz (delay: 1000ms)
```typescript
const quizzes = await getAllQuiz()
```

##### `createQuiz(quiz: Quiz): Promise<Quiz>`
Crea un nuovo quiz o aggiorna uno esistente (delay: 800ms)
```typescript
const newQuiz = await createQuiz({
  id: '123',
  titolo: 'Quiz di Storia',
  domande: [...]
})
```

##### `deleteQuiz(id: string): Promise<boolean>`
Elimina un quiz (delay: 500ms)
```typescript
const success = await deleteQuiz('123')
```

##### `getQuizById(id: string): Promise<Quiz | undefined>`
Recupera un singolo quiz (delay: 500ms)
```typescript
const quiz = await getQuizById('123')
```

##### `updateQuiz(id: string, updatedQuiz: Partial<Quiz>): Promise<Quiz | undefined>`
Aggiorna un quiz esistente (delay: 800ms)
```typescript
const updated = await updateQuiz('123', { titolo: 'Nuovo titolo' })
```

### 4. **Type Definitions** (`types/quiz.ts`)

```typescript
interface Opzione {
  id: string
  testo: string
  corretta: boolean
}

interface Domanda {
  id: string
  testo: string
  opzioni: Opzione[]
}

interface Quiz {
  id: string
  titolo: string
  domande: Domanda[]
}
```

## 🚀 Come Usare

### 1. Navigazione
Dalla homepage, clicca sul pulsante **"➕ Crea Nuovo Quiz"** per accedere al creator.

### 2. Creazione Quiz

#### Passo 1: Titolo
Inserisci il titolo del quiz nel primo campo.

#### Passo 2: Aggiungere Domande
1. Per default viene creata una domanda vuota
2. Clicca **"+ Aggiungi Domanda"** per aggiungere più domande
3. Clicca **"Rimuovi"** per eliminare una domanda (minimo 1 richiesta)

#### Passo 3: Aggiungere Opzioni
1. Ogni domanda parte con 2 opzioni
2. Clicca **"+ Aggiungi Opzione"** per aggiungerne altre
3. Clicca **"×"** per rimuovere un'opzione (minimo 2 richieste)

#### Passo 4: Selezionare Risposta Corretta
Usa i radio button per indicare quale opzione è corretta (una per domanda).

#### Passo 5: Salvare
Clicca **"Salva Quiz"** per creare il quiz.

### 3. Gestione Quiz
Dopo aver creato dei quiz, verranno visualizzati nella lista:
- **Visualizza**: Vai alla pagina del quiz
- **Elimina**: Rimuovi il quiz (con conferma)

## ✅ Validazione

Il sistema valida:
- ✓ Titolo non vuoto
- ✓ Almeno una domanda
- ✓ Testo domanda non vuoto
- ✓ Almeno 2 opzioni per domanda
- ✓ Almeno una risposta corretta selezionata
- ✓ Testo opzioni non vuoto

## 🎨 Styling

Il sistema include:
- Design moderno e pulito
- Animazioni fluide
- Responsive design (mobile-friendly)
- Feedback visivo per azioni utente
- Notifiche toast
- Modal di conferma

## 🔄 Flusso dei Dati

```
QuizForm (UI)
    ↓
quizStore.createQuiz() (Pinia Action)
    ↓
createQuiz() (Service Layer)
    ↓
Database in memoria (Array)
    ↓
Return & Update State
    ↓
UI Aggiornata
```

## 📝 Esempio Completo

```vue
<template>
  <QuizCreatorPage />
</template>

<script setup lang="ts">
import QuizCreatorPage from '@/views/QuizCreatorPage.vue'
</script>
```

## 🔧 Personalizzazione

### Modificare i Delay
Modifica i valori in `service/quiz.ts`:
```typescript
await delay(1000)  // Cambia questo valore
```

### Aggiungere Nuovi Campi
1. Aggiorna `types/quiz.ts`
2. Modifica `QuizForm.vue` per includere il campo
3. Aggiorna la validazione

### Modificare gli Stili
I componenti usano scoped CSS. Modifica le sezioni `<style scoped>` nei file `.vue`.

## 🐛 Debug

Per debuggare:
1. Usa Vue DevTools per ispezionare lo store Pinia
2. Controlla la console per errori
3. Verifica il database in memoria: `quizzesInMemory` in `service/quiz.ts`

## 📱 Responsive Design

Il sistema è completamente responsive:
- Desktop: Grid multi-colonna
- Tablet: Layout adattivo
- Mobile: Single column, touch-friendly

## 🚦 Stati del Sistema

### Loading
Mostra spinner durante operazioni asincrone.

### Error
Messaggi di errore specifici per ogni operazione.

### Success
Notifiche toast per operazioni completate.

## 🎯 Best Practices

1. **Validazione**: Sempre validare prima di submit
2. **Error Handling**: Usa try-catch per operazioni async
3. **User Feedback**: Mostra loading states e notifiche
4. **ID Unici**: Usa la funzione `generateId()` per ID univoci
5. **Immutabilità**: Lo store Pinia gestisce lo stato in modo reattivo

## 📦 Struttura File

```
src/
├── components/
│   └── QuizForm.vue           # Form principale
├── views/
│   ├── HomeView.vue           # Homepage (aggiornata)
│   ├── QuizCreatorPage.vue    # Pagina creator
│   └── QuizView.vue           # Visualizzazione quiz
├── stores/
│   └── quiz.ts                # Pinia store (esteso)
├── service/
│   └── quiz.ts                # Service layer (esteso)
├── types/
│   └── quiz.ts                # Type definitions
└── router/
    └── index.ts               # Routes (aggiornato)
```

## 🔗 Routes

```typescript
{
  path: '/',
  name: 'home',
  component: HomeView
}
{
  path: '/create',
  name: 'create-quiz',
  component: QuizCreatorPage
}
{
  path: '/quiz/:id',
  name: 'quiz',
  component: QuizView
}
```

## 🎓 Conclusione

Il sistema Quiz Creator è completo, modulare e pronto per l'uso in produzione. Può essere facilmente esteso per includere:
- Backend reale
- Autenticazione utente
- Condivisione quiz
- Statistiche e analytics
- Categorie e tag
- E molto altro!

