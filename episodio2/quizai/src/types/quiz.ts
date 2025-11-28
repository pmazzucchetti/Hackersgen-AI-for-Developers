export interface Opzione {
  id: string;
  testo: string;
  corretta: boolean; // true se questa opzione è corretta
}

export interface Domanda {
  id: string;
  testo: string;
  opzioni: Opzione[];
}

export interface Quiz {
  id: string;
  titolo: string;
  domande: Domanda[];
}


