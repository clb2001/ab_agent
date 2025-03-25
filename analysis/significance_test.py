import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

true_data = []
false_data = []
arr = []
with open('/Users/clb/Desktop/project/code/paper/experiment/res/classification_gpt-4o-2024-08-06.json') as f:
    data = json.load(f)

for d in data:
    if d['response_classification'] is not None and d['response_get_score'] is not None and d['label'] == 'true':
        true_data.append([
            d['alignment'],
            d['causality_confusion'],
            d['accuracy'],
            d['generalization'],
            d['contextual_fidelity'],
            d['SGC'],
            d['WGC'],
            d['LC']
        ])
    elif d['response_classification'] is not None and d['response_get_score'] is not None and d['label'] == 'false':
        false_data.append([
            d['alignment'],
            d['causality_confusion'],
            d['accuracy'],
            d['generalization'],
            d['contextual_fidelity'],
            d['SGC'],
            d['WGC'],
            d['LC']
        ])        

labels = ['Alignment', 'Causality', 'Accuracy', 'Generalization', 
          'Fidelity', 'SGC', 'WGC', 'LC']
true_data = np.array(true_data)
false_data = np.array(false_data)

# 进行Mann-Whitney U检验
results = {}
for i, label in enumerate(labels):
    stat, p_value = mannwhitneyu(true_data[:, i], false_data[:, i])
    results[label] = p_value

for label, p_value in results.items():
    print(f"{label}: p-value = {p_value}")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, label in enumerate(labels):
    axes[i].boxplot([true_data[:, i], false_data[:, i]], labels=['True', 'False'])
    axes[i].set_title(label)

plt.tight_layout()
plt.savefig('./pics/significance_test_v2.pdf', format='pdf')

