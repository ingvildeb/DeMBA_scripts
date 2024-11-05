import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load the data
datapath = "../data_files/"

ages = ["P28", "P21", "P14", "P07", "P04"]

colours = pd.read_csv(f"{datapath}/points_hierarchies.csv")
colour_map = {
    "Isocortex": "#3F631C",
    "Hippocampal formation": "#7ED04B",
    "Olfactory areas": "#9AD2BD",
    "Hypothalamus": "#E32F21",
    "Cerebral nuclei": "#98D6F9",
    "Midbrain, hindbrain, medulla": "#FF9B88",
    "Thalamus": "#FF70A4",
    "Cerebellum": "#F0F080",
    "Fibre Tracts": "#CCCCCC",
    "Ventricular System": "#AAAAAA",
    "out of brain": "#000000",
}

for age in ages:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(f"{datapath}/iterative_{age}.csv")
    # Ensure the colours DataFrame and df are in sync
    merged_df = df.merge(colours, left_on="Acronym", right_on="point name", how="left")
    # Filter the data to focus on the "DeMBA" column
    data = merged_df[["hierarchical_region", "Distance DeMBA to others"]]
    data = data.rename(columns={"Distance DeMBA to others": "DeMBA"})
    data['DeMBA'] = data['DeMBA'] * 20
    
    # Group the data by hierarchical region
    grouped_data = data.groupby("hierarchical_region").mean().reset_index()
    #convert to mictons
    # Define the order of hierarchical regions
    order = grouped_data["hierarchical_region"]

    # Create the plot
    plt.figure(figsize=(12, 8))
    sns.barplot(
        x="hierarchical_region",
        y="DeMBA",
        data=grouped_data,
        palette=colour_map,
        edgecolor="black",
        order=order,  # Ensure consistent order
    )

    # Overlay individual data points
    sns.swarmplot(
        x="hierarchical_region",
        y="DeMBA",
        data=data,
        color="white",
        edgecolor="black",  # Add hard outline
        linewidth=0.5,  # Set the width of the outline
        order=order,  # Ensure consistent order
    )

    # Customize the plot
    plt.title(f"{age} DeMBA Distance per Region")
    plt.xlabel("Hierarchical Region")
    plt.ylabel("Mean DeMBA Distance (microns)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    # Save the plot as an SVG file
    plt.savefig(f"{datapath}/demba_distance_per_region_{age}.svg", format="svg")
    plt.show()

# Create a separate legend plot
fig_legend = plt.figure(figsize=(8, 6))
ax_legend = fig_legend.add_subplot(111)
handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10)
    for color in colour_map.values()
]
labels = colour_map.keys()
ax_legend.legend(handles, labels, loc="center")
ax_legend.axis("off")
plt.savefig(f"{datapath}/legend_plot.svg", format="svg")
plt.show()