import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts import sensitivity_r0_var
from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    color_palette = sns.color_palette("colorblind")
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_var"
    figure_dir.mkdir(exist_ok=True, parents=True)
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    r0_mean = default_parameters["unvaccinated_reproduction_no_mean"]
    peak_transmission_time = default_parameters["peak_transmission_time"]
    vaccination_time_range_default = default_parameters["vaccination_time_range"]
    fig_r0, ax_r0 = plotting_utils.setup_figure()
    fig_cor_default, ax_cor_default = plotting_utils.setup_figure()
    for r0_var_index in [0, "baseline", 1]:
        if r0_var_index == "baseline":
            r0_var = default_parameters["unvaccinated_reproduction_no_prop_variation"]
            color = color_palette[0]
            results_dir = pathlib.Path(__file__).parents[2] / "results"
            load_path_default = results_dir / "vaccination_example.csv"
            load_path_grid_search = (
                results_dir / "optimizing_vaccination/grid_search.csv"
            )
            load_path_best = results_dir / "optimizing_vaccination/best.csv"
            load_path_vaccination_time_range_best = (
                results_dir / "optimizing_vaccination/vaccination_time_range_best.csv"
            )
        else:
            r0_var = sensitivity_r0_var.r0_var_vals[r0_var_index]
            color = color_palette[r0_var_index + 1]
            results_dir = (
                pathlib.Path(__file__).parents[2] / "results/sensitivity_r0_var"
            )
            load_path_default = results_dir / f"default_{r0_var_index}.csv"
            load_path_grid_search = results_dir / f"grid_search_{r0_var_index}.csv"
            load_path_best = results_dir / f"best_{r0_var_index}.csv"
            load_path_vaccination_time_range_best = (
                results_dir / f"vaccination_time_range_best_{r0_var_index}.csv"
            )
        # Plot reproduction number without vaccination
        time_vec = np.arange(2 * period)
        r0_vec = r0_mean * (
            1
            + r0_var * np.cos(2 * np.pi * (time_vec - peak_transmission_time) / period)
        )
        ax_r0.plot(
            time_vec,
            r0_vec,
            label="$\\varepsilon$ = " + f"{r0_var}",
            color=color,
        )
        # Plot COR without vaccination and with default vaccination
        df = pd.read_csv(load_path_default, index_col="time")
        df["cor_unvacc"].plot(
            ax=ax_cor_default, label="", color=color, linestyle="--", alpha=0.75
        )
        df["cor"].plot(
            ax=ax_cor_default,
            label="$\\varepsilon$ = " + f"{r0_var}",
            color=color,
        )
        # Make plots for optimization of vaccination
        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_dir / f"heatmap_{r0_var_index}.svg",
            figure_path_best=figure_dir / f"best_{r0_var_index}.svg",
            show_plots=False,
            kwargs_best_unvacc={"color": color, "linestyle": "--", "alpha": 0.75},
            kwargs_best_vacc={"color": color},
        )
    # Format and save reproduction number plot
    plotting_utils.months_x_axis(ax_r0, period=period, no_periods=2)
    ax_r0.set_ylim(0, 3.5)
    ax_r0.set_ylabel("Instantaneous reproduction number")
    ax_r0.legend(loc="lower right")
    fig_r0.savefig(figure_dir / "reproduction_number.pdf")
    fig_r0.savefig(figure_dir / "reproduction_number.svg")
    # Format and save default COR plot
    plotting_utils.months_x_axis(ax_cor_default, period=period, no_periods=2)
    ax_cor_default.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(
        ax_cor_default, vaccination_time_range_default
    )
    ax_cor_default.set_ylabel("Outbreak risk")
    ax_cor_default.legend(loc="lower right")
    fig_cor_default.savefig(figure_dir / "default.pdf")
    fig_cor_default.savefig(figure_dir / "default.svg")


if __name__ == "__main__":
    make_plots()
    if "snakemake" not in globals():
        plt.show()
