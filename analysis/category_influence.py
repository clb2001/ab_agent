import matplotlib.pyplot as plt
import numpy as np

categories = ['Society', 'Science', 'Health', 'Politics', 'Culture']
macro_f1_gpt_4o = [63.37, 72.87, 65.47, 70.07, 69.98]
macro_f1_gpt_4o_mini = [60.52, 68.80, 58.39, 60.86, 53.41]
bar_width = 0.2
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]
plt.figure(figsize=(10, 5))
plt.bar(r1, macro_f1_gpt_4o, color='orange', width=bar_width, edgecolor='grey', label='gpt-4o')
plt.bar(r2, macro_f1_gpt_4o_mini, color='green', width=bar_width, edgecolor='grey', label='gpt-4o-mini')
plt.xlabel('Category', fontweight='bold')
plt.ylabel('Macro F1', fontweight='bold')
plt.xticks([r + bar_width*0.5 for r in range(len(categories))], categories)
plt.title('Macro F1 by Category')
plt.legend()
plt.tight_layout()
plt.savefig('./pics/influence_category_v2.pdf')
