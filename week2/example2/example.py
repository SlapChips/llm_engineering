#!/bin/python3

import requests
import json
import os
import finnhub
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def validate_api(api_key, llm):
    llm.models.list()
    return True
    

def get_env():
    load_dotenv(override=True)

def llm_session(llm,tools, user_prompt):
    messages = [
            {"role": "system",
             "content": "you are a helpful assistant that responds in short single sentences"},
            {"role": "user",
             "content": user_prompt}
        ]
    response = llm.chat.completions.create(
        model='gpt-4o-mini',
        messages= messages,
        tools=tools
    )
    if response.choices[0].finish_reason == "tool_calls":
        print("TOOL_CALLED")
        print(response.choices[0].message.tool_calls)
        tool_call = response.choices[0].message.tool_calls[0]
        kwargs = json.loads(tool_call.function.arguments)
        tool = tool_call.function.name
        
        print(kwargs)
        
        # result = get_the_news(args['subject'])
        result = globals()[tool](**kwargs)
        messages.append(response.choices[0].message)  # append model's function call message
        messages.append({                               # append result message
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        completion_2 = llm.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        print(completion_2.choices[0].message.content)

    elif response.choices[0].finish_reason == "stop":
        print("TOOL_CALL_SKIPPED")
    else:
        print(response.choices[0].finish_reason)

def get_stock_info(**kwargs):
    symbol = kwargs.get('symbol')
    API_KEY = os.getenv('FINNHUB_API_KEY')
    client = finnhub.Client(api_key=API_KEY)
    quote = client.quote(symbol=symbol)
    today = datetime.today()
    from_days = today - relativedelta(days=7)
    _from = from_days.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
    today = today.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
    news = client.company_news(symbol=symbol, _from=_from, to=today)
    print(news)
    return quote, news

def get_the_news(**kwargs):
    subject = kwargs.get('subject')
    API_KEY = os.getenv('GUARDIAN_API_KEY')
    URL = f'https://content.guardianapis.com/search?q={subject}&api-key={API_KEY}'
    news = requests.get(URL)
    return news.content

def load_tools() -> dict:
    tools = [
        {"type": "function",
            "function": {
                "name": "get_the_news",
                "description": "Get the news for a given Subject.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "A subject or field of interest i.e. Sport or Politics"
                        }
                    },
                    "required": [
                        "subject"
                    ],
                    "additionalProperties": False
                },
                "strict": True
        }},
        {"type": "function",
            "function": {
                "name": "get_stock_info",
                "description": "Get the stock market information for a given Company. The information provides current company news and stock price quotations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock Symbol for a given company i.e. Cisco Systems is CSCO, Apple is AAPL"
                        }
                    },
                    "required": [
                        "symbol"
                    ],
                    "additionalProperties": False
                },
                "strict": True
            }
        }]
    return tools

def main():
    api_key=os.getenv('OPENAI_API_KEY')
    print(api_key)
    llm = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    if validate_api(api_key=api_key, llm=llm):
        print("API Key Validated Successfully")
    tools = load_tools()
    message = "Whats the latest news related to Microsoft stock prices??"
    llm_session(llm=llm,user_prompt=message, tools=tools)

    # get_stock_info(symbol='CSCO')


if __name__=="__main__":
    get_env()
    main()

    
