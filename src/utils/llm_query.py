import openai 
from openai import OpenAI
from config import OPENAI_API_KEY, GROQ_API_KEY,HF_TOKEN
from groq import Groq
import transformers
import torch
from huggingface_hub import login


def query_gpt(prompt,engine='gpt-4o',temp=1):
    client=OpenAI(api_key=OPENAI_API_KEY)
    try:
        response=client.chat.completions.create(model=engine,messages=prompt,temperature=temp)
    except Exception as exc:
        print('failed')
        return query_gpt(prompt,engine,temp)
    return response.choices[0].message.content.strip()


def query_llama(prompt,model='meta-llama/Llama-3.3-70B-Instruct',temp=1):
    login(HF_TOKEN)
    pipeline=transformers.pipeline('text-generation',model=model,
                                   model_kwargs={"torch_dtype":torch.bfloat16},
                                   device_map="auto"
                                   )
    outputs=pipeline(prompt,temperature=temp)
    response=outputs[0]["generated_text"][-1]
    return response 

#def query_groq_llm(prompt,model='llama-3.3-70b-versatile',temp=1, top_p=1):
  #  client = Groq(api_key=GROQ_API_KEY)
  #  try:
   #     response=client.chat.completions.create(messages=prompt,
  #          model=model,
   #         temperature=temp,
  #          top_p=top_p,
  #      )
  #  except:
 #       return query_groq_llm(prompt,model,temp,top_p)
 #   return response.choices[0].message.content.strip()


    
