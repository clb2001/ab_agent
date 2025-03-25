PROMPT_rate = '''
你是一个信息理解专家，请判断下面两个列表中的句子是否有一致的情况，并输出一致率，保留三位小数即可。
参考结果是：
{refs}，
输出结果是：
{res}
示例如下：
参考结果是：
[a, b, c]
输出结果是：
[c, b, d]
输出：0.667
'''

PROMPT_comprehension = '''
你是一个信息理解专家，请从文本中获取最能支持论述的{nums}个句子，并返回这些句子。
论述是：
{claim}
如果nums为0或者不存在相关的论述，返回空列表。
你只要输出这些句子即可，以列表的格式输出，示例如下：
["aaa", "bbb", "ccc"]
'''
import re
import os
import sys
sys.path.append('/Users/clb/Desktop/project/code/paper/utils')
sys.path.append('/Users/clb/Desktop/project/code/paper')
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from my_rag import get_corase_sift_res
from call_openai import call_openai
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def load_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)    

def analysis():
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/CHEF/dev.json'
    dataset = load_json(dataset_path)
    a = set()
    for d in dataset:
        a.add(d['category'])
    print(a)

def get_info(d):
    res = []
    for kv in d['evidence']:
        res.append(d['evidence'][kv]['text'])
    if len(res) == 0:
        return ""
    return '\n'.join(res)

def get_nums(d):
    cnt = 0
    for kv in d['gold evidence']:
        if len(d['gold evidence'][kv]['text']) != 0:
            cnt += 1
    return str(cnt)

def get_refs(d):
    refs = []
    for kv in d['gold evidence']:
        if len(d['gold evidence'][kv]['text']) != 0:
            refs.append(d['gold evidence'][kv]['text'])    
    return str(refs)

def get_info_rag(d):
    docs = set()
    for kv in d['evidence']:
        texts = d['evidence'][kv]['text']
        sentences = re.split(r'(?<=[。！？])', texts)
        sentences = [s.strip() for s in sentences if s.strip()]
        for sentence in sentences:
            docs.add(sentence)
    return list(docs)

MAX_ITERS = 10

def comprehend(model):
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/CHEF/dev.json'
    save_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/comprehension_{model}.json'
    df = load_json(dataset_path)
    data = list()
    cnt = 0
    for id, d in tqdm(enumerate(df)):
        if len(d['claim']) != 0:
            claim = d['claim']
            label = d['label']
            claim = d['claim']
            ele = {
                'id': id,
                'main_text': get_info(d),
                'nums': get_nums(d),
                'claim': claim,
                'label': label,
                'refs': get_refs(d)
            }
            data.append(ele)
            cnt += 1
            if cnt == MAX_ITERS:
                break
    call_openai(
        data,
        'comprehension',
        PROMPT_comprehension,
        output_path=save_path,
        model=model,
        num_workers=20
    )

def comprehension_rag(model):
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/CHEF/dev.json'
    save_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/comprehension_rag_{model}.json'
    df = load_json(dataset_path)
    data = list()
    cnt = 0
    for id, d in tqdm(enumerate(df)):
        if len(d['claim']) != 0:
            claim = d['claim']
            label = d['label']
            ele = {
                'id': id,
                'sentences': get_info_rag(d),
                'nums': get_nums(d),
                'claim': claim,
                'label': label,
                'refs': get_refs(d)
            }
            corase_sift_res = get_corase_sift_res(claim, ele['sentences'])
            ele['main_text'] = corase_sift_res 
            data.append(ele)
            cnt += 1
            if cnt == MAX_ITERS:
                break        
    call_openai(
        data,
        'comprehension',
        PROMPT_comprehension,
        output_path=save_path,
        model=model,
        num_workers=20
    )

def evaluate(model, mode=None):
    if mode is None:
        data_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/comprehension_{model}.json'
    else:
        data_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/comprehension_rag_{model}.json'
    data = load_json(data_path)
    call_openai(
        data,
        'comprehension_evaluate',
        PROMPT_comprehension,
        output_path=data_path,
        model='gpt-4o-2024-08-06',
        num_workers=20
    )
    cnt = 0
    for d in tqdm(data):
        sim_ref, sim_response_comprehension = d['response_comprehension_evaluate']['refs'], d['response_comprehension_evaluate']['response_comprehension']
        np_sim_ref, np_sim_response_comprehension = np.array(sim_ref).astype(float), np.array(sim_response_comprehension).astype(float)
        sim = np.dot(np_sim_ref, np_sim_response_comprehension) / (np.linalg.norm(np_sim_ref) * np.linalg.norm(np_sim_response_comprehension))
        d['sim'] = sim
    df = pd.DataFrame(data)
    accuracy_score = cnt / len(data)
    print(f"accuracy: {accuracy_score:.2f}")  
    print(f"{df['sim'].mean()}")  
    save_json(data, data_path)

if __name__=='__main__':
    models = ['gpt-4o-2024-08-06', 'gpt-4o-mini']
    for model in models:
        comprehend(model)
        comprehension_rag(model)
        evaluate(model)
        evaluate(model, mode='rag')
