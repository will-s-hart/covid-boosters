import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots


def make_plots(prop_vacc_index):
    results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_prop_vacc"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_prop_vacc"
    figure_dir.mkdir(exist_ok=True, parents=True)

    load_path = results_dir / f"grid_search_{prop_vacc_index}.csv"
    load_path_best = results_dir / f"best_{prop_vacc_index}.csv"
    load_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{prop_vacc_index}.csv"
    )
    figure_path_heatmap = figure_dir / f"heatmap_{prop_vacc_index}.svg"
    figure_path_best = figure_dir / f"best_{prop_vacc_index}.svg"

    optimizing_vaccination_plots.make_plots(
        load_path=load_path,
        load_path_best=load_path_best,
        load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
        figure_path_heatmap=figure_path_heatmap,
        figure_path_best=figure_path_best,
        show_plots=False,
    )


if __name__ == "__main__":
    for _prop_vacc_index in range(3):
        make_plots(prop_vacc_index=_prop_vacc_index)
    if "snakemake" not in globals():
        plt.show()
