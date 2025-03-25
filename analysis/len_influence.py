import matplotlib.pyplot as plt
import numpy as np

x_labels = ['&lt;40', '40-80', '80-120', '120-160', '&gt;=160']
x = np.arange(len(x_labels))

macro_f1_gpt_4o = [46.25, 66.28, 68.50, 67.35, 71.10]
macro_f1_gpt_4o_mini = [36.65, 61.04, 58.40, 57.04, 53.38]

ratio = [4, 54, 23, 10, 9]

fig, ax1 = plt.subplots()

ax1.plot(x, macro_f1_gpt_4o, 'o--', label='gpt-4o', color='orange')
ax1.plot(x, macro_f1_gpt_4o_mini, 's--', label='gpt-4o-mini', color='green')

ax1.set_xlabel('Length of the Claim')
ax1.set_ylabel('Macro F1', color='black')
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels)
ax1.tick_params(axis='y', labelcolor='black')

ax2 = ax1.twinx()  
ax2.bar(x, ratio, alpha=0.2, color='purple', width=0.4, label='Ratio')

ax2.set_ylabel('Ratio (%)', color='purple')
ax2.set_ylim(0, 100)
ax2.tick_params(axis='y', labelcolor='purple')

lines, labels = ax1.get_legend_handles_labels()
bars, blabels = ax2.get_legend_handles_labels()
ax1.legend(lines + bars, labels + blabels, loc='upper left')

for i, v in enumerate(ratio):
    ax2.text(i, v + 1, f'{v}%', ha='center', va='bottom')

plt.title('Macro F1 vs Length of the Claim')
plt.tight_layout()
# plt.show()
plt.savefig('./pics/influence_len_v2.pdf')