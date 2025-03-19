#!python3
# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai
from IPython.display import Markdown, display, update_display
from AiHelper import GetApiKeys







def main():
    GetApiKeys()
    print(os.getenv('OPENAI_API_KEY'))
    openai = OpenAI()
    system_message = "You are an assistant that is great at telling jokes"
    user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"
    prompts = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompts,
        temperature=0.7
    )
    # this is how we print the whole answer, when stream = False
    print(completion.choices[0].message.content)
   
    # if we want to stream:
    # Below works in Jupyter notebook only..
    # stream = openai.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=prompts,
    #     temperature=0.7,
    #     stream=True
    # )
    # reply = ""
    # # Display the initial empty markdown cell for update
    # display_handle = display(Markdown(""), display_id=True)
    
    # # Iterate over the streamed response
    # for chunk in stream:
    #     reply += chunk.choices[0].delta.content or ''
    #     reply = reply.replace("```", "").replace("markdown", "")
        
    #     # Update the markdown display in place using display_id
    #     update_display(Markdown(reply), display_id=display_handle.display_id)

if __name__ == "__main__":
    main()