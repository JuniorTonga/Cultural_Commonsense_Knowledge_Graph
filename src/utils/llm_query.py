import openai 
from openai import OpenAI
from config import OPENAI_API_KEY, GROQ_API_KEY
from groq import Groq


def query_gpt(prompt,engine='gpt-4o',temp=1):
    client=OpenAI(api_key=OPENAI_API_KEY)
    try:
        response=client.chat.completions.create(model=engine,messages=prompt,temperature=temp)
    except Exception as exc:
        print('failed')
        return query_gpt(prompt,engine,temp)
    return response.choices[0].message.content.strip()

def query_groq_llm(prompt,model='llama-3.3-70b-versatile',temp=1, top_p=1):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response=client.chat.completions.create(messages=prompt,
            model=model,
            temperature=temp,
            top_p=top_p,
        )
    except:
        return query_groq_llm(prompt,model,temp,top_p)
    return response.choices[0].message.content.strip()