# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:48:46 2024

@author: ingvieb
"""

import matplotlib.pyplot as plt
import pandas as pd



##Graphing with CCFv3 data

dataPath = r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\Allen_Dev_ISH\nutil\LoadSummary_CCFv3-2017.xlsx"

data = pd.read_excel(dataPath)
data = pd.DataFrame(data)
data = data.set_index("Region")

regions = (data.index.values).tolist()

colors = ["#3F631C", 
          "#7ED04B",
          "#9AD2BD",
          "#e32f21",
          "#98D6F9",
          "#FF9B88",
          "#ff70a4",
          "#F0F080"]
          
plt.figure(figsize=(12,6))

for region, color in zip(regions, colors):
    plt.plot(data.loc[region], color=color, label=region, linewidth=2)

plt.legend(loc='upper right')
plt.xlabel('Age')
plt.ylabel('Calbindin neuron load')
plt.title('Calbindin neuron load analyzed with CCFv3-2017')
plt.ylim(0,0.1)
plt.savefig("Load_CCFv3.svg")



##Graphing with KimLabDevCCFv001 data

dataPath = r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\Allen_Dev_ISH\nutil\LoadSummary_KimLabDevCCFv001.xlsx"

data = pd.read_excel(dataPath)
data = pd.DataFrame(data)
data = data.set_index("Region")

regions = (data.index.values).tolist()

colors = ["#A84D10", 
          "#fff17b",
          "#0e6f0e",
          "#00D100",
          "#EA37FF",
          "#9442FF",
          "#37A7FF",
          "#12D9B9"]
          
plt.figure(figsize=(12,6))

for region, color in zip(regions, colors):
    plt.plot(data.loc[region], color=color, label=region, linewidth=2)

plt.legend(loc='upper right')
plt.xlabel('Age')
plt.ylabel('Calbindin neuron load')
plt.title('Calbindin neuron load analyzed with KimLabDevCCFv001')
plt.ylim(0,0.1)
plt.savefig("Load_KimLabDevCCFv001.svg")

















