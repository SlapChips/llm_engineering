#!/opt/homebew/python3

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr



# def chat(message, history):
#     messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
#     response = openai.chat.completions.create(model=MODEL, messages=messages)
#     return response.choices[0].message.content
# Example of Using Tools
#
# This creates a function that the LLM can use to provide responses
#
# Step 1. Create a function that you want to add as a tool
#
#
ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
#

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")
#
# Step 5. Setup LLM to use tool
#

# Step 2. Create a dict structure that the LLM  expects to use in its toolset
#
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
# Step 3. And the tool function a list of tools:
tools = [{"type": "function", "function": price_function}]
#
def chat(message, history):
    messages = [
        {"role":"system", 
         "content": system_message
        }] \
              + history + \
        [{
            "role": "user",
            "content":message
        }]
    response = openai.chat.completions.create(
        model="llama3.2",
        messages=messages, 
        tools=tools
    )
    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(
            model="llama3.2",
            messages=message
        )
    return response.choices[0].message.content
#
# Step 5. Write a function to handle the tool call:
#
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,
                               "price": price}),
        "tool_call_id":tool_call.id
    }
    return response, city

def main():
    aaa

#Initialization
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")    
# MODEL = "gpt-4o-mini"
MODEL = "llama3.2"
openai = OpenAI(
    base_url='http://localhost:11434/v1', 
    api_key='ollama'
    )
# As an alternative, if you'd like to use Ollama instead of OpenAI
# Check that Ollama is running for you locally (see week1/day2 exercise) then uncomment these next 2 lines
# MODEL = "llama3.2"
# openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

#System Prompt:
system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."




gr.ChatInterface(fn=chat, type="messages").launch()

