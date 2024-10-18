import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load the data
datapath = "../data_files/"

ages = ["P28", "P21", "P14"]
for age in ages:
    df = pd.read_csv(f"{datapath}/iterative_{age}.csv")

    # Extract the data
    Ing = df["Distance Ingvild to others"]
    Dem = df["Distance DeMBA to others"]
    Sim = df["Distance Simon to others"]
    Hei = df["Distance Heidi to others"]

    # Combine the data into a DataFrame for easier plotting
    data = pd.DataFrame({
        'Rater 1': Ing,
        'Rater 2': Sim,
        'Rater 3': Hei,
        'DeMBA': Dem
    })
    data = data * 20

    truncation_thresholds = {
        "P28": 1000,
        "P21": np.nan,
        "P14": 2000
    }

    # Switch to enable or disable truncation
    truncation_threshold = truncation_thresholds[age]  # Set the threshold for truncation
    enable_truncation = True if not pd.isna(truncation_threshold) else False

    if enable_truncation:
        # Create the figure and two subplots with height ratios
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 3]})
    else:
        # Create the figure with a single subplot
        fig, ax1 = plt.subplots(1, 1, figsize=(10, 8))

    # Plot the bar plot on the subplot(s)
    sns.barplot(data=data, ci=None, palette="muted", estimator=np.median, ax=ax1)
    if enable_truncation:
        sns.barplot(data=data, ci=None, palette="muted", estimator=np.median, ax=ax2)

    # Add the scatter plot on the subplot(s)
    for i, column in enumerate(data.columns):
        sns.stripplot(x=[column]*len(data), y=data[column], color='black', alpha=0.5, jitter=True, ax=ax1)
        if enable_truncation:
            sns.stripplot(x=[column]*len(data), y=data[column], color='black', alpha=0.5, jitter=True, ax=ax2)

    if enable_truncation:
        # Set the y-axis limits to exclude the range above the threshold
        ax1.set_ylim(truncation_threshold, data.max().max() + 600)  # Adjust the upper limit as needed
        ax2.set_ylim(0, truncation_threshold)

        # Hide the spines between ax1 and ax2
        ax1.spines['bottom'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.xaxis.tick_top()
        ax1.tick_params(labeltop=False)  # Don't put tick labels at the top
        ax2.xaxis.tick_bottom()

        # Add diagonal lines to indicate the break
        d = .015  # How big to make the diagonal lines in axes coordinates
        kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
        ax1.plot((-d, +d), (-d, +d), **kwargs)        # Top-left diagonal
        ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # Top-right diagonal

        kwargs.update(transform=ax2.transAxes)  # Switch to the bottom axes
        ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # Bottom-left diagonal
        ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # Bottom-right diagonal

        # Set y-ticks every 200 increments
        ax2.set_yticks(np.arange(0, truncation_threshold + 600, 200))
    else:
        # Set the y-axis limits to the full range
        ax1.set_ylim(0, data.max().max() + 200)
        # Set y-ticks every 200 increments
        ax1.set_yticks(np.arange(0, data.max().max() + 200, 200))

    # Customize the plot
    ax1.set_title(f'{age} Median Error')
    if enable_truncation:
        ax2.set_xlabel('Individuals')
        ax1.set_ylabel('')
        ax2.set_ylabel('')
    else:
        ax1.set_ylabel('')
        ax1.set_xlabel('Individuals')

    # Add a centered y-axis label
    fig.text(0.04, 0.5, 'Distance to mean of others (microns)', va='center', rotation='vertical')

    # Save the plot as an SVG file
    plt.savefig(f"{datapath}/plot_{age}.svg", format='svg')

    plt.show()