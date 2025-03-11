"""
Script for running the within-host model in the main COVID-19 case study.

Antibody titers and susceptibility values are calculated relative to the most recent
vaccine dose for a cohort of individuals. Summary statistics are calculated and saved in
the `results` directory. The population susceptibility values when all individuals are
vaccinated at time 0 are also saved for re-use in other scripts.
"""

import pathlib
import sys

import numpy as np
import pandas as pd
import tqdm

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import PeriodicIndividualSusceptibilityModel
from scripts.default_parameters import get_default_parameters


def run_analyses(
    save_path,
    save_path_susceptibility_all_0=None,
    **kwargs_individual_susceptibility_model_in,
):
    """
    Run the analyses.

    Parameters
    ----------
    save_path : str
        Path to save the results.
    save_path_susceptibility_all_0 : str, optional
        Path to save the population susceptibility values when all individuals are
        vaccinated at time 0 (to re-use in other scripts).
    kwargs_individual_susceptibility_model_in : dict
        Additional keyword arguments for the
        `covidboosters.PeriodicIndividualSusceptibilityModel` class.

    Returns
    -------
    None
    """
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    population_size = default_parameters["population_size"]
    antibody_model_params_pop = default_parameters["antibody_model_params_pop"]
    antibody_model_params_random_effects = default_parameters[
        "antibody_model_params_random_effects"
    ]
    susceptibility_func_params = default_parameters["susceptibility_func_params"]
    rng = np.random.default_rng(seed=2)
    time_vec = np.arange(period)
    log10_antibodies_mat = np.zeros((period, population_size))
    susceptibility_mat = np.zeros((period, population_size))
    print(f"Running the within-host model for {population_size} individuals")
    for individual_no in tqdm.tqdm(range(population_size)):
        antibody_model_params = {}
        for param_name, param_pop in antibody_model_params_pop.items():
            param_random_effect = antibody_model_params_random_effects[param_name]
            antibody_model_params[param_name] = param_pop * np.exp(
                param_random_effect * rng.standard_normal()
            )
        kwargs_individual_susceptibility_model = {
            "period": period,
            "susceptibility_func_params": susceptibility_func_params,
            "vaccination_times": 0,
            **kwargs_individual_susceptibility_model_in,
            "antibody_model_params": antibody_model_params,
        }
        individual_susceptibility_model = PeriodicIndividualSusceptibilityModel(
            **kwargs_individual_susceptibility_model
        )
        log10_antibodies_mat[:, individual_no] = np.log10(
            individual_susceptibility_model.antibodies(time_vec)
        )
        susceptibility_mat[:, individual_no] = (
            individual_susceptibility_model.susceptibility(time_vec)
        )
    df = pd.DataFrame({"time": time_vec})
    df.set_index("time", inplace=True)
    df["log10_antibodies_mean"] = np.mean(log10_antibodies_mat, axis=1)
    df["log10_antibodies_median"] = np.median(log10_antibodies_mat, axis=1)
    df["log10_antibodies_95ci_lower"] = np.percentile(log10_antibodies_mat, 2.5, axis=1)
    df["log10_antibodies_95ci_upper"] = np.percentile(
        log10_antibodies_mat, 97.5, axis=1
    )
    df["susceptibility_mean"] = np.mean(susceptibility_mat, axis=1)
    df["susceptibility_median"] = np.median(susceptibility_mat, axis=1)
    df["susceptibility_95ci_lower"] = np.percentile(susceptibility_mat, 2.5, axis=1)
    df["susceptibility_95ci_upper"] = np.percentile(susceptibility_mat, 97.5, axis=1)
    # Save the results
    df.to_csv(save_path)
    if save_path_susceptibility_all_0 is not None:
        df_susceptibility_all_0 = df["susceptibility_mean"].rename("susceptibility")
        df_susceptibility_all_0.to_csv(save_path_susceptibility_all_0)


if __name__ == "__main__":
    results_dir = pathlib.Path(__file__).parents[1] / "results"
    results_dir.mkdir(exist_ok=True, parents=True)
    run_analyses(
        save_path=results_dir / "within_host_dynamics.csv",
        save_path_susceptibility_all_0=results_dir / "susceptibility_all_0.csv",
    )
