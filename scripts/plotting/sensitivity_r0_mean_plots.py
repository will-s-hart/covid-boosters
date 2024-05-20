import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts import sensitivity_r0_mean
from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_r0_mean"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_mean"
    figure_dir.mkdir(exist_ok=True, parents=True)

    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(2 * period)
    r0_prop_variation = default_parameters[
        "unvaccinated_reproduction_no_prop_variation"
    ]
    peak_transmission_time = default_parameters["peak_transmission_time"]
    r0_mean_vals = np.concatenate(
        (
            sensitivity_r0_mean.r0_mean_vals,
            [default_parameters["unvaccinated_reproduction_no_mean"]],
        ),
    )
    fig, ax = plotting_utils.setup_figure()
    r0_plot_list = []
    for r0_mean_index, r0_mean in enumerate(r0_mean_vals):
        r0_vec = r0_mean * (
            1
            + r0_prop_variation
            * np.cos(2 * np.pi * (time_vec - peak_transmission_time) / period)
        )
        p = ax.plot(time_vec, r0_vec, label="$\\it{\\widebar{R}_0}$ = " + f"{r0_mean}")
        r0_plot_list.append(p[0])

        if r0_mean_index == 2:
            continue

        load_path_grid_search = results_dir / f"grid_search_{r0_mean_index}.csv"
        load_path_best = results_dir / f"best_{r0_mean_index}.csv"
        load_path_vaccination_time_range_best = (
            results_dir / f"vaccination_time_range_best_{r0_mean_index}.csv"
        )
        figure_path_heatmap = figure_dir / f"heatmap_{r0_mean_index}.svg"
        figure_path_best = figure_dir / f"best_{r0_mean_index}.svg"

        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_path_heatmap,
            figure_path_best=figure_path_best,
            show_plots=False,
        )
    r0_plot_list = [r0_plot_list[0], r0_plot_list[2], r0_plot_list[1]]
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylabel("Instantaneous reproduction number")
    ax.legend(r0_plot_list, [p.get_label() for p in r0_plot_list], loc="upper right")
    fig.savefig(figure_dir / "reproduction_number.pdf")
    fig.savefig(figure_dir / "reproduction_number.svg")


if __name__ == "__main__":
    make_plots()
    if "snakemake" not in globals():
        plt.show()
