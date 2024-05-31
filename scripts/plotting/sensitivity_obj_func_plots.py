import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots

obj_func_name_dict = {
    "baseline": "Maximum case outbreak risk",
    "mean": "Mean case outbreak risk",
    "weighted_mean": "Weighted mean case outbreak risk",
    "dec_jan_mean": "Dec-Jan mean case outbreak risk",
    "max_mean_comb1": "Max + (1/3) * mean case outbreak risk",
    "max_mean_comb2": "Max + mean case outbreak risk",
    "max_mean_comb3": "Max + 3 * mean case outbreak risk",
    "max_dec_jan_mean_comb": "Max + Dec-Jan mean case outbreak risk",
}


def make_plots():
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_obj_func"
    figure_dir.mkdir(exist_ok=True, parents=True)
    for obj_func_key, obj_func_name in obj_func_name_dict.items():
        if obj_func_key == "baseline":
            results_dir = (
                pathlib.Path(__file__).parents[2] / "results/optimizing_vaccination"
            )
            load_path_grid_search = results_dir / "grid_search.csv"
            load_path_best = results_dir / "best.csv"
            load_path_vaccination_time_range_best = (
                results_dir / "vaccination_time_range_best.csv"
            )
        else:
            results_dir = (
                pathlib.Path(__file__).parents[2] / "results/sensitivity_obj_func"
            )
            load_path_grid_search = results_dir / f"grid_search_{obj_func_key}.csv"
            load_path_best = results_dir / f"best_{obj_func_key}.csv"
            load_path_vaccination_time_range_best = (
                results_dir / f"vaccination_time_range_best_{obj_func_key}.csv"
            )
        # Make plots for optimization of vaccination
        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_dir / f"heatmap_{obj_func_key}.svg",
            figure_path_best=figure_dir / f"best_{obj_func_key}.svg",
            show_plots=False,
            kwargs_heatmap={"cbar_kws": {"label": obj_func_name}},
        )


if __name__ == "__main__":
    make_plots()
    if "snakemake" not in globals():
        plt.show()
