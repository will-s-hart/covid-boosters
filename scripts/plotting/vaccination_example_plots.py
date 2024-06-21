import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/vaccination_example"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df = pd.read_csv(results_dir / "vaccination_example.csv", index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    vaccination_time_range = default_parameters["vaccination_time_range"]
    # Plot population-average susceptibility
    _, ax = plotting_utils.setup_figure()
    df["susceptibility"].plot(ax=ax)
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 1)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range)
    ax.set_ylabel("Average susceptibility")
    plt.savefig(figure_dir / "susceptibility.svg")
    # Plot reproduction number with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df["r_unvacc"].plot(ax=ax, label="Without vaccination")
    df["r"].plot(ax=ax, label="With vaccination")
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 3.02)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range)
    ax.set_ylabel("Instantaneous reproduction number")
    ax.legend(loc="lower right")
    plt.savefig(figure_dir / "reproduction_number.svg")
    # Plot COR with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df["cor_unvacc"].plot(ax=ax, label="Without vaccination")
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
