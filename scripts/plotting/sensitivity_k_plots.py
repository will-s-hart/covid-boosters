import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots


def make_plots(k_index):
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_k"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_k"
    figure_dir.mkdir(exist_ok=True, parents=True)

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
    )


if __name__ == "__main__":
    if "snakemake" in globals() and "mean_index" in snakemake.wildcards:  # noqa: F821
        make_plots(
            k_index=int(snakemake.wildcards["k_index"]),  # noqa: F821
        )
    else:
        for _k_index in range(3):
            make_plots(_k_index)
        plt.show()
