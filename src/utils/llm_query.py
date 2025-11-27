import openai 
from openai import OpenAI
from config import OPENAI_API_KEY,HF_TOKEN
import transformers
import torch
from huggingface_hub import login
from vllm import LLM, SamplingParams
import re


login(HF_TOKEN)

def clean_tokens(output: str):
    cleaned_output = re.sub(r'<\|start_header_id\|>.*?<\|end_header_id\|>', '', output)
    return cleaned_output.strip()

def query_gpt(prompt,engine='gpt-4o',temp=1):
    client=OpenAI(api_key=OPENAI_API_KEY)
    try:
        response=client.chat.completions.create(model=engine,messages=prompt,temperature=temp)
    except Exception as exc:
        print('failed')
        return query_gpt(prompt,engine,temp)
    return response.choices[0].message.content.strip()


def query_llama(prompt,model_name='meta-llama/Llama-3.1-8B-Instruct',temp=1, model=None, tokenizer=None, llm=None):
    if "meta-llama" in model_name or "google" in model_name :
        formatted_prompts = tokenizer.apply_chat_template(prompt, tokenize=False)
        outputs = llm.generate(formatted_prompts, SamplingParams(temperature=1, max_tokens=2048, top_p=0.95, top_k=-1, seed=0))
        response = clean_tokens(outputs[0].outputs[0].text)
    else:
        formatted_prompts=tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        tokenizer.pad_token = tokenizer.eos_token
        inputs = tokenizer(formatted_prompts, padding=True, return_tensors="pt").to(model.device)
        prompt_padded_len = len(inputs[0])
        gen_tokens = model.generate(inputs.input_ids, attention_mask=inputs.attention_mask, max_new_tokens=2048, do_sample=True,temperature=1, pad_token_id=tokenizer.pad_token_id)
        gen_tokens = [gt[prompt_padded_len:] for gt in gen_tokens]
        decoded_answer  = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)
        response=decoded_answer[0]
    
    print('=========NON GPT RESULT========', response)
    return response 

    
