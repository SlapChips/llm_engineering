#!python3
# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai
from IPython.display import Markdown, display, update_display
from AiHelper import GetApiKeys


def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, llama_message in zip(gpt_messages, llama_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": llama_message})
    
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_llama():
    messages = []
    for gpt, llama_message in zip(gpt_messages, llama_messages):
        messages.append({"role":"system", "content":llama_system})
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": llama_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    completion = openai_llama.chat.completions.create(
        model=llama_model,
        messages=messages
    )
    return completion.choices[0].message.content

GetApiKeys()
openai =OpenAI()
openai_llama = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)
gpt_model = "gpt-4o-mini"
llama_model = "llama3.2"

gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

llama_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

gpt_messages = ["Hi there"]
llama_messages = ["Hi"]

print(f"GPT:\n{gpt_messages[0]}\n")
print(f"Llama:\n{llama_messages[0]}\n")

for i in range(5):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)
    
    llama_next = call_llama()
    print(f"Claude:\n{llama_next}\n")
    llama_messages.append(llama_next)
