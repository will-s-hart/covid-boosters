import copy
import itertools
import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

import joblib
import numpy as np
import pandas as pd
import tqdm

from covidboosters import OutbreakRiskModel
from scripts import optimizing_vaccination, vaccination_example
from scripts.default_parameters import get_default_parameters


def run_analyses():
    unvacc_rep_no_mean_vals = [1, 2, 3]
    unvacc_rep_no_prop_var_vals = [0.1, 0.25, 0.4]
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_unvacc_r"
    results_dir.mkdir(exist_ok=True, parents=True)
    for unvacc_rep_no_mean, unvacc_rep_no_prop_var in itertools.product(
        unvacc_rep_no_mean_vals, unvacc_rep_no_prop_var_vals
    ):
        file_ext = f"_{unvacc_rep_no_mean}_{100*unvacc_rep_no_prop_var}"
        optimizing_vaccination.run_analyses(
            save_path=results_dir / f"grid_search{file_ext}.csv",
            save_path_best=results_dir / f"best{file_ext}.csv",
            save_path_vaccination_time_range_best=results_dir
            / f"vaccination_time_range_best{file_ext}.csv",
            load_path_susceptibility_all_0=pathlib.Path(__file__).parents[1]
            / "results/susceptibility_all_0.csv",
            unvaccinated_reproduction_no_mean=unvacc_rep_no_mean,
            unvaccinated_reproduction_no_prop_variation=unvacc_rep_no_prop_var,
        )


if __name__ == "__main__":
    run_analyses()
