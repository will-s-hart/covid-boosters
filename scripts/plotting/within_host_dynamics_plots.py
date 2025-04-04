"""
Script to generate plots of within-host dynamics following vaccination.

Plots of log10 antibody titres and relative susceptibility over time following
vaccination are generated, with population average values and 95% prediction interval
endpoints shown. The plots are saved in the `figures/within_host_dynamics` directory.

The `within_host_dynamics.py` script must be run before this script to generate the
underlying results.
"""

import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots(plot_ci=True):
    """
    Make and save the plots.

    Parameters
    ----------
    plot_ci : bool, optional
        Whether to plot the 95% prediction interval around the mean values. Default is
        True.

    Returns
    -------
    None
    """
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
    df["log10_antibodies_mean"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, 361, 60))
    ax.set_ylim(0, 4)
    if plot_ci:
        ax.fill_between(
            df.index,
            df["log10_antibodies_95ci_lower"],
            df["log10_antibodies_95ci_upper"],
            alpha=0.5,
        )
        ax.set_ylim(0, 5)
    ax.set_xlabel("Time since vaccination (days)")
    ax.set_ylabel("log$_{10}$[IgG(S) antibody titre (AU/mL)]")
    plt.savefig(figure_dir / "antibodies.svg")
    # Plot susceptibility dynamics following vaccination
    _, ax = plotting_utils.setup_figure()
    df["susceptibility_mean"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, 361, 60))
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
    plt.savefig(figure_dir / "susceptibility.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots(plot_ci=True)
