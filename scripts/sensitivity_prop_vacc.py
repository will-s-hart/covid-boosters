"""
Script for exploring sensitivity to the proportion of the population vaccinated.

The script calculates the optimal vaccination timing to minimise the peak annual
outbreak risk for different values of the proportion of the population vaccinated each
year. The grid search output, optimal vaccination timing and outbreak risk values under
the optimal vaccination timing are saved in the `results/sensitivity_prop_vacc`
directory.

The `vaccination_example.py` script should be run first to run the within-host model
and generate the population susceptibility values when all individuals are vaccinated at
time 0 (which is used to calculate susceptibility values under different vaccination
scenarios in this script).
"""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination, vaccination_example

prop_vacc_vals = [0.4, 0.8]


def run_analyses(prop_vacc_index):
    """
    Run the analyses.

    Parameters
    ----------
    prop_vacc_index : int
        Index of the proportion of the population vaccinated each year in the
        `prop_vacc_vals` list (as defined within this script).
    """
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_prop_vacc"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_default = results_dir / f"default_{prop_vacc_index}.csv"
    save_path_grid_search = results_dir / f"grid_search_{prop_vacc_index}.csv"
    save_path_best = results_dir / f"best_{prop_vacc_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{prop_vacc_index}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    vaccination_example.run_analyses(
        save_path=save_path_default,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        proportion_vaccinated=prop_vacc_vals[prop_vacc_index],
    )
    optimizing_vaccination.run_analyses(
        save_path_grid_search=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        proportion_vaccinated=prop_vacc_vals[prop_vacc_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            prop_vacc_index=int(snakemake.wildcards["index"]),  # noqa: F821
        )
    else:
        for _prop_vacc_index in range(len(prop_vacc_vals)):
            run_analyses(prop_vacc_index=_prop_vacc_index)
