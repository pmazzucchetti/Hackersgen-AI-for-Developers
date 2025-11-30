import json
from ollama import Client

client = Client()

def read_knowledge_base():
    """Apre in lettura un file json contenente informazioni sulle macchine.
    
    Return:
        Ritorna l'intero file json
    """
    with open("kb.json") as f:
        return json.load(f)
    

SYSTEM_PROMPT="""
Sei un assistente sistemista, che deve rispondere a delle domande relative alcune macchine.
"""
messages=[{"role": "system", "content": SYSTEM_PROMPT}]


while True:

    user_input = input(">>> ")
    messages.append({"role": "user", "content": user_input})
    resp = client.chat(
        model="llama3.1:8b", 
        messages=messages,
        tools=[read_knowledge_base]
    )
    if resp.message.tool_calls:
        for tool_call in resp.message.tool_calls:
            call = resp.message.tool_calls[0]
            try:
                result = read_knowledge_base(**call.function.arguments)
            except:
                continue
            messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

            final_response = client.chat(model="llama3.1:8b", messages=messages, tools=[read_knowledge_base])
            print(final_response.message.content)
            messages.append({"role": "assistant", "content": final_response.message.content})
    else: 
        messages.append({"role": "assistant", "content": resp.message.content})
        print(resp.message.content)


