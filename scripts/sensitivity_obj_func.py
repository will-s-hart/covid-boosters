import pathlib
import sys

import numpy as np

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination
from scripts.default_parameters import get_default_parameters

if get_default_parameters()["period"] != 360:
    raise ValueError("This script is only valid for 360-day calendar.")


def dec_jan_mean(x):
    return np.mean(np.concatenate([x[0:30], x[330:360]]))


def max_mean_comb1(x):
    return np.max(x) + np.mean(x) / 3


def max_mean_comb2(x):
    return np.max(x) + np.mean(x)


def max_mean_comb3(x):
    return np.max(x) + 3 * np.mean(x)


def max_dec_jan_mean_comb(x):
    return np.max(x) + dec_jan_mean(x)


def weighted_mean(x):
    weights = 2.5 * (1 + 0.2 * np.cos(2 * np.pi * np.arange(360) / 360))
    weights -= np.min(weights)
    weights /= np.sum(weights)
    return np.sum(x * weights)


obj_func_dict = {
    "mean": np.mean,
    "dec_jan_mean": dec_jan_mean,
    "weighted_mean": weighted_mean,
    "max_mean_comb1": max_mean_comb1,
    "max_mean_comb2": max_mean_comb2,
    "max_mean_comb3": max_mean_comb3,
    "max_dec_jan_mean_comb": max_dec_jan_mean_comb,
}


def run_analyses(obj_func_key):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_obj_func"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_grid_search = results_dir / f"grid_search_{obj_func_key}.csv"
    save_path_best = results_dir / f"best_{obj_func_key}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{obj_func_key}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    obj_func = obj_func_dict[obj_func_key]
    optimizing_vaccination.run_analyses(
        save_path_grid_search=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        obj_func=obj_func,
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        _obj_func_key = obj_func_dict[snakemake.wildcards["obj_func_key"]]  # noqa: F821
        run_analyses(obj_func_key=_obj_func_key)
    else:
        for _obj_func_key in obj_func_dict.keys():
            run_analyses(obj_func_key=_obj_func_key)
