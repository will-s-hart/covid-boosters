import itertools
import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots


def make_plots(mean_index, prop_var_index):
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_unvacc_r"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_unvacc_r"
    figure_dir.mkdir(exist_ok=True, parents=True)

    load_path = results_dir / f"grid_search_{mean_index}_{prop_var_index}.csv"
    load_path_best = results_dir / f"best_{mean_index}_{prop_var_index}.csv"
    load_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{mean_index}_{prop_var_index}.csv"
    )
    figure_path_heatmap = figure_dir / f"heatmap_{mean_index}_{prop_var_index}.svg"
    figure_path_best = figure_dir / f"best_{mean_index}_{prop_var_index}.svg"

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
            mean_index=int(snakemake.wildcards["mean_index"]),  # noqa: F821
            prop_var_index=int(snakemake.wildcards["prop_var_index"]),  # noqa: F821
        )
    else:
        for _mean_index, _prop_var_index in itertools.product(range(3), range(3)):
            make_plots(_mean_index, _prop_var_index)
        plt.show()
