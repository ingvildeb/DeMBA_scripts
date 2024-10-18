import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load the data
datapath = "../data_files/"

ages = ["P28", "P21", "P14"]
all_data = []

# Load all data and find global min and max
for age in ages:
    df = pd.read_csv(f"{datapath}/iterative_{age}.csv")
    Ing = df["Distance Ingvild to others"]
    Dem = df["Distance DeMBA to others"]
    Sim = df["Distance Simon to others"]
    Hei = df["Distance Heidi to others"]
    data = pd.DataFrame({"Rater 1": Ing, "Rater 2": Sim, "Rater 3": Hei, "DeMBA": Dem})
    all_data.append(data * 20)

# Concatenate all data to find global min and max
combined_data = pd.concat(all_data)
global_min = combined_data.min().min()
global_max = combined_data.max().max()

# Plot each age with the same y-scale
for age, data in zip(ages, all_data):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot the bar plot
    sns.barplot(data=data, ci=None, palette="muted", estimator=np.median, ax=ax)

    # Add the scatter plot
    for i, column in enumerate(data.columns):
        sns.stripplot(
            x=[column] * len(data),
            y=data[column],
            color="black",
            alpha=0.5,
            jitter=True,
            ax=ax,
        )

    # Set the y-axis to log scale and same limits
    ax.set_yscale("log")
    ax.set_ylim(global_min, global_max + 1000)

    # Customize the plot
    ax.set_title(f"{age} Median Error")
    ax.set_xlabel("Individuals")
    ax.set_ylabel("Distance to mean of others (microns)")

    # Save the plot as an SVG file
    plt.savefig(f"{datapath}/plot_{age}_log.svg", format="svg")

    plt.show()
