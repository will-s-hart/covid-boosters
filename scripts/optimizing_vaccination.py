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
from scripts import vaccination_example
from scripts.default_parameters import get_default_parameters


def run_analyses():
    results_dir = pathlib.Path(__file__).parents[1] / "results/optimizing_vaccination"
    results_dir.mkdir(exist_ok=True, parents=True)
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    vaccination_time_range_best = run_grid_search(
        save_path=results_dir / "grid_search.csv",
        save_path_vaccination_time_range_best=results_dir
        / "vaccination_time_range_best.csv",
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
    )
    vaccination_example.run_analyses(
        save_path=results_dir / "best.csv",
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        vaccination_time_range=vaccination_time_range_best,
    )


def run_grid_search(
    save_path=None,
    save_path_vaccination_time_range_best=None,
    load_path_susceptibility_all_0=None,
    **kwargs_outbreak_risk_model,
):
    default_parameters = get_default_parameters()
    kwargs_outbreak_risk_model_in = kwargs_outbreak_risk_model
    kwargs_outbreak_risk_model = {
        key: default_parameters[key]
        for key in [
            "period",
            "unvaccinated_reproduction_no_mean",
            "unvaccinated_reproduction_no_prop_variation",
            "peak_transmission_time",
            "generation_time_dist",
            "dispersion_param",
            "vaccination_time_range",
            "proportion_vaccinated",
            "antibody_model_params_pop",
            "susceptibility_func_params",
            "antibody_model_params_random_effects",
            "population_size",
        ]
    }
    kwargs_outbreak_risk_model["rng_seed"] = 2
    kwargs_outbreak_risk_model.update(kwargs_outbreak_risk_model_in)
    period = kwargs_outbreak_risk_model["period"]
    # Grid of vaccination start times and durations
    step = 5
    vaccination_start_time_vals = np.arange(0, period + 1, step)
    vaccination_duration_vals = np.arange(step, period + 1, step)
    # Set up outbreak risk model
    outbreak_risk_model = OutbreakRiskModel(**kwargs_outbreak_risk_model)
    if load_path_susceptibility_all_0 is not None:
        outbreak_risk_model.load_susceptibility_all_0(load_path_susceptibility_all_0)

    # Loop over vaccination start times and durations
    def worker(vaccination_start_time, vaccination_duration):
        vaccination_time_range = [
            vaccination_start_time,
            vaccination_start_time + vaccination_duration,
        ]
        outbreak_risk_model_curr = copy.copy(outbreak_risk_model)
        outbreak_risk_model_curr.update_vaccination_params(
            vaccination_time_range=vaccination_time_range
        )
        cor_max = np.max(outbreak_risk_model.case_outbreak_risk(np.arange(period)))
        return cor_max

    n_jobs = joblib.cpu_count(only_physical_cores=True)
    print(f"Scanning over start times and durations using {n_jobs} cores")
    results = list(
        tqdm.tqdm(
            joblib.Parallel(return_as="generator", n_jobs=n_jobs)(
                joblib.delayed(worker)(start, duration)
                for start, duration in itertools.product(
                    vaccination_start_time_vals, vaccination_duration_vals
                )
            ),
            total=len(vaccination_start_time_vals) * len(vaccination_duration_vals),
        )
    )
    df_grid_search = (
        pd.DataFrame(
            np.reshape(
                results,
                (len(vaccination_start_time_vals), len(vaccination_duration_vals)),
            ),
            index=vaccination_start_time_vals,
            columns=vaccination_duration_vals,
            dtype=float,
        )
        .rename_axis("start", axis=0)
        .rename_axis("duration", axis=1)
    )
    # Save the results
    if save_path is not None:
        df_grid_search.to_csv(save_path)
    # Return optimal vaccination time range
    start_time_best, duration_best = df_grid_search.stack().idxmin()
    vaccination_time_range_best = [
        start_time_best,
        start_time_best + duration_best,
    ]
    if save_path_vaccination_time_range_best is not None:
        pd.DataFrame(
            {
                "start": [vaccination_time_range_best[0]],
                "end": [vaccination_time_range_best[1]],
            }
        ).to_csv(save_path_vaccination_time_range_best)
    return vaccination_time_range_best


if __name__ == "__main__":
    run_analyses()