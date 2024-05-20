import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/input"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the inputs
    default_parameters = get_default_parameters()
    generation_time_dist = default_parameters["generation_time_dist"]
    # Plot the generation time distribution
    _, ax = plotting_utils.setup_figure()
    ax.bar(
        generation_time_dist.xk,
        generation_time_dist.pk,
        width=1,
        color="black",
        alpha=0.25,
    )
    ax.set_xlim(-0.5, 10.5)
    ax.set_xticks(np.arange(0, 11, 2))
    ax.set_xlabel("Generation time (days)")
    ax.set_ylabel("Probability")
    plt.savefig(figure_dir / "generation_time.pdf")
    plt.savefig(figure_dir / "generation_time.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
