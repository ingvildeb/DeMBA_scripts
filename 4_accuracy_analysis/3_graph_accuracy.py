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
    "Fibre Tracts":"#CCCCCC",
    "Ventricular System":"#AAAAAA",
    "unknown":"#000000",
    "out of brain":"#000000"
}

for age in ages:

    # Read the CSV file into a DataFrame
    df = pd.read_csv(f"{datapath}/iterative_{age}.csv")

    # Ensure the colours DataFrame and df are in sync
    merged_df = df.merge(colours, left_on='Acronym', right_on='point name', how='left')

    # Create the colour list based on the merged DataFrame
    colour_list = [colour_map.get(region, "#FFFFFF") for region in merged_df['hierarchical_region']]
    # Extract the data
    Ing = df["Distance Ingvild to others"]
    Dem = df["Distance DeMBA to others"]
    Sim = df["Distance Simon to others"]
    Hei = df["Distance Heidi to others"]
    Har = df["Distance Harry to others"]

    # Combine the data into a DataFrame for easier plotting
    data = pd.DataFrame({"Rater 1": Ing, "Rater 2": Sim, "Rater 3": Hei, "Rater 4": Har, "DeMBA": Dem})
    data = data * 20

    # Define the thresholds for the broken axis
    lower_threshold = 650
    upper_threshold = 9000
    buffer = 50  # Add a buffer to ensure points are not cropped

    # Create the figure and two subplots with height ratios
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3], hspace=0.05)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    # Plot the bar plot on the subplot(s)
    bars1 = sns.barplot(
        data=data, errorbar=None, palette="muted", estimator=np.median, ax=ax1
    )
    bars2 = sns.barplot(
        data=data, errorbar=None, palette="muted", estimator=np.median, ax=ax2
    )

    # Customize the bars to have white face color and black edge color
    for bar in bars1.patches:
        bar.set_facecolor("white")
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    for bar in bars2.patches:
        bar.set_facecolor("white")
        bar.set_edgecolor("black")
        bar.set_linewidth(1)

    # Add the scatter plot on the subplot(s) using swarmplot to avoid overlap
    for i, column in enumerate(data.columns):
        # Filter data points for the bottom graph
        data_bottom = data[data[column] <= lower_threshold]
        sns.swarmplot(
            x=[column] * len(data_bottom),
            y=data_bottom[column],
            hue=colours['hierarchical_region'][data[column] <= lower_threshold],
            palette=colour_map,
            alpha=1,
            ax=ax2,
            legend=False,
            edgecolor="black",  # Add hard outline
            linewidth=0.5,  # Set the width of the outline
            clip_on=False  # Allow points to be drawn outside the axes limits
        )

        # Filter data points for the top graph
        data_top = data[data[column] > lower_threshold]
        sns.swarmplot(
            x=[column] * len(data_top),
            y=data_top[column],
            hue=colours['hierarchical_region'][data[column] > lower_threshold],
            palette=colour_map,
            alpha=1,
            ax=ax1,
            legend=False,
            edgecolor="black",  # Add hard outline
            linewidth=0.5,  # Set the width of the outline
            clip_on=False  # Allow points to be drawn outside the axes limits
        )

    # Annotate the bars with the median values, offset to the left
    for p in ax1.patches:
        ax1.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(-40, 9),  # Offset to the left
            textcoords="offset points",
        )

    for p in ax2.patches:
        ax2.annotate(
            f"{p.get_height():.1f}", 
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(-40, 9),  # Offset to the left
            textcoords="offset points",
        )

    # Set the y-axis limits
    ax1.set_ylim(
        lower_threshold - buffer, upper_threshold + buffer
    )  # Add buffer to lower and upper limits
    ax2.set_ylim(0, lower_threshold)

    # Hide the spines between ax1 and ax2
    ax1.spines["bottom"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # Don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    # Add a straight dotted red line to indicate the separation
    ax1.axhline(y=lower_threshold, color="red", linestyle="--", linewidth=1)
    ax2.axhline(y=lower_threshold, color="red", linestyle="--", linewidth=1)

    # Set y-ticks automatically and ensure lower_threshold is included
    y_ticks_bottom = np.arange(0, lower_threshold, 200).tolist()
    if lower_threshold not in y_ticks_bottom:
        y_ticks_bottom.append(lower_threshold)
    ax2.set_yticks(y_ticks_bottom)

    y_ticks_top = np.arange(lower_threshold, upper_threshold + buffer + 1000, 1000)
    ax1.set_yticks(y_ticks_top)

    # Customize the plot
    ax1.set_title(f"{age} Median Error")
    # ax2.set_xlabel("Individuals")
    ax1.set_ylabel("")
    ax2.set_ylabel("")
    # Add a centered y-axis label
    fig.text(
        0.04,
        0.5,
        "Distance to mean of others (microns)",
        va="center",
        rotation="vertical",
    )
    # Save the plot as an SVG file
    plt.savefig(f"{datapath}/two_scale_plot_{age}.svg", format="svg")

    plt.show()

# Create a separate legend plot
fig_legend = plt.figure(figsize=(8, 6))
ax_legend = fig_legend.add_subplot(111)
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colour_map.values()]
labels = colour_map.keys()
ax_legend.legend(handles, labels, loc='center')
ax_legend.axis('off')
plt.savefig(f"{datapath}/legend_plot.svg", format="svg")
plt.show()