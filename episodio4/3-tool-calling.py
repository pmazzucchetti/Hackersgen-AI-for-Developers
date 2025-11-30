import requests

from ollama import chat


def get_meteo(latitudine, longitudine):
    """API pubblica che restituisce le condizioni meteo attuali per una determinata posizione.
    
    Args:
        latitudine: latitudine della località
        longitudine: longitudine della località
        
    Return:
        Il meteo corrente nella località selezionata
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitudine}&longitude={longitudine}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

system_prompt = "Sei un assistente meteo utile e informativo."


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Che tempo fa oggi a Bergamo?"},
]

resp = chat(
    model="llama3.1:8b",
    messages=messages,
    tools=[get_meteo]
)
print(resp)
messages.append(resp.message)

if resp.message.tool_calls:
    call = resp.message.tool_calls[0]
    result = get_meteo(**call.function.arguments)
    messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

    final_response = chat(model="llama3.1:8b", messages=messages, tools=[get_meteo])
    print(final_response.message.content)

