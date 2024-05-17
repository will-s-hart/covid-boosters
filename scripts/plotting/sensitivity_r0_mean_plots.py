import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots


def make_plots(r0_mean_index):
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_r0_mean"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_mean"
    figure_dir.mkdir(exist_ok=True, parents=True)

    load_path = results_dir / f"grid_search_{r0_mean_index}.csv"
    load_path_best = results_dir / f"best_{r0_mean_index}.csv"
    load_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{r0_mean_index}.csv"
    )
    figure_path_heatmap = figure_dir / f"heatmap_{r0_mean_index}.svg"
    figure_path_best = figure_dir / f"best_{r0_mean_index}.svg"

    optimizing_vaccination_plots.make_plots(
        load_path=load_path,
        load_path_best=load_path_best,
        load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
        figure_path_heatmap=figure_path_heatmap,
        figure_path_best=figure_path_best,
        show_plots=False,
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        make_plots(
            int(snakemake.wildcards["r0_mean_index"]),  # noqa: F821
        )
    else:
        for _r0_mean_index in range(2):
            make_plots(_r0_mean_index)
        plt.show()
