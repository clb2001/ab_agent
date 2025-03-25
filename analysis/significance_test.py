import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

np.random.seed(42)  

true_data = np.random.randint(2, 6, (100, 8))
false_data = np.random.randint(1, 6, (100, 8))

labels = ['Alignment', 'Causality Confusion', 'Accuracy', 'Generalization', 
          'Contextual Fidelity', 'SGC', 'WGC', 'LC']

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
plt.savefig('./pics/significance_test.pdf', format='pdf')

