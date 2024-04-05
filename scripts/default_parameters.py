from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gamma, rv_discrete

results_dir = Path(__file__).parents[1] / "results"


def _get_default_parameters():
    period = 360
    unvacc_rep_no_mean = 3
    unvacc_rep_no_prop_var = 0.25
    peak_transmission_time = 0

    generation_time_max = 30
    generation_time_vals = np.arange(1, generation_time_max + 1)
    generation_time_probs = gamma.pdf(generation_time_vals, a=3, scale=5 / 3)
    generation_time_probs /= generation_time_probs.sum()
    generation_time_dist = rv_discrete(
        values=(generation_time_vals, generation_time_probs)
    )

    dispersion_param = 0.41

    antibody_model_params_pop = pd.read_csv(
        results_dir / "antibody_model_params_pop.csv", index_col=0, header=None
    )[1].to_dict()
    antibody_model_params_random_effects = pd.read_csv(
        results_dir / "antibody_model_params_random_effects.csv",
        index_col=0,
        header=None,
    )[1].to_dict()

    susceptibility_func_params = {
        "antibody_response_steepness": 3 / np.log(10),
        "half_protection_antibody": 114.92 * np.exp(0.2 * np.log(10)),
    }

    vaccination_time_range = [270, 360]
    proportion_vaccinated = 0.8
    population_size = 1000

    default_parameters = {
        "period": period,
        "unvaccinated_reproduction_no_mean": unvacc_rep_no_mean,
        "unvaccinated_reproduction_no_prop_variation": unvacc_rep_no_prop_var,
        "peak_transmission_time": peak_transmission_time,
        "generation_time_dist": generation_time_dist,
        "dispersion_param": dispersion_param,
        "antibody_model_params_pop": antibody_model_params_pop,
        "antibody_model_params_random_effects": antibody_model_params_random_effects,
        "susceptibility_func_params": susceptibility_func_params,
        "vaccination_time_range": vaccination_time_range,
        "proportion_vaccinated": proportion_vaccinated,
        "population_size": population_size,
    }

    return default_parameters


DEFAULT_PARAMETERS = _get_default_parameters()
