import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import ttest_rel
import warnings

# Suppress specific warnings
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="Passing `palette` without assigning `hue` is deprecated.",
)
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Ignoring `palette` because no `hue` variable has been assigned.",
)
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="use_inf_as_na option is deprecated and will be removed in a future version.",
)
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="When grouping with a length-1 list-like, you will need to pass a length-1 tuple to get_group in a future version of pandas.",
)

datapath = "../data_files/"

ages = ["P28", "P21", "P14", "P07", "P04"]

colours = pd.read_csv(f"{datapath}/points_hierarchies.csv")

colours = colours.loc[:, ~colours.columns.str.contains("^Unnamed")]
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

    # Create the colour list based on the merged DataFrame
    colour_list = [
        colour_map.get(region, "#FFFFFF") for region in merged_df["hierarchical_region"]
    ]
    # Extract the data
    Ing = df["Distance Ingvild to others"]
    Dem = df["Distance DeMBA to others"]
    Sim = df["Distance Simon to others"]
    Hei = df["Distance Heidi to others"]
    Har = df["Distance Harry to others"]

    mean_human = np.mean([Ing, Sim, Hei, Har], axis=0)
    # Combine the data into a DataFrame for easier plotting
    data = pd.DataFrame(
        {
            "Rater 1": Ing,
            "Rater 2": Sim,
            "Rater 3": Hei,
            "Rater 4": Har,
            "Average of humans": mean_human,
            "DeMBA": Dem,
        }
    )
    # convert the data from voxels to microns
    data = data * 20

    # Perform paired samples t-test
    nans = np.isnan(mean_human) | np.isnan(Dem)
    t_stat, p_value = ttest_rel(mean_human[~nans], Dem[~nans])

    # Define the thresholds for the broken axis
    lower_threshold = 650
    upper_threshold = 6000
    buffer = 50  # Add a buffer to ensure points are not cropped

    # Create the figure and two subplots with height ratios
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3], hspace=0.05)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    # Plot the bar plot on the subplot(s)
    bars1 = sns.barplot(
        data=data, errorbar=None, palette="muted", estimator=np.mean, ax=ax1
    )
    bars2 = sns.barplot(
        data=data, errorbar=None, palette="muted", estimator=np.mean, ax=ax2
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
    # Add the scatter plot on the subplot(s) using swarmplot to avoid overlap
    for i, column in enumerate(data.columns):
        # Filter data points for the bottom graph
        data_bottom = data[data[column] <= lower_threshold]
        sns.swarmplot(
            x=[column] * len(data_bottom),
            y=data_bottom[column],
            hue=merged_df["hierarchical_region"][data[column] <= lower_threshold],
            palette=colour_map,
            alpha=1,
            ax=ax2,
            legend=False,
            edgecolor="black",  # Add hard outline
            linewidth=0.5,  # Set the width of the outline
            clip_on=False,  # Allow points to be drawn outside the axes limits
        )

        # Filter data points for the top graph
        data_top = data[data[column] > lower_threshold]
        sns.swarmplot(
            x=[column] * len(data_top),
            y=data_top[column],
            hue=merged_df["hierarchical_region"][data[column] > lower_threshold],
            palette=colour_map,
            alpha=1,
            ax=ax1,
            legend=False,
            edgecolor="black",  # Add hard outline
            linewidth=0.5,  # Set the width of the outline
            clip_on=False,  # Allow points to be drawn outside the axes limits
        )

    # Annotate the bars with the mean values, offset to the left
    for p in ax1.patches:
        ax1.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(-30, 9),  # Offset to the left
            textcoords="offset points",
        )

    for p in ax2.patches:
        ax2.annotate(
            f"{p.get_height():.1f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(-30, 9),  # Offset to the left
            textcoords="offset points",
        )
    # Annotate the plot with the p-value and significance
    significance = (
        "ns"
        if p_value > 0.05
        else "*" if p_value <= 0.05 else "**" if p_value <= 0.01 else "***"
    )

    # Add lines to show which bars are being compared
    x1, x2 = 4, 5  # Indices of the bars being compared (Average of humans and DeMBA)
    y, h, col = upper_threshold - 2000, 200, "k"
    ax1.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c=col)
    ax1.plot([x1, x1], [y, y - h], lw=1.5, c=col)  # Left vertical line pointing down
    ax1.plot([x2, x2], [y, y - h], lw=1.5, c=col)  # Right vertical line pointing down
    ax1.text(
        (x1 + x2) * 0.5,
        y + h + 200,
        f"p = {p_value:.3f} ({significance})",
        ha="center",
        va="bottom",
        color=col,
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
    ax1.set_title(f"{age} Mean Error")
    # ax2.set_xlabel("Individuals")
    ax1.set_ylabel("")
    ax2.set_ylabel("")
    # Add a centered y-axis label
    fig.text(
        0.04,
        0.5,
        "Distance to median of others (microns)",
        va="center",
        rotation="vertical",
    )
    # Save the plot as an SVG file
    plt.savefig(f"{datapath}/two_scale_plot_{age}.svg", format="svg")
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
