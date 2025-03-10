"""
Script to generate plots of effect of the dispersion parameter on superspreading.

Plots of the individual reproduction number distribution and the contribution to
transmission vs proportion of cases are generated for different values of the
dispersion parameter of the negative binomial offspring distribution, k. The plots are
saved in the `figures/superspreading` directory.
"""

import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import gamma

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    """Make and save the plots."""
    plotting_utils.set_sns_theme()
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/superspreading"
    figure_dir.mkdir(exist_ok=True, parents=True)
    default_parameters = get_default_parameters()
    # Plot comparison of individual reproduction number distributions for different
    # values of the dispersion parameter
    dispersion_param_vals = [0.1, default_parameters["dispersion_param"], 1, 10, 100]
    color_vals = [sns.color_palette("colorblind")[i] for i in [3, 0, 2, 1, 9]]
    inf_factor_vec = np.linspace(0, 40, 10000)
    _, ax = plotting_utils.setup_figure()
    for dispersion_param, color in zip(dispersion_param_vals, color_vals):
        density_vec = gamma.pdf(
            inf_factor_vec, dispersion_param, scale=1 / dispersion_param
        )
        ax.plot(
            inf_factor_vec,
            density_vec,
            color=color,
            label="$\\it{k}$ = " + str(dispersion_param),
        )
    ax.plot(
        [1, 1], [0, 5], color="black", linestyle="--", label="$\\it{k}$ = $\\infty$"
    )
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 5)
    ax.set_xlabel("Relative individual infectiousness, $\\alpha$")
    ax.set_ylabel("Density")
    ax.legend()  # loc="upper right")
    plt.savefig(figure_dir / "infectiousness_factors.svg")
    # Plot contribution to transmission vs proportion of cases for different values of
    # the dispersion parameter
    _, ax = plotting_utils.setup_figure()
    for dispersion_param, color in zip(dispersion_param_vals, color_vals):
        prop_cases_vec = gamma.sf(
            inf_factor_vec, dispersion_param, scale=1 / dispersion_param
        )
        prop_transmission_vec = gamma.sf(
            inf_factor_vec, dispersion_param + 1, scale=1 / dispersion_param
        )
        ax.plot(
            prop_cases_vec,
            prop_transmission_vec,
            color=color,
            label="$\\it{k}$ = " + str(dispersion_param),
        )
    ax.plot(
        [0, 1], [0, 1], color="black", linestyle="--", label="$\\it{k}$ = $\\infty$"
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.set_xlabel("Most infectious proportion of cases")
    ax.set_ylabel("Proportion of transmissions")
    ax.legend()
    plt.savefig(figure_dir / "transmission_proportions.svg")
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
