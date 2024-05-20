import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots


def make_plots(k_index):
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_k"
    figure_dir.mkdir(exist_ok=True, parents=True)
    if k_index == "default":
        results_dir = (
            pathlib.Path(__file__).parents[2] / "results/optimizing_vaccination"
        )
        load_path = results_dir / "grid_search.csv"
        load_path_best = results_dir / "best.csv"
        load_path_vaccination_time_range_best = (
            results_dir / "vaccination_time_range_best.csv"
        )
    else:
        results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_k"
        load_path = results_dir / f"grid_search_{k_index}.csv"
        load_path_best = results_dir / f"best_{k_index}.csv"
        load_path_vaccination_time_range_best = (
            results_dir / f"vaccination_time_range_best_{k_index}.csv"
        )
    figure_path_heatmap = figure_dir / f"heatmap_{k_index}.svg"
    figure_path_best = figure_dir / f"best_{k_index}.svg"

    optimizing_vaccination_plots.make_plots(
        load_path=load_path,
        load_path_best=load_path_best,
        load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
        figure_path_heatmap=figure_path_heatmap,
        figure_path_best=figure_path_best,
        show_plots=False,
        ylim_best=(0, 0.6),
    )


if __name__ == "__main__":
    for _k_index in ["default", 0, 1]:
        make_plots(k_index=_k_index)
    if "snakemake" not in globals():
        plt.show()
