import matplotlib.pyplot as plt
import numpy as np

categories = ['Society', 'Science', 'Health', 'Politics', 'Culture']
macro_f1_gpt_4o = [74.7, 65.5, 67.2, 73.3, 75.2]
macro_f1_gpt_4o_mini = [72.1, 61.8, 63.2, 69.5, 71.3]


# 条形图的宽度和位置
bar_width = 0.2
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]

# 绘制条形图
plt.figure(figsize=(10, 5))
plt.bar(r1, macro_f1_gpt_4o, color='orange', width=bar_width, edgecolor='grey', label='gpt-4o')
plt.bar(r2, macro_f1_gpt_4o_mini, color='green', width=bar_width, edgecolor='grey', label='gpt-4o-mini')

# 添加标签、标题和图例
plt.xlabel('Category', fontweight='bold')
plt.ylabel('Macro F1', fontweight='bold')
plt.xticks([r + bar_width*0.5 for r in range(len(categories))], categories)
plt.title('Macro F1 by Category')
plt.legend()

# 展示图形
plt.tight_layout()
plt.savefig('./pics/influence_category.pdf')
