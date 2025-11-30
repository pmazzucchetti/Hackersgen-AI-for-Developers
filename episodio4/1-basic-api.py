from ollama import Client

client = Client()

messages=[{"role": "system", "content": "Sei un assistente utile e informativo."},]

while True:

    user_input = input(">>> ")
    messages.append({"role": "user", "content": user_input})
    resp = client.chat(
        model="llama3.1:8b", 
        messages=messages,
        stream=False  
    )
    messages.append({"role": "assistant", "content": resp.message.content})
    print(resp.message.content)
