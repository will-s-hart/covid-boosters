import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots(plot_ci=True):
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/within_host_dynamics"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df = pd.read_csv(results_dir / "within_host_dynamics.csv", index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    # Plot antibody dynamics following vaccination
    _, ax = plotting_utils.setup_figure()
    df["antibodies_mean"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, period + 1, period / 6))
    ax.set_ylim(0, 4000)
    if plot_ci:
        ax.fill_between(
            df.index,
            df["antibodies_95ci_lower"],
            df["antibodies_95ci_upper"],
            alpha=0.5,
        )
        ax.set_ylim(0, 14000)
    ax.set_xlabel("Time since vaccination (days)")
    ax.set_ylabel("IgG(S) antibody titre (AU/mL)")
    plt.savefig(figure_dir / "antibodies.pdf")
    plt.savefig(figure_dir / "antibodies.svg")
    # Plot susceptibility dynamics following vaccination
    _, ax = plotting_utils.setup_figure()
    df["susceptibility_mean"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, period + 1, period / 6))
    ax.set_ylim(0, 1)
    if plot_ci:
        ax.fill_between(
            df.index,
            df["susceptibility_95ci_lower"],
            df["susceptibility_95ci_upper"],
            alpha=0.5,
        )
        ax.set_xlabel("Time since vaccination (days)")
    ax.set_ylabel("Relative susceptibility")
    plt.savefig(figure_dir / "susceptibility.pdf")
    plt.savefig(figure_dir / "susceptibility.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots(plot_ci=True)
