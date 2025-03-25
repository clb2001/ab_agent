import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict

def plot_zhifang(data):
    plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
    plt.title('Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def pubhealth():
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/PUBHEALTH/dev.tsv'
    df = pd.read_csv(dataset_path, sep='\t')
    default_dict = defaultdict(int)
    arr = []
    for id, d in tqdm(df.iterrows()):
        # default_dict[d['subjects']] += 1
        if pd.notna(d['claim']):
            a = len(d['claim'])
            arr.append(a)
            if a < 40:
                default_dict['1'] += 1 / len(df)
            elif 40 <= a < 80:
                default_dict['2'] += 1 / len(df)
            elif 80 <= a < 120:
                default_dict['3'] += 1 / len(df)
            elif 120 <= a < 160:
                default_dict['4'] += 1 / len(df)
            else:
                default_dict['5'] += 1 / len(df)
    arr = np.array(arr)
    # plot_zhifang(arr)
    print(default_dict)
    
def chef():
    dataset_path = '/Users/clb/Desktop/project/code/paper/dataset/PUBHEALTH/dev.tsv'
    df = pd.read_csv(dataset_path, sep='\t')
    default_dict = defaultdict(int)
    for id, d in tqdm(df.iterrows()):
        default_dict[d['subjects']] += 1
        # d['len_main_text']
    print(default_dict)    

if __name__=='__main__':
    pubhealth()