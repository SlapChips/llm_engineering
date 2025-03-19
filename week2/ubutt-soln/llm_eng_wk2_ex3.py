#!/opt/homebrew/bin/python3

import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic
import gradio as gr # oh yeah!



def message_gpt(prompt): # takes prompt as an input...
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    completion = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
    )
    return completion.choices[0].message.content

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

system_message = "You are a helpful assistant that responds in markdown"

openai = OpenAI()

message_gpt("What is today's date?")
shout("hello")
# gr.Interface(fn=shout, inputs="textbox", outputs="textbox").launch()
# Adding share=True means that it can be accessed publically
# A more permanent hosting is available using a platform called Spaces from HuggingFace, which we will touch on next week
# NOTE: Some Anti-virus software and Corporate Firewalls might not like you using share=True. If you're at work on on a work network, I suggest skip this test.

view = gr.Interface(
    fn=stream_gpt,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=[gr.Textbox(label="Response:")],
    flagging_mode="never"
)
view.launch()