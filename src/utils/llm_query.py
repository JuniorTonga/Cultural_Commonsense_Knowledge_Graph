import openai
from openai import OpenAI
from config import OPENAI_API_KEY, GROQ_API_KEY,HF_TOKEN
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login
from transformers import BitsAndBytesConfig

double_quant_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_use_double_quant=True,
)
import os

model_name = os.environ['LLAMA_PATH']
login(HF_TOKEN)

llama_model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto', local_files_only=True, quantization_config=double_quant_config, low_cpu_mem_usage=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)


def query_gpt(prompt,engine='gpt-4o',temp=1):
    client=OpenAI(api_key=OPENAI_API_KEY)
    try:
        response=client.chat.completions.create(model=engine,messages=prompt,temperature=temp)
    except Exception as exc:
        print('failed')
        return query_gpt(prompt,engine,temp)
    return response.choices[0].message.content.strip()

@torch.no_grad()
def query_llama(prompt, model='meta-llama/Llama-3.3-70B-Instruct',temp=1):
    # Generate predictions
    prompt = tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(prompt, return_tensors="pt").to("cuda") 
    output = llama_model.generate(inputs, max_new_tokens=6000, temperature=1)
    response = tokenizer.decode(output[0].tolist())
    response = response.split("<|end_header_id|>")[-1].replace("<|eot_id|>", "").strip()
    if not response.endswith("]"):
        response = response + "]"
    return response 


