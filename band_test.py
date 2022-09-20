import numpy as np
import matplotlib.pyplot as plt

N, K = 1, 3
data = np.random.rand(N, K)
tick_labels = ["a"]
labels = ["x", "y", "z"]

normalized = data / data.sum(axis=1, keepdims=True)
print(normalized.shape)
cumulative = 0
tick = [0]

for k in range(K):
    color = plt.cm.viridis(float(k) / K, 1)
    plt.barh(tick, normalized[:, k], left=cumulative, color=color, label=labels[k])
    cumulative += normalized[:, k]

plt.xlim((0, 1))
plt.yticks(tick, tick_labels)
plt.legend()
plt.show()