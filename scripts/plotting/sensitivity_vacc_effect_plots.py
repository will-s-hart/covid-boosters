import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts import sensitivity_vacc_effect
from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    color_palette = sns.color_palette()
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
    figure_dir.mkdir(exist_ok=True, parents=True)
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    vaccination_time_range_default = default_parameters["vaccination_time_range"]
    fig_sus, ax_sus = plotting_utils.setup_figure()
    fig_cor_default, ax_cor_default = plotting_utils.setup_figure()
    for half_protection_antibody_index in [0, "baseline", 1]:
        if half_protection_antibody_index == "baseline":
            half_protection_antibody = default_parameters["susceptibility_func_params"][
                "half_protection_antibody"
            ]
            color = color_palette[0]
            results_dir = pathlib.Path(__file__).parents[2] / "results"
            load_path_within_host = results_dir / "within_host_dynamics.csv"
            load_path_default = results_dir / "vaccination_example.csv"
            load_path_grid_search = (
                results_dir / "optimizing_vaccination/grid_search.csv"
            )
            load_path_best = results_dir / "optimizing_vaccination/best.csv"
            load_path_vaccination_time_range_best = (
                results_dir / "optimizing_vaccination/vaccination_time_range_best.csv"
            )
        else:
            half_protection_antibody = (
                sensitivity_vacc_effect.half_protection_antibody_vals[
                    half_protection_antibody_index
                ]
            )
            color = color_palette[half_protection_antibody_index + 1]
            results_dir = (
                pathlib.Path(__file__).parents[2] / "results/sensitivity_vacc_effect"
            )
            load_path_within_host = (
                results_dir / f"within_host_{half_protection_antibody_index}.csv"
            )
            load_path_default = (
                results_dir / f"default_{half_protection_antibody_index}.csv"
            )
            load_path_grid_search = (
                results_dir / f"grid_search_{half_protection_antibody_index}.csv"
            )
            load_path_best = results_dir / f"best_{half_protection_antibody_index}.csv"
            load_path_vaccination_time_range_best = (
                results_dir
                / f"vaccination_time_range_best_{half_protection_antibody_index}.csv"
            )
        # Plot reproduction number without vaccination
        df = pd.read_csv(load_path_within_host, index_col="time")
        ax_sus.plot(
            df.index,
            df["susceptibility_mean"],
            label="$\\it{A_{1/2}}$ = " + f"{half_protection_antibody}",
            color=color,
        )
        # Plot COR without vaccination and with default vaccination
        df = pd.read_csv(load_path_default, index_col="time")
        df["cor"].plot(
            ax=ax_cor_default,
            label="$\\it{A_{1/2}}$ = " + f"{half_protection_antibody}",
            color=color,
        )
        if half_protection_antibody_index == "baseline":
            df["cor_unvacc"].plot(
                ax=ax_cor_default, label="", color="k", linestyle="--", alpha=0.75
            )
        # Make plots for optimization of vaccination
        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_dir
            / f"heatmap_{half_protection_antibody_index}.svg",
            figure_path_best=figure_dir / f"best_{half_protection_antibody_index}.svg",
            show_plots=False,
            kwargs_best_unvacc={"color": "k", "linestyle": "--", "alpha": 0.75},
            kwargs_best_vacc={"color": color},
        )
    # Format and save susceptibility plot
    ax_sus.set_xlim(0, period)
    ax_sus.set_xticks(np.arange(0, period + 1, period / 6))
    ax_sus.set_ylim(0, 1)
    ax_sus.set_xlabel("Time since vaccination (days)")
    ax_sus.set_ylabel("Relative susceptibility")
    ax_sus.legend(loc="lower right")
    fig_sus.savefig(figure_dir / "susceptibility.pdf")
    fig_sus.savefig(figure_dir / "susceptibility.svg")
    # Format and save default COR plot
    plotting_utils.months_x_axis(ax_cor_default, period=period, no_periods=2)
    ax_cor_default.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(
        ax_cor_default, vaccination_time_range_default
    )
    ax_cor_default.set_ylabel("Case outbreak risk")
    ax_cor_default.legend(loc="lower right")
    fig_cor_default.savefig(figure_dir / "default.pdf")
    fig_cor_default.savefig(figure_dir / "default.svg")


if __name__ == "__main__":
    make_plots()
    if "snakemake" not in globals():
        plt.show()
