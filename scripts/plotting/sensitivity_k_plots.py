import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts import sensitivity_k
from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    color_palette = sns.color_palette()
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_k"
    figure_dir.mkdir(exist_ok=True, parents=True)
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    vaccination_time_range_default = default_parameters["vaccination_time_range"]
    fig_cor_default, ax_cor_default = plotting_utils.setup_figure()
    for k_index in [0, "baseline", 1]:
        if k_index == "baseline":
            dispersion_param = default_parameters["dispersion_param"]
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
            dispersion_param = sensitivity_k.k_vals[k_index]
            color = color_palette[k_index + 1]
            results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_k"
            load_path_default = results_dir / f"default_{k_index}.csv"
            load_path_grid_search = results_dir / f"grid_search_{k_index}.csv"
            load_path_best = results_dir / f"best_{k_index}.csv"
            load_path_vaccination_time_range_best = (
                results_dir / f"vaccination_time_range_best_{k_index}.csv"
            )
        # Plot COR without vaccination and with default vaccination
        df = pd.read_csv(load_path_default, index_col="time")
        df["cor_unvacc"].plot(
            ax=ax_cor_default, label="", color=color, linestyle="--", alpha=0.75
        )
        df["cor"].plot(
            ax=ax_cor_default, label="$\\it{k}$ = " + f"{dispersion_param}", color=color
        )
        # Make plots for optimization of vaccination
        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_dir / f"heatmap_{k_index}.svg",
            figure_path_best=figure_dir / f"best_{k_index}.svg",
            show_plots=False,
            ylim_best=(0, 0.6),
            kwargs_best_unvacc={"color": color, "linestyle": "--", "alpha": 0.75},
            kwargs_best_vacc={"color": color},
        )
    plotting_utils.months_x_axis(ax_cor_default, period=period, no_periods=2)
    ax_cor_default.set_ylim(0, 0.6)
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
