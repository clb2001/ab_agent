# -*- encoding: utf-8 -*-
import os
import requests
import json
import base64
import cv2
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

headers = {
    'Authorization': '',    
    'Content-Type': 'application/json',
}

def image_to_base64(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    max_length = 1200
    if max(height, width) > max_length:
        scale = max_length / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def _make_request(content: List[str], model: str):
    data = {
        "model": model,
        "messages": [{'role': 'user', 'content': []}],
        # "temperature": 0.0001,
        "stream": False
    }
    for msg in content:
        if msg.startswith('http'):
            c = {
                'type': 'image_url',
                'image_url': {'url': msg}
            }
        elif msg.startswith('/Users'):
            c = {
                'type': 'image_url',
                'image_url': {'url': f"data:image/jpeg;base64,{image_to_base64(msg)}"}
            }
        else:
            c = {
                'type': 'text',
                'text': msg
            }
        data['messages'][0]['content'].append(c)
    return data

def _make_embedding_request(content: str, model: str):
    data = {
        "model": model,
        "input": content,
        "stream": False
    }
    return data

# content, prompt, task, model
def call_openai_single(
        content, 
        prompt=None,
        task=None,
        model='gpt-4o-mini', 
    ):
    if task == 'classification':
        c = [prompt.format(text=content['main_text'], claim=content['claim'])]
    elif task == 'comprehension' or task == 'comprehension_rag':
        c = [prompt.format(nums=content['nums'], text=content['main_text'], claim=content['claim'])]
    elif task == 'generation':
        c = [prompt.format(text=content['main_text'], requirement=content['requirement'])]
    elif task == 'get_score':
        c = [prompt.format(text=content['main_text'], description=content['description'])]
    elif task == 'label':
        c = [prompt.format(label=content['subjects'])]
    else:
        c = [content]
    url = ''
    request = _make_request(c, model)
    cnt = 0
    while True:
        if cnt >= 100:
            return None
        response = requests.post(url, headers=headers, data=json.dumps(request))
        if response.status_code == 200:
            response = response.json()    
            if isinstance(response, dict) and "choices" in response.keys() and isinstance(response["choices"], list) \
                and "message" in response["choices"][0].keys() and "content" in response["choices"][0]["message"].keys():          
                return response
        cnt += 1

def call_openai_embedding_double(content, model='text-embedding-ada-002'):
    url = ''
    res = {}
    request = _make_embedding_request(content['refs'], model)
    cnt = 0
    while True:
        if cnt >= 100:
            return None
        response = requests.post(url, headers=headers, data=json.dumps(request))
        if response.status_code == 200:
            response = response.json()    
            if isinstance(response, dict) and "data" in response.keys() and isinstance(response["data"], list) \
                and "embedding" in response["data"][0].keys():          
                res['refs'] = response["data"][0]["embedding"]
                break
        cnt += 1
    request = _make_embedding_request(content['response_comprehension'], model)
    cnt = 0
    while True:
        if cnt >= 100:
            return None
        response = requests.post(url, headers=headers, data=json.dumps(request))
        if response.status_code == 200:
            response = response.json()    
            if isinstance(response, dict) and "data" in response.keys() and isinstance(response["data"], list) \
                and "embedding" in response["data"][0].keys():          
                res['response_comprehension'] = response["data"][0]["embedding"]
                break
        cnt += 1
    return res

def call_openai_embedding_single(content, model='text-embedding-ada-002'):
    url = ''
    request = _make_embedding_request(content, model)
    cnt = 0
    while True:
        if cnt >= 100:
            return None
        response = requests.post(url, headers=headers, data=json.dumps(request))
        if response.status_code == 200:
            response = response.json()    
            if isinstance(response, dict) and "data" in response.keys() and isinstance(response["data"], list) \
                and "embedding" in response["data"][0].keys():          
                return response["data"][0]["embedding"]
        cnt += 1
            
def call_openai_embedding(content: List[str], model='text-embedding-ada-002'):
    results = [None] * len(content)
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(call_openai_embedding_single, content, model*len(content)), total=len(content)))
    return results
              
def _call_openai_parallel(
        content: List[dict],
        prompt: str = None,
        task=None,
        num_workers=20,
        model='gpt-4o-mini', 
):
    if num_workers > 20:
        num_workers = 20
        print(f'[Warning] num_workers 不能超过10, 改为10!')
    if prompt is None:
        prompt = []
    results = [None] * len(content)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:         
        if task == 'comprehension_evaluate':
            results = list(tqdm(executor.map(call_openai_embedding_double, content), total=len(content)))
        else:
            results = list(tqdm(executor.map(call_openai_single, content, [prompt]*len(content), [task]*len(content), [model]*len(content)), total=len(content)))
    for i, c in enumerate(content):
        if results[i] is None:
            c[f'response_{task}'] = None
        else:
            if task == 'comprehension_evaluate':
                c[f'response_{task}'] = results[i]
            else:
                c[f'response_{task}'] = results[i]['choices'][0]['message']['content']
    return content

def call_openai(
    data, 
    task,
    prompt: str = None, 
    output_path: str = None,
    model: str = 'gpt-4o-mini',
    num_workers: int = 1
):
    if isinstance(data, str):
        with open(data) as f:
            data = json.load(f)
    if num_workers == 1:
        result = call_openai_single(data, prompt, task, model=model)
        print(result)
        return
    results = _call_openai_parallel(data, prompt, task, num_workers, model)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    pass
