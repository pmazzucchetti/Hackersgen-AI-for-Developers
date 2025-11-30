import json
from pydantic import BaseModel, ValidationError
from ollama import Client

client = Client() 

class CalendarEvent(BaseModel):
    nome: str
    data: str
    orario: str
    partecipanti: list[str]

system_prompt = """
Genera un JSON che estrae le informazione sull'evento da calendario dato dall'utente.

Schema:
{
  "nome": "string",
  "data": "string",
  "orario": "string",
  "partecipanti": ["string", "string", ...]
}

Rispondi SOLO con JSON valido e conforme allo schema.
"""

messages = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": "Mario, Luigi e Zelda andranno ad una conferenza su Python il 10 dicembre 2025 alle 9:00 AM",
    },
]

resp = client.chat(
    model="llama3.1:8b",
    messages=messages,
    stream=False,
    format="json"
)

raw_text = resp["message"]["content"]

data = json.loads(raw_text)

try:
    event = CalendarEvent(**data)
    print("Evento Valido:")
    print(event)
    print(event.nome)
    print(event.data)
    print(event.orario)
    print(event.partecipanti)
except ValidationError as e:
    print("Errore di validazione:", e)

for person in event.partecipanti:
    print(person + " parteciperà all'evento: " + event.nome + " il " + event.data)
