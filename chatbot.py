import gradio as gr
import os
from openai import OpenAI

#client = OpenAI(
    # Replace with your valid API key
    #api_key=""
#)

def chat_gpt(message):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content.strip()

message_history = []

def chat_response(message, history):  # Only takes one argument `message`
    print(message)
    user_message = {"role": "user", "content": message}
    message_history.append(user_message)

    content = chat_gpt(message)
    assistant_message = {"role": "assistant", "content": content}
    message_history.append(assistant_message)

    return content

chat_demo = gr.ChatInterface(fn=chat_response, title="Phases Bot")
chat_demo.launch(share=True,server_port=4001)