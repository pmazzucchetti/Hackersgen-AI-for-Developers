from flask import Flask, jsonify, request
from flask_cors import CORS
import json

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


if __name__ == "__main__":
    app.run(debug=True)
