import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots(half_protection_antibody_index, plot_ci=True):
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_vacc_effect"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
    figure_dir.mkdir(exist_ok=True, parents=True)

    load_path_within_host = (
        results_dir / f"within_host_{half_protection_antibody_index}.csv"
    )
    load_path_grid_search = (
        results_dir / f"grid_search_{half_protection_antibody_index}.csv"
    )
    load_path_best = results_dir / f"best_{half_protection_antibody_index}.csv"
    load_path_vaccination_time_range_best = (
        results_dir
        / f"vaccination_time_range_best_{half_protection_antibody_index}.csv"
    )
    figure_path_susceptibility = (
        figure_dir / f"susceptibility_{half_protection_antibody_index}.svg"
    )
    figure_path_heatmap = figure_dir / f"heatmap_{half_protection_antibody_index}.svg"
    figure_path_best = figure_dir / f"best_{half_protection_antibody_index}.svg"

    # Plot susceptibility dynamics following vaccination
    df = pd.read_csv(load_path_within_host, index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
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
    plt.savefig(figure_path_susceptibility)
    plt.savefig(str(figure_path_susceptibility).replace(".svg", ".pdf"))

    # Plot heatmap and outbreak risk under optimal vaccination strategy
    optimizing_vaccination_plots.make_plots(
        load_path=load_path_grid_search,
        load_path_best=load_path_best,
        load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
        figure_path_heatmap=figure_path_heatmap,
        figure_path_best=figure_path_best,
        show_plots=False,
    )


if __name__ == "__main__":
    _plot_ci = True
    if "snakemake" in globals():
        make_plots(
            half_protection_antibody_index=int(
                snakemake.wildcards[  # noqa: F821
                    "half_protection_antibody_index"
                ]
            ),
            plot_ci=_plot_ci,
        )
    else:
        for _half_protection_antibody_index in range(2):
            make_plots(_half_protection_antibody_index, plot_ci=_plot_ci)
        plt.show()
