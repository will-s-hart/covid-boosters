import pathlib
import sys

import numpy as np

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination, vaccination_example

k_vals = [0.23, 0.60]  # based on CI in https://doi.org/10.1186/s12889-023-15915-1


def run_analyses(k_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_k"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_default = results_dir / f"default_{k_index}.csv"
    save_path_grid_search = results_dir / f"grid_search_{k_index}.csv"
    save_path_best = results_dir / f"best_{k_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{k_index}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    vaccination_example.run_analyses(
        save_path=save_path_default,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        dispersion_param=k_vals[k_index],
    )
    optimizing_vaccination.run_analyses(
        save_path_grid_search=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        dispersion_param=k_vals[k_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            k_index=int(snakemake.wildcards["index"]),  # noqa: F821
        )
    else:
        for _k_index in range(len(k_vals)):
            run_analyses(k_index=_k_index)
