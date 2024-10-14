import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load the data
datapath = "../data_files/"
df = pd.read_csv(f"{datapath}/iterative_P28.csv")

# Extract the data
Ing = df["Distance Ingvild to others"]
Dem = df["Distance DeMBA to others"]
Sim = df["Distance Simon to others"]
Hei = df["Distance Heidi to others"]

# Combine the data into a DataFrame for easier plotting
data = pd.DataFrame({
    'Ingvild': Ing,
    'DeMBA': Dem,
    'Simon': Sim,
    'Heidi': Hei
})

# Create the bar plot using median
plt.figure(figsize=(10, 6))
sns.barplot(data=data, ci=None, palette="muted", estimator=np.median)

# Add the scatter plot
for i, column in enumerate(data.columns):
    sns.stripplot(x=[column]*len(data), y=data[column], color='black', alpha=0.5, jitter=True)

# Customize the plot
plt.yscale('symlog', linthresh=50)
plt.ylim(0, 70)  # Set the y-axis limits to truncate the empty space
plt.title('Distances to Others (Log Scale for Values > 50, Median)')
plt.ylabel('Distance')
plt.xlabel('Individuals')
plt.show()