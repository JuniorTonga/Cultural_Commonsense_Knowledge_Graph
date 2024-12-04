import openai 
from openai import OpenAI
from config import OPENAI_API_KEY

def query_llm(prompt,engine='gpt-4o',temp=1):
    client=OpenAI(api_key=OPENAI_API_KEY)
    try:
        response=client.chat.completions.create(model=engine,messages=prompt,temperature=temp)
    except Exception as exc:
        print('failed')
        return query_llm(prompt,engine,temp)
    return response.choices[0].message.content.strip()