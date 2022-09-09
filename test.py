import pandas as pd
import seaborn as sns
import scipy as sp
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

labels = ['this is some really really long label text, so long that it is much better read horizontally',
          'and another really long label, this could probably be very much reduced',
          'a short label for a change',
          'lorem ipsum',
          'and another really long and very descriptive label, including some abbreviations a.n.g']

Df = pd.DataFrame(sp.randn(len(labels),10))
Df['labels'] = labels

# fig, ax = plt.subplots()
plt.figure(figsize=(10, 10))
ax = sns.boxplot(data=Df.melt(id_vars='labels'),x='labels',y='value', orient='v', width=0.5, linewidth=1.5, fliersize=0)
# ax.set_xticklabels('')

# leg_handles = []
# for label,artist in zip(labels,ax.artists):
#     handle = mpatches.Patch(facecolor=artist.get_facecolor(),label=label)
#     leg_handles.append(handle)

# ax.legend(handles=leg_handles,bbox_to_anchor=(0., 1.82, 1., 2), loc=3, ncol=5, mode="expand", borderaxespad=0.)
# fig.subplots_adjust(top=0.5)
# plt.show()

ax.tick_params(labelsize=14)
ax.set_ylabel("Número de escanteios",fontsize=15)
ax.set_xlabel("",fontsize=1)
ax.set_xticklabels(labels,rotation=90,fontsize=14)
# ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, horizontalalignment = 'center')
plt.show()
