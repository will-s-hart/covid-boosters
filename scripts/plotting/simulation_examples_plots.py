import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results/simulation_examples"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/simulation_examples"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df_simulations = pd.read_csv(results_dir / "simulations.csv", index_col="time")
    incidence_cutoff = 10
    # Plot simulations
    simulations_plot = [0, 1, 2, 3, 21, 15, 10, 11, 4, 5]
    x_max = 16
    fig, axs = plt.subplots(2, 5, sharex=True, sharey=True)
    fig.supxlabel("Day of outbreak", y=0.27)
    fig.supylabel("Incidence", x=0.04)
    for ax in axs.flat:
        ax.set_box_aspect(1)
        ax.xaxis.label.set_fontsize(12)
        ax.yaxis.label.set_fontsize(12)
        ax.tick_params(axis="both", which="major", labelsize=12)
        ax.set_xlim(0, x_max)
        ax.set_xticks(np.arange(0, 16, 5))
        ax.set_ylim(0, incidence_cutoff)
        ax.set_yticks(np.arange(0, incidence_cutoff + 1, 2))
    fig.subplots_adjust(top=0.65, bottom=0.35)
    for simulation, ax in zip(simulations_plot, axs.flat):
        x = np.arange(x_max + 1)
        y = df_simulations.loc[x, f"{simulation}"]
        x_first = np.argmax(y >= incidence_cutoff)
        if x_first > 0:
            x = x[: x_first + 1]
            y = y[: x_first + 1]
            color = "tab:red"
            clip_on = True
        else:
            color = "tab:blue"
            clip_on = False
        ax.plot(x, y, color=color, linewidth=2, zorder=10, clip_on=clip_on)
    plt.xlim(0, x_max)
    plt.ylim(0, incidence_cutoff)
    plt.savefig(figure_dir / "simulations.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
