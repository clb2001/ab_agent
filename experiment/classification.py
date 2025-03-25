PROMPT_rate = '''
You are an information generation expert. 
Please evaluate and score from the following perspectives, assigning a score from 1 to 5 according to the degree from low to high. 
(1) Alignment: The text and the description may show varying degrees of alignment, meaning they have a certain degree of consistency. The higher the consistency, the higher the score. 
(2) Causality confusion: The description may confuse correlations presented in the text as causal relationships. The lower the degree of causality confusion, the higher the score. 
(3) Accuracy: This refers to whether the description is qualitatively and quantitatively in accordance with scientific accuracy. The higher the accuracy, the higher the score. 
(4) Generalization: This refers to whether the description excessively generalizes or oversimplifies the text. The lower the degree of generalization, the higher the score. 
(5) Contextual fidelity: Does the description retain the broader context of the text? The higher the fidelity, the higher the score. 
(6) Strong Global Coherence (SGC): Each sentence in the description must contain content mentioned in the text. The higher the SGC, the higher the score. 
(7) Weak Global Coherence (WGC): All sentences in the description should contain or maintain a neutral relationship with the text. Therefore, no sentence in the description should contradict the content of the text. The higher the WGC, the higher the score. 
(8) Local Coherence (LC): In the description, two sentences should not contradict each other. The higher the LC, the higher the score. 

Given the following text: 
{text}
Based on the above text, here is the following description: 
{description}

Output in JSON format, as shown in the examples below. Do not output other irrelevant information, such as the reason.
{{'alignment': 3, 'causality_confusion': 2, 'accuracy': 3, 'generalization': 4, 'contextual_fidelity': 3, 'SGC': 2, 'WGC': 5, 'LC': 3}}
{{'alignment': 1, 'causality_confusion': 2, 'accuracy': 1, 'generalization': 2, 'contextual_fidelity': 2, 'SGC': 2, 'WGC': 2, 'LC': 2}}
'''

PROMPT_classification = '''
You are an information detection expert. 

Based on the scoring results and your judgment, you need to categorize the results into the following four types and provide reasons:
false: Indicates that the description is completely incorrect.
true: Indicates that the description is completely correct.
mixture: Indicates that the description contains both errors and correct elements.
unproven: Indicates that the description has not been verified. 

Given the following text: 
{text}
Based on the above text, here is the following description: 
{claim}

Output in JSON format, as shown in the examples below: 
{{'result': 'mixture', 'reason': 'What's true: Pancake and cake mixes that contain mold can cause life-threatening allergic reactions. What's false: Pancake and cake mixes that have passed their expiration dates are not inherently dangerous to ordinarily healthy people.'}}
{{'result': 'Talk of a Harvard study linking the popular British children's show "Peppa Pig" to autism went viral, but neither the study nor the scientist who allegedly published it exists.'}}
'''

import re
import sys
sys.path.append('/Users/clb/Desktop/project/code/paper/utils')
import json
import pandas as pd
from tqdm import tqdm
from call_openai import call_openai
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def load_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)    

def classify(model):
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/PUBHEALTH/test.tsv'
    save_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/classification_{model}.json'
    df = pd.read_csv(dataset_path, sep='\t')
    data = list()
    for id, d in tqdm(df.iterrows()):
        if not pd.isna(d['label']):
            subjects = d['subjects']
            main_text = d['main_text']
            claim = d['claim']
            label = d['label']
            explanation = d['explanation']
            claim = d['claim']
            ele = {
                'id': id,
                'subjects': subjects,
                'main_text': main_text,
                'claim': claim,
                'label': label,
                'explanation': explanation,
            }
            data.append(ele)
        if id == 99:
            break
    call_openai(
        data,
        'classification',
        PROMPT_classification,
        output_path=save_path,
        model=model,
        num_workers=20
    )

def get_score(model):
    dataset_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/classification_{model}.json'
    df = load_json(dataset_path)
    data = list()
    for id, d in tqdm(enumerate(df)):
        if not pd.isna(d['label']):
            d['description'] = d['claim']
            data.append(d)
    call_openai(
        data,
        'get_score',
        PROMPT_rate,
        output_path=dataset_path,
        model='gpt-4o-2024-08-06',
        num_workers=20
    )

def get_result_classification_res(text):
    if 'true' in text:
        return 'true'
    elif 'false' in text:
        return 'false'
    elif 'mixture' in text:
        return 'mixture'
    else:
        return 'unproven'

def get_result_get_score_res(text):
    try:
        return eval(text.replace("```", "").replace("json", "").replace("\n", ""))
    except:
        pattern = r"'(\w+)':\s*(\d+)"
        matches = re.findall(pattern, text)
        result_dict = {key: int(value) for key, value in matches}
        return result_dict

def evaluate(model, label='unproven'):
    data_path = f'/Users/clb/Desktop/project/code/paper/experiment/res/classification_{model}.json'
    data = load_json(data_path)
    for d in tqdm(data):
        try:
            result_get_score = get_result_get_score_res(d['response_get_score'])
            d['alignment'] = result_get_score['alignment']
            d['causality_confusion'] = result_get_score['causality_confusion']
            d['accuracy'] = result_get_score['accuracy']
            d['generalization'] = result_get_score['generalization']
            d['contextual_fidelity'] = result_get_score['contextual_fidelity']
            d['SGC'] = result_get_score['SGC']
            d['WGC'] = result_get_score['WGC']
            d['LC'] = result_get_score['LC']
            d['predict_result'] = get_result_classification_res(d['response_classification'])
        except:
            pass
    save_json(data, data_path)
    df = pd.DataFrame(data)
    y_true = df['label']
    y_pred = df['predict_result']
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro') 
    recall = recall_score(y_true, y_pred, average='macro')        
    f1 = f1_score(y_true, y_pred, average='macro')                
    print(f"model: {model}")
    print(f"accuracy: {accuracy:.2f}, precision: {precision:.2f}, recall: {recall:.2f}, f1: {f1:.2f}") 
    print(f"alignment: {df[df['label'] == label]['alignment'].mean():.2f}")
    print(f"causality_confusion: {df[df['label'] == label]['causality_confusion'].mean():.2f}")
    print(f"accuracy: {df[df['label'] == label]['accuracy'].mean():.2f}")
    print(f"generalization: {df[df['label'] == label]['generalization'].mean():.2f}")
    print(f"contextual_fidelity: {df[df['label'] == label]['contextual_fidelity'].mean():.2f}")
    print(f"SGC: {df[df['label'] == label]['SGC'].mean():.2f}")
    print(f"WGC: {df[df['label'] == label]['WGC'].mean():.2f}")
    print(f"LC: {df[df['label'] == label]['LC'].mean():.2f}")
    print("-----------------------------")

if __name__=='__main__':
    models = ['gpt-4o-2024-08-06', 'gpt-4o-mini']
    for model in models: 
        classify(model)
        get_score(model)
        evaluate(model)
