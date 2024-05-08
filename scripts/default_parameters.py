from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gamma, rv_discrete

results_dir = Path(__file__).parents[1] / "results"


def get_default_parameters():
    period = 360
    unvacc_rep_no_mean = 2
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
    # antibody_model_params_random_effects = {key: 0 for key in antibody_model_params_pop}

    antibody_covalescent = 114.92
    half_protection_neutralizing_ab = 0.2
    omicron_reduction_factor = 22
    vaccine_adaptation_factor = 1.61

    susceptibility_func_params = {
        "antibody_response_steepness": np.exp(1.13) / np.log(10),
        "half_protection_antibody": half_protection_neutralizing_ab
        * antibody_covalescent
        * (omicron_reduction_factor / vaccine_adaptation_factor),
    }

    vaccination_time_range = [270, 360]
    proportion_vaccinated = 0.5
    population_size = 1000
    # population_size = 1

    sim_incidence_cutoff = 10
    no_simulations = 5000

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
        "sim_incidence_cutoff": sim_incidence_cutoff,
        "no_simulations": no_simulations,
    }

    return default_parameters
