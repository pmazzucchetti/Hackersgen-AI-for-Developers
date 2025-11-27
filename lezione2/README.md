# Guida Completa: Creare un'App Vue da Zero con l'AI

Questa guida ti accompagnerà nella creazione di un'applicazione Vue.js **sfruttando l'intelligenza artificiale** come assistente di sviluppo.

## 🎯 Focus di Questa Lezione

**Non stai solo imparando Vue.js - stai imparando a usare l'AI per sviluppare più velocemente.**

In questa lezione vedrai:
- Come l'AI può generare componenti Vue in secondi
- Come usare Cursor per scrivere meno codice manualmente
- Come far spiegare all'AI concetti Vue complessi
- Come debuggare errori con l'aiuto dell'AI
- Quando accettare i suggerimenti dell'AI e quando modificarli

**Ricorda**: L'app quiz è solo un pretesto per vedere l'AI all'opera!

## Prerequisiti

Prima di iniziare, assicurati di avere installato sul tuo computer:

- **Node.js** (versione 16 o superiore): [Scarica qui](https://nodejs.org/)
- **npm** (viene installato automaticamente con Node.js)

Per verificare se hai già installato questi strumenti, apri il terminale e digita:

```bash
node --version
npm --version
```

Se vedi i numeri di versione, sei pronto per iniziare!

## 🤖 Usare Cursor come Assistente AI

**Cursor** è il nostro strumento principale. È un editor di codice con AI integrata che ti aiuterà durante tutto lo sviluppo.

### Come Funziona Cursor

1. **Cmd/Ctrl + K**: Apre il prompt AI per modificare il codice
2. **Cmd/Ctrl + L**: Apre la chat AI per fare domande
3. **Tab**: Accetta i suggerimenti dell'AI
4. **Esc**: Rifiuta i suggerimenti

### Esempi di Prompt Utili per Vue

Durante questa lezione, potrai chiedere a Cursor:

**Per imparare concetti:**
- "Spiegami cosa fa `<script setup>` in Vue 3"
- "Qual è la differenza tra ref e reactive?"
- "Come funziona il ciclo di vita dei componenti Vue?"

**Per generare codice:**
- "Crea un componente Vue che mostra una lista di quiz"
- "Aggiungi uno stato reattivo per tracciare il quiz selezionato"
- "Crea una funzione che filtra i quiz per categoria"

**Per debugging:**
- "Perché questo componente non si aggiorna quando cambio i dati?"
- "Come posso risolvere questo errore: [copia errore]"

### ⚠️ Regola d'Oro

**Leggi e capisci sempre il codice generato dall'AI prima di usarlo!**

Non copiare ciecamente - usa l'AI per imparare più velocemente.

## Creazione del Progetto

Esistono due metodi principali per creare un progetto Vue. Ti consigliamo **Vite** perché è più veloce e moderno.

### Metodo 1: Con Vite (Consigliato)

1. Apri il terminale nella cartella dove vuoi creare il progetto

2. Esegui il comando:
```bash
npm create vue@latest
```

3. Ti verranno fatte alcune domande. Ecco le risposte consigliate per iniziare:
   - **Project name**: il nome del tuo progetto (es. `my-vue-app`)
   - **Add TypeScript?**: Yes
   - **Add JSX Support?**: No
   - **Add Vue Router?**: Yes (se vuoi creare più pagine)
   - **Add Pinia?**: Yes (per gestire lo stato dell'app)
   - **Add Vitest?**: No (per ora)
   - **Add ESLint?**: Yes (per mantenere il codice pulito)
   - **Add Prettier?**: Yes (per formattare il codice)

4. Entra nella cartella del progetto:
```bash
cd my-vue-app
```

5. Installa le dipendenze:
```bash
npm install
```

### Metodo 2: Con Vue CLI

1. Installa Vue CLI globalmente (solo la prima volta):
```bash
npm install -g @vue/cli
```

2. Crea il progetto:
```bash
vue create my-vue-app
```

3. Seleziona "Default" per una configurazione base, oppure "Manually select features" per personalizzare

4. Entra nella cartella del progetto:
```bash
cd my-vue-app
```

## Struttura del Progetto

Dopo la creazione, troverai questa struttura di cartelle:

```
my-vue-app/
├── node_modules/      # Librerie e dipendenze (non modificare)
├── public/            # File statici pubblici
├── src/               # Il tuo codice sorgente
│   ├── assets/        # Immagini, CSS, etc.
│   ├── components/    # Componenti Vue riutilizzabili
│   ├── App.vue        # Componente principale
│   └── main.js        # Punto di ingresso dell'app
├── index.html         # File HTML principale
├── package.json       # Configurazione del progetto
└── vite.config.js     # Configurazione di Vite
```

## Avviare l'Applicazione

Per avviare il server di sviluppo e vedere la tua app in azione:

```bash
npm run dev
```

Il terminale mostrerà un messaggio simile a:

```
VITE v5.x.x  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

Apri il browser e vai all'indirizzo indicato (solitamente `http://localhost:5173/`). Vedrai la tua app Vue in esecuzione!

## Comandi Principali

- **Avviare il server di sviluppo**:
  ```bash
  npm run dev
  ```

- **Creare una build di produzione**:
  ```bash
  npm run build
  ```
  Questo comando crea una versione ottimizzata dell'app nella cartella `dist/`

- **Visualizzare la build di produzione**:
  ```bash
  npm run preview
  ```

- **Formattare il codice**:
  ```bash
  npm run format
  ```

- **Controllare errori di sintassi**:
  ```bash
  npm run lint
  ```

## Modificare l'Applicazione

Per iniziare a personalizzare la tua app:

1. Apri il file `src/App.vue` con il tuo editor di codice preferito

2. Modifica il template HTML all'interno del tag `<template>`

3. Salva il file

4. Il browser si aggiornerà automaticamente mostrando le modifiche (hot reload)

### Esempio di Modifica

Apri `src/App.vue` e sostituisci il contenuto con:

```vue
<template>
  <div id="app">
    <h1>La Mia Prima App Vue!</h1>
    <p>Messaggio: {{ messaggio }}</p>
    <button @click="cambiaMessaggio">Clicca qui</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messaggio: 'Ciao Vue!'
    }
  },
  methods: {
    cambiaMessaggio() {
      this.messaggio = 'Hai cliccato il bottone!'
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
```

## Creare Nuovi Componenti

1. Crea un nuovo file nella cartella `src/components/`, ad esempio `MioComponente.vue`

2. Scrivi la struttura del componente:

```vue
<template>
  <div class="mio-componente">
    <h2>{{ titolo }}</h2>
  </div>
</template>

<script>
export default {
  name: 'MioComponente',
  props: {
    titolo: String
  }
}
</script>

<style scoped>
.mio-componente {
  padding: 20px;
  border: 1px solid #ccc;
}
</style>
```

3. Importa e usa il componente in `App.vue`:

```vue
<script>
import MioComponente from './components/MioComponente.vue'

export default {
  components: {
    MioComponente
  }
}
</script>

<template>
  <MioComponente titolo="Benvenuto!" />
</template>
```

## 🤖 Sviluppare con l'AI: Esempi Pratici

Ora vediamo come usare l'AI per accelerare lo sviluppo. **Questi esempi ti mostrano il vero valore del corso!**

### Esempio 1: Creare un Componente con Cursor

Invece di scrivere tutto il codice manualmente, puoi:

1. Crea un file vuoto `QuizCard.vue` in `src/components/`
2. Premi **Cmd/Ctrl + K** in Cursor
3. Scrivi il prompt:
   ```
   Crea un componente Vue che mostra una card di un quiz con titolo,
   descrizione e numero di domande. Usa props per passare i dati.
   ```
4. **Leggi il codice generato** - capisci cosa fa ogni parte
5. **Modifica se necessario** - l'AI è un punto di partenza, non la soluzione finale

### Esempio 2: Far Spiegare Concetti

Stai leggendo codice Vue e vedi qualcosa che non capisci?

1. Seleziona il codice
2. Premi **Cmd/Ctrl + L** per aprire la chat
3. Chiedi: "Spiegami questo codice come se avessi 15 anni"
4. L'AI ti darà una spiegazione semplice

**Esempio pratico:**
```vue
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>
```

Chiedi a Cursor: "Qual è la differenza tra ref e computed in questo esempio?"

### Esempio 3: Debugging Intelligente

Hai un errore? Niente panico!

1. **Copia l'errore completo** dal terminale o dal browser
2. Apri la chat di Cursor (Cmd/Ctrl + L)
3. Scrivi:
   ```
   Ho questo errore:
   [incolla errore]

   Stavo facendo:
   [spiega cosa stavi facendo]

   Aiutami a capire il problema e come risolverlo.
   ```

4. **Analizza la risposta** - non copiare subito la soluzione!
5. **Capisci perché** si è verificato l'errore
6. **Applica la soluzione** e verifica che funzioni

### Esempio 4: Refactoring con AI

Hai scritto codice che funziona ma è ripetitivo? L'AI può aiutarti!

```vue
<!-- Codice ripetitivo -->
<template>
  <div>
    <button @click="answer1">Risposta 1</button>
    <button @click="answer2">Risposta 2</button>
    <button @click="answer3">Risposta 3</button>
    <button @click="answer4">Risposta 4</button>
  </div>
</template>
```

Seleziona il codice, Cmd/Ctrl + K, e chiedi:
```
Refactorizza questo codice usando un v-for per evitare ripetizioni
```

### 💡 Consigli per Prompt Efficaci

**Buoni prompt:**
- Sii specifico: "Crea un form di login con validazione email"
- Dai contesto: "Nel mio componente Vue che gestisce quiz..."
- Chiedi spiegazioni: "Spiega perché usi v-model qui"

**Cattivi prompt:**
- Troppo vago: "Crea qualcosa"
- Senza contesto: "Aggiusta l'errore" (quale errore?)
- Solo codice senza capire: "Scrivi tutto il codice dell'app"

### ⚠️ Importante: Verifica Sempre!

L'AI può sbagliare! Controlla sempre:
- Il codice funziona davvero?
- È sicuro? (niente vulnerabilità XSS, injection, etc.)
- È efficiente? (niente loop infiniti, troppi re-render)
- Lo capisci? Se no, chiedi spiegazioni!

## Risolvere Problemi Comuni

### Consiglio Generale

**Leggi sempre attentamente i messaggi di errore!** Gli errori in JavaScript e nei tool di sviluppo sono generalmente molto parlanti e indicano chiaramente cosa non va.

Se non riesci a capire l'errore:
- **Copia l'errore completo** e incollalo su Google - troverai quasi sempre qualcuno che ha avuto lo stesso problema
- Usa **ChatGPT o altri assistenti AI** - incolla l'errore e chiedi una spiegazione e una soluzione
- Cerca su **Stack Overflow** - è pieno di soluzioni a problemi comuni

La maggior parte dei problemi che incontrerai sono già stati risolti da altri sviluppatori!

### Il server non parte

- Verifica che la porta non sia già in uso
- Prova a eliminare la cartella `node_modules` e il file `package-lock.json`, poi esegui `npm install` di nuovo

### Errori durante l'installazione

- Assicurati di avere una versione aggiornata di Node.js
- Prova a pulire la cache di npm: `npm cache clean --force`

### Le modifiche non si vedono nel browser

- Assicurati di aver salvato il file
- Ricarica la pagina manualmente con Ctrl+R (o Cmd+R su Mac)
- Riavvia il server di sviluppo

### Errore "running scripts is disabled" su Windows (PowerShell)

Se su Windows ricevi questo errore: `File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system`, segui questi passaggi:

1. **Apri PowerShell come Amministratore**
   - Cerca "PowerShell" nel menu Start
   - Fai clic destro su "Windows PowerShell"
   - Seleziona "Esegui come amministratore"

2. **Verifica la policy corrente** (opzionale):
   ```powershell
   Get-ExecutionPolicy
   ```
   Se restituisce "Restricted", è necessario modificarla.

3. **Modifica la policy di esecuzione**:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```
   Conferma digitando `Y` quando richiesto.

4. **Verifica la modifica** (opzionale):
   ```powershell
   Get-ExecutionPolicy -List
   ```
   Dovresti vedere "CurrentUser" impostato su "RemoteSigned".

Dopo questi passaggi, i comandi npm dovrebbero funzionare correttamente. L'impostazione "RemoteSigned" è un buon compromesso tra sicurezza e funzionalità.

## Risorse Utili

- [Documentazione Ufficiale Vue.js](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/) - Per gestire le rotte
- [Pinia](https://pinia.vuejs.org/) - Per gestire lo stato globale
- [Vite Documentation](https://vitejs.dev/) - Documentazione di Vite

## Prossimi Passi

Ora che hai imparato a usare l'AI con Vue, puoi:

1. **Sperimentare con Cursor**: Prova a creare componenti complessi con l'aiuto dell'AI
2. **Passare alla Lezione 3**: Impara a usare l'AI per creare il backend Flask
3. **Esplorare Vue + AI**: Chiedi all'AI di spiegarti Vue Router, Pinia, Composition API
4. **Costruire qualcosa di tuo**: Usa quello che hai imparato per creare un progetto personale
5. **Confrontare approcci**: Prova a scrivere codice manualmente e con l'AI - quando è meglio uno o l'altro?

**Ricorda**: L'obiettivo non è solo costruire app, ma imparare a usare l'AI come strumento di potenziamento delle tue abilità.

Buon coding con l'AI! 🚀🤖
