# Guida Completa: Creare un'App Vue da Zero

Questa guida ti accompagnerà passo dopo passo nella creazione e nell'esecuzione di un'applicazione Vue.js.

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
   - **Add TypeScript?**: No (per ora)
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

## Risolvere Problemi Comuni

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

## Risorse Utili

- [Documentazione Ufficiale Vue.js](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/) - Per gestire le rotte
- [Pinia](https://pinia.vuejs.org/) - Per gestire lo stato globale
- [Vite Documentation](https://vitejs.dev/) - Documentazione di Vite

## Prossimi Passi

Ora che hai creato la tua prima app Vue, puoi:

1. Esplorare i componenti Vue e creare componenti personalizzati
2. Aggiungere Vue Router per creare un'app multi-pagina
3. Utilizzare Pinia per gestire lo stato dell'applicazione
4. Integrare API esterne per recuperare dati
5. Esplorare librerie di componenti UI come Vuetify o Element Plus

Buon coding! 🚀
