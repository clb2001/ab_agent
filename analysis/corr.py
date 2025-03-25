import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
data = np.random.rand(100, 8) 
columns = ['alignment', 'causality', 'accuracy', 'generalization', 'fidelity', 'SGC', 'WGC', 'LC']
df = pd.DataFrame(data, columns=columns)

corr_matrix = df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title('Correlation Matrix of Features')
# plt.show()
plt.savefig('./pics/corr.pdf', format='pdf')
