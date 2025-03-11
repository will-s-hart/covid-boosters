"""
Script for analysis of the optimal timing of annual COVID-19 vaccine distribution.

The script calculates the optimal vaccination timing to minimise the peak annual
outbreak risk via grid search. The grid search output, optimal vaccination timing and
outbreak risk values under the optimal vaccination timing are saved in the
`results/optimizing_vaccination` directory.

The `within_host_dynamics.py` script should be run first to run the within-host model
and generate the population susceptibility values when all individuals are vaccinated at
time 0 (which is used to calculate susceptibility values under different vaccination
scenarios in this script).

A refinement option in the grid search is available for efficiency (this isn't used
in this script as the entire grid is searched for illustrative purposes, but is used
by other scripts for sensitivity analyses which call the `run_analyses` function from
this script).
"""

import copy
import itertools
import pathlib
import sys

import joblib
import numpy as np
import pandas as pd
import tqdm

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import OutbreakRiskModel
from scripts import vaccination_example
from scripts.default_parameters import get_default_parameters


def run_analyses(
    save_path_grid_search=None,
    save_path_best=None,
    save_path_vaccination_time_range_best=None,
    load_path_susceptibility_all_0=None,
    obj_func=np.max,
    grid_step=10,
    refine=True,
    **kwargs_outbreak_risk_model,
):
    """
    Run the analyses.

    Parameters
    ----------
    save_path_grid_search : str, optional
        Path to save the objective function value at each grid point.
    save_path_best : str, optional
        Path to save the results with the optimal vaccination timing.
    save_path_vaccination_time_range_best : str, optional
        Path to save the optimal vaccination timing.
    load_path_susceptibility_all_0 : str, optional
        Path from which to load the population susceptibility values when all
        individuals are vaccinated at time 0, if they have been saved previously.
    obj_func : function, optional
        Objective function to minimize in the grid search. Default is `np.max` (i.e.,
        the peak annual outbreak risk is minimized).
    grid_step : int, optional
        Grid step size for the grid search. Default is 10.
    refine : bool, optional
        Whether to refine the search around the optimal grid point. Default is True.
    kwargs_outbreak_risk_model : dict
        Additional keyword arguments for the `covidboosters.OutbreakRiskModel` class.

    Returns
    -------
    None
    """
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
    # Set up outbreak risk model and load susceptibility values with vaccination of all
    # individuals at time 0
    outbreak_risk_model = OutbreakRiskModel(**kwargs_outbreak_risk_model)
    if (
        load_path_susceptibility_all_0 is not None
        and pathlib.Path(load_path_susceptibility_all_0).exists()
    ):
        outbreak_risk_model.load_susceptibility_all_0(load_path_susceptibility_all_0)
    else:
        print(
            "Saved susceptibility values with vaccination of all individuals at time 0 "
            "not found (or 'load_path_susceptibility_all_0' not provided). Calculating "
            "from scratch."
        )
        _ = outbreak_risk_model.susceptibility(np.arange(period))
    # Determine optimal vaccination timing
    vaccination_time_range_best = _run_optimization(
        outbreak_risk_model,
        obj_func=obj_func,
        grid_step=grid_step,
        refine=refine,
        save_path_grid_search=save_path_grid_search,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
    )
    # Results with optimal vaccination timing
    if save_path_best is not None:
        vaccination_example.run_analyses(
            save_path=save_path_best,
            load_path_susceptibility_all_0=load_path_susceptibility_all_0,
            **{
                **kwargs_outbreak_risk_model,
                "vaccination_time_range": vaccination_time_range_best,
            },
        )


def _run_optimization(
    outbreak_risk_model,
    obj_func=np.max,
    start_time_grid_vals=None,
    duration_grid_vals=None,
    grid_step=1,
    refine=False,
    save_path_grid_search=None,
    save_path_vaccination_time_range_best=None,
):
    # Helper function to run the actual optimization (grid search followed by optional
    # refinement step)
    period = outbreak_risk_model._period
    # Grid of vaccination start times and durations
    if start_time_grid_vals is None:
        start_time_grid_vals = np.arange(0, period + 1, grid_step)
    if duration_grid_vals is None:
        duration_grid_vals = np.arange(grid_step, period + 1, grid_step)
    start_time_best, duration_best = _run_grid_search(
        outbreak_risk_model,
        save_path_grid_search=save_path_grid_search,
        obj_func=obj_func,
        start_time_grid_vals=start_time_grid_vals,
        duration_grid_vals=duration_grid_vals,
    )
    # Refine the search
    if refine and grid_step > 1:
        print("Refining the search")
        start_time_grid_vals_refine = np.arange(
            start_time_best - grid_step, start_time_best + grid_step + 1
        )
        start_time_grid_vals_refine = start_time_grid_vals_refine[
            (start_time_grid_vals_refine >= 0) & (start_time_grid_vals_refine <= period)
        ]
        duration_grid_vals_refine = np.arange(
            duration_best - grid_step, duration_best + grid_step + 1
        )
        duration_grid_vals_refine = duration_grid_vals_refine[
            (duration_grid_vals_refine >= 1) & (duration_grid_vals_refine <= period)
        ]
        start_time_best, duration_best = _run_grid_search(
            outbreak_risk_model,
            obj_func=obj_func,
            start_time_grid_vals=start_time_grid_vals_refine,
            duration_grid_vals=duration_grid_vals_refine,
        )
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


def _run_grid_search(
    outbreak_risk_model,
    save_path_grid_search=None,
    obj_func=None,
    start_time_grid_vals=None,
    duration_grid_vals=None,
):
    # Helper function to run the grid search
    period = outbreak_risk_model._period

    def worker(vaccination_start_time, vaccination_duration):
        vaccination_time_range = [
            vaccination_start_time,
            vaccination_start_time + vaccination_duration,
        ]
        outbreak_risk_model_curr = copy.deepcopy(outbreak_risk_model)
        outbreak_risk_model_curr.update_vaccination_params(
            vaccination_time_range=vaccination_time_range
        )
        cor_vec = outbreak_risk_model_curr.case_outbreak_risk(np.arange(period))
        obj_val = obj_func(cor_vec)
        return obj_val

    # Loop over vaccination start times and durations
    n_jobs = joblib.cpu_count(only_physical_cores=True)
    print(f"Scanning over start times and durations using {n_jobs} cores")
    results = list(
        tqdm.tqdm(
            joblib.Parallel(return_as="generator", n_jobs=n_jobs)(
                joblib.delayed(worker)(start, duration)
                for start, duration in itertools.product(
                    start_time_grid_vals, duration_grid_vals
                )
            ),
            total=len(start_time_grid_vals) * len(duration_grid_vals),
        )
    )
    df_grid_search = (
        pd.DataFrame(
            np.reshape(
                results,
                (len(start_time_grid_vals), len(duration_grid_vals)),
            ),
            index=start_time_grid_vals,
            columns=duration_grid_vals,
            dtype=float,
        )
        .rename_axis("start", axis=0)
        .rename_axis("duration", axis=1)
    )
    # Save the results
    if save_path_grid_search is not None:
        df_grid_search.to_csv(save_path_grid_search)
    # Calculate optimal vaccination time range and corresponding case outbreak risk
    start_time_best, duration_best = df_grid_search.stack().idxmin()
    return start_time_best, duration_best


if __name__ == "__main__":
    results_dir = pathlib.Path(__file__).parents[1] / "results/optimizing_vaccination"
    results_dir.mkdir(exist_ok=True, parents=True)
    run_analyses(
        save_path_grid_search=results_dir / "grid_search.csv",
        save_path_best=results_dir / "best.csv",
        save_path_vaccination_time_range_best=results_dir
        / "vaccination_time_range_best.csv",
        load_path_susceptibility_all_0=pathlib.Path(__file__).parents[1]
        / "results/susceptibility_all_0.csv",
        grid_step=1,
    )
