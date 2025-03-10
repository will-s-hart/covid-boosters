"""
Script to make plots of the default analysis of annual COVID-19 vaccination.

Plots of the reproduction number before vaccination and population susceptibility under
vaccination are generated (combined as two subplots of one figure), as well as plots of
the reproduction number with/without vaccination, and of the outbreak risk with and
without vaccination. The plots are saved in the `figures/vaccination_example` directory.

The `vaccination_example.py` script must be run before this script to generate the
underlying results.
"""

import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    """Make and save the plots."""
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/vaccination_example"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df = pd.read_csv(results_dir / "vaccination_example.csv", index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    vaccination_time_range = default_parameters["vaccination_time_range"]
    # Plot reproduction number without vaccination and population-average susceptibility
    _, ax1, ax2 = plotting_utils.setup_figure_subplots()
    df["susceptibility"].plot(ax=ax1)
    plotting_utils.months_x_axis(ax1, period=period, no_periods=2)
    ax1.set_xticklabels([])
    ax1.set_ylim(0.5, 1)
    ax1.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plotting_utils.shade_vaccination_time_range(ax1, vaccination_time_range)
    ax1.set_ylabel("Average\nsusceptibility")
    df["r_unvacc"].plot(ax=ax2)
    plotting_utils.months_x_axis(ax2, period=period, no_periods=2)
    ax2.set_ylim(1.98, 3.02)
    ax2.set_yticks([2, 2.2, 2.4, 2.6, 2.8, 3])
    ax2.set_ylabel("Reproduction number\n(no vaccination)")
    plotting_utils.shade_vaccination_time_range(ax2, vaccination_time_range)
    plt.savefig(figure_dir / "susceptibility_reproduction_number.svg")
    # Plot reproduction number with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df["r_unvacc"].plot(ax=ax, style="--", label="Without vaccination")
    df["r"].plot(ax=ax, label="With vaccination")
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 3.02)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range)
    ax.set_ylabel("Instantaneous reproduction number")
    ax.legend(loc="lower right")
    plt.savefig(figure_dir / "reproduction_number.svg")
    # Plot COR with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df["cor_unvacc"].plot(ax=ax, style="--", label="Without vaccination")
    df["cor"].plot(ax=ax, label="With vaccination")
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range)
    ax.set_ylabel("Outbreak risk")
    ax.legend(loc="lower right")
    plt.savefig(figure_dir / "outbreak_risk.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
