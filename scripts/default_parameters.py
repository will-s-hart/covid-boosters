import functools
import pathlib

import numpy as np
import pandas as pd
from scipy import integrate
from scipy.stats import lognorm, rv_discrete

results_dir = pathlib.Path(__file__).parents[1] / "results"


def get_default_parameters():
    period = 360
    unvacc_rep_no_mean = 2.5  # with below, max is 3
    unvacc_rep_no_prop_var = 0.2
    peak_transmission_time = 0

    generation_time_logmean = 0.979396480343543
    generation_time_logsd = 0.470500197316974
    generation_time_dist_cont = lognorm(
        s=generation_time_logsd, scale=np.exp(generation_time_logmean)
    )
    generation_time_dist = _discretise_gt(generation_time_dist_cont, t_max=14)

    dispersion_param = 0.41

    df_antibody_model_params = pd.read_csv(
        results_dir / "antibody_model_params.csv", index_col=0
    )
    antibody_model_params_pop = df_antibody_model_params["population_value"].to_dict()
    antibody_model_params_random_effects = df_antibody_model_params[
        "random_effect"
    ].to_dict()

    # antibody_covalescent = 114.92
    # half_protection_neutralizing_ab = 0.2
    # omicron_reduction_factor = 22
    # # vaccine_adaptation_factor = 1.61
    # vaccine_adaptation_factor = 1

    # susceptibility_func_params = {
    #     "antibody_response_steepness": np.exp(1.13) / np.log(10),
    #     "half_protection_antibody": half_protection_neutralizing_ab
    #     * antibody_covalescent
    #     * (omicron_reduction_factor / vaccine_adaptation_factor),
    # }
    susceptibility_func_params = {
        "antibody_response_steepness": 3.2 / np.log(10),
        "half_protection_antibody": 1000,
    }

    vaccination_time_range = [270, 345]
    proportion_vaccinated = 0.35
    population_size = 1000

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


def _discretise_gt(gt_dist_cont, t_max):
    def _integrand_fun(t, y):
        # To get probability mass function at time x, need to integrate this expression
        # with respect to y between y=x-1 and and y=x+1
        return (1 - abs(t - y)) * gt_dist_cont.pdf(y)

    # Set up vector of t values and pre-allocate vector of probabilities
    t_vec = np.arange(t_max + 1)
    p_vec = np.zeros(len(t_vec))
    # Calculate probability mass function at each x value
    for i, t in enumerate(t_vec):
        integrand = functools.partial(_integrand_fun, t)
        p_vec[i] = integrate.quad(integrand, t - 1, t + 1)[0]
    # Reassign probability mass from 0 to 1
    p_vec[1] = p_vec[0] + p_vec[1]
    p_vec = p_vec[1:]
    t_vec = t_vec[1:]
    # Normalise probabilities
    p_sum = np.sum(p_vec)
    if 1 - p_sum > 1e-3:
        raise ValueError("Sum of probabilities is not close to 1. Increase t_max.")
    p_vec = p_vec / p_sum
    gt_dist_discr = rv_discrete(values=(t_vec, p_vec))
    return gt_dist_discr


if __name__ == "__main__":
    get_default_parameters()
