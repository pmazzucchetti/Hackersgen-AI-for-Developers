from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import uuid
import requests   

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route("/api/quiz", methods=['GET'])
def get_quizzes():
    # Leggi i quiz dal file

    with open('data.json', 'r') as f:
        quizzes = json.load(f)

    # Assicurati che quizzes sia una lista di quiz validi
    valid_quizzes = []
    for item in quizzes:
        if isinstance(item, dict):
            valid_quizzes.append(item)
        elif isinstance(item, list):
            valid_quizzes.extend(item)

    return jsonify(valid_quizzes), 200


@app.route("/api/quiz", methods=['POST'])
def save_quiz():
    # Carica i nuovi dati dal corpo della richiesta
    new_data = request.json

    # Leggi i quiz esistenti dal file
    with open('data.json', 'r') as f:
        quizzes = json.load(f)

    returned_id = None
    if isinstance(new_data, dict):
        # Aggiungi un singolo quiz
        quizzes.append(new_data)
        returned_id = new_data.get("id")
    elif isinstance(new_data, list):
        # Aggiungi una lista di quiz
        quizzes.extend(new_data)
        if new_data:
            returned_id = new_data[0].get("id")  # Ritorna l'ID del primo quiz della lista
    else:
        return jsonify({
                           "error": "Dati non validi. Il corpo della richiesta deve essere un oggetto JSON o una lista di oggetti."}), 400

    # Salva la lista aggiornata nel file
    with open('data.json', 'w') as f:
        json.dump(quizzes, f, indent=2)

    return jsonify({"message": "Quiz salvati con successo!", "quiz_id": returned_id}), 201


@app.route("/api/generate-quiz", methods=['POST'])
def generate_quiz():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "Dati mancanti"}), 400
        
        tema = data.get('tema')
        difficolta = data.get('difficolta')
        numero_domande = data.get('numeroDomande')
        
        if not tema or not difficolta or not numero_domande:
            return jsonify({"error": "Parametri mancanti: tema, difficolta e numeroDomande sono obbligatori"}), 400
        
        # Valida difficoltà
        if difficolta not in ['facile', 'medio', 'difficile']:
            return jsonify({"error": "Difficoltà non valida. Valori accettati: facile, medio, difficile"}), 400
        
        # Valida numero domande
        if not isinstance(numero_domande, int) or numero_domande < 1 or numero_domande > 10:
            return jsonify({"error": "Numero domande deve essere un intero tra 1 e 10"}), 400
        
        # Crea lo schema JSON dettagliato per il prompt
        schema_json = {
            "id": "string (ID univoco del quiz)",
            "titolo": "string (titolo del quiz)",
            "domande": [
                {
                    "id": "string (ID univoco della domanda)",
                    "testo": "string (testo della domanda)",
                    "opzioni": [
                        {
                            "id": "string (ID univoco dell'opzione)",
                            "testo": "string (testo dell'opzione di risposta)",
                            "corretta": "boolean (true se questa è la risposta corretta, false altrimenti)"
                        }
                    ]
                }
            ]
        }
        
        # Crea il prompt dettagliato per Ollama
        prompt = f"""Genera un quiz in formato JSON seguendo ESATTAMENTE questo schema:

{json.dumps(schema_json, indent=2, ensure_ascii=False)}

REQUISITI:
- Tema del quiz: {tema}
- Difficoltà: {difficolta}
- Numero di domande: {numero_domande}
- Ogni domanda deve avere esattamente 4 opzioni di risposta
- Solo UNA opzione per domanda deve avere "corretta": true
- Le domande devono essere appropriate per il livello di difficoltà specificato
- Gli ID devono essere stringhe univoche (usa formato come "q1_d1", "q1_d1_o1", ecc.)
- Il titolo deve essere in italiano e descrittivo del tema
- Tutti i testi devono essere in italiano

IMPORTANTE: 
- Restituisci SOLO il JSON valido, senza testo aggiuntivo prima o dopo
- Il JSON deve essere valido e parsabile
- Segui ESATTAMENTE la struttura dello schema fornito
- Assicurati che ogni domanda abbia esattamente 4 opzioni
- Assicurati che solo una opzione per domanda sia corretta

Genera il quiz ora:"""
        
        # Chiama Ollama con format=json usando l'API REST
        ollama_url = 'http://localhost:11434/api/chat'
        payload = {
            'model': 'llama3.1:8b',
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'format': 'json',
            'stream': False
        }
        
        try:
            ollama_response = requests.post(ollama_url, json=payload, timeout=120)
            ollama_response.raise_for_status()
            response_data = ollama_response.json()
            
            # Estrai il contenuto della risposta
            quiz_json_str = response_data['message']['content']
        except requests.exceptions.ConnectionError:
            return jsonify({
                "error": "Impossibile connettersi a Ollama. Assicurati che Ollama sia in esecuzione su http://localhost:11434"
            }), 500
        except requests.exceptions.Timeout:
            return jsonify({
                "error": "Timeout nella chiamata a Ollama. La generazione del quiz sta richiedendo troppo tempo."
            }), 500
        except requests.exceptions.RequestException as e:
            return jsonify({
                "error": f"Errore nella chiamata a Ollama: {str(e)}"
            }), 500
        
        # Pulisci la risposta da eventuali markdown code blocks
        if '```json' in quiz_json_str:
            quiz_json_str = quiz_json_str.split('```json')[1].split('```')[0].strip()
        elif '```' in quiz_json_str:
            quiz_json_str = quiz_json_str.split('```')[1].split('```')[0].strip()
        
        # Parse del JSON
        quiz_data = json.loads(quiz_json_str)
        
        # Genera ID univoci se non presenti o non validi
        if 'id' not in quiz_data or not quiz_data['id']:
            quiz_data['id'] = f"quiz_{uuid.uuid4().hex[:12]}"
        
        # Assicurati che ogni domanda e opzione abbia un ID
        for i, domanda in enumerate(quiz_data.get('domande', [])):
            if 'id' not in domanda or not domanda['id']:
                domanda['id'] = f"q_{i+1}_d{i+1}"
            
            for j, opzione in enumerate(domanda.get('opzioni', [])):
                if 'id' not in opzione or not opzione['id']:
                    opzione['id'] = f"{domanda['id']}_o{j+1}"
        
        # Valida che ci sia almeno una risposta corretta per domanda
        for domanda in quiz_data.get('domande', []):
            opzioni_corrette = [op for op in domanda.get('opzioni', []) if op.get('corretta', False)]
            if len(opzioni_corrette) != 1:
                return jsonify({
                    "error": f"Ogni domanda deve avere esattamente una risposta corretta. Domanda '{domanda.get('id', 'unknown')}' ha {len(opzioni_corrette)} risposte corrette."
                }), 400
        
        # Salva il quiz nel file data.json
        with open('data.json', 'r', encoding='utf-8') as f:
            quizzes = json.load(f)
        
        quizzes.append(quiz_data)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(quizzes, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            "message": "Quiz generato con successo!",
            "quiz": quiz_data
        }), 201
        
    except json.JSONDecodeError as e:
        return jsonify({
            "error": f"Errore nel parsing del JSON generato da Ollama: {str(e)}",
            "raw_response": quiz_json_str if 'quiz_json_str' in locals() else None
        }), 500
    except KeyError as e:
        return jsonify({
            "error": f"Struttura JSON non valida: campo mancante {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Errore durante la generazione del quiz: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
