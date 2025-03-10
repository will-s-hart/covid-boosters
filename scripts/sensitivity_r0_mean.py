"""
Script for exploring sensitivity to the mean reproduction number before vaccination.

The script calculates the optimal vaccination timing to minimise the peak annual
outbreak risk for different values of the annual mean reproduction number in the
absence of vaccination. The grid search output, optimal vaccination timing and
outbreak risk values under the optimal vaccination timing are saved in the
`results/sensitivity_r0_mean` directory.

The `vaccination_example.py` script should be run first to run the within-host model
and generate the population susceptibility values when all individuals are vaccinated at
time 0 (which is used to calculate susceptibility values under different vaccination
scenarios in this script).
"""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination, vaccination_example

r0_mean_vals = [2, 3]


def run_analyses(r0_mean_index):
    """
    Run the analyses.

    Parameters
    ----------
    r0_mean_index : int
        Index of the annual mean reproduction number without vaccination in the
        `r0_mean_vals` list (as defined within this script).
    """
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_r0_mean"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_default = results_dir / f"default_{r0_mean_index}.csv"
    save_path_grid_search = results_dir / f"grid_search_{r0_mean_index}.csv"
    save_path_best = results_dir / f"best_{r0_mean_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{r0_mean_index}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    vaccination_example.run_analyses(
        save_path=save_path_default,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_mean=r0_mean_vals[r0_mean_index],
    )
    optimizing_vaccination.run_analyses(
        save_path_grid_search=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_mean=r0_mean_vals[r0_mean_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            r0_mean_index=int(snakemake.wildcards["index"]),  # noqa: F821
        )
    else:
        for _r0_mean_index in range(len(r0_mean_vals)):
            run_analyses(r0_mean_index=_r0_mean_index)
