import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/within_host_example"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df = pd.read_csv(results_dir / "within_host_example.csv", index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    # Plot antibody dynamics following vaccination
    _, ax = plotting_utils.setup_figure()
    df["antibodies"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, period + 1, period / 6))
    ax.set_ylim(0, 3500)
    ax.set_xlabel("Time since vaccination (days)")
    ax.set_ylabel("Antibody titre (AU)")
    plt.savefig(figure_dir / "antibodies.pdf")
    plt.savefig(figure_dir / "antibodies.svg")
    # Plot susceptibility dynamics following vaccination
    _, ax = plotting_utils.setup_figure()
    df["susceptibility"].plot(ax=ax)
    ax.set_xlim(0, period)
    ax.set_xticks(np.arange(0, period + 1, period / 6))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time since vaccination (days)")
    ax.set_ylabel("Relative susceptibility")
    plt.savefig(figure_dir / "susceptibility.pdf")
    plt.savefig(figure_dir / "susceptibility.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
