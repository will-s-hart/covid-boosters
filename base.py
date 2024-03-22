"""
Base module defining main classes and methods.
"""

import numpy as np
from scipy.stats import gamma, poisson


class HeterogeneousRenewalModel:
    """
    Base class for renewal models in hetergeneous populations.
    """

    def __init__(
        self, reproduction_no_func, generation_time_dist, dispersion_param=1.0
    ):
        self._reproduction_no_func = reproduction_no_func
        self._generation_time_dist = generation_time_dist
        self._generation_time_max = generation_time_dist.support()[1]
        self._dispersion_param = dispersion_param

    def simulate(
        self,
        time_start=0,
        incidence_start=1,
        incidence_cutoff=1000,
        rng=None,
        rng_seed=None,
    ):
        if rng is None:
            rng = np.random.default_rng(rng_seed)
        reproduction_no_func = self._reproduction_no_func
        generation_time_dist = self._generation_time_dist
        generation_time_max = self._generation_time_max
        generation_time_pmf_vec = generation_time_dist.pmf(
            np.arange(1, generation_time_max + 1)
        )
        dispersion_param = self._dispersion_param
        time = time_start
        incidence = incidence_start
        infectiousness_scaling = gamma.rvs(
            a=incidence_start * dispersion_param,
            scale=1 / dispersion_param,
            random_state=rng,
        )
        infectiousness_scaled_incidence = infectiousness_scaling * incidence
        time_vec = np.array([time])
        incidence_vec = np.array([incidence])
        infectiousness_scaled_incidence_vec = np.array(
            [infectiousness_scaled_incidence]
        )
        while 1:
            time += 1
            reproduction_no = reproduction_no_func(time)
            expected_incidence = reproduction_no * generation_time_pmf_vec[
                : min(time - time_start, generation_time_max)
            ].dot(
                infectiousness_scaled_incidence_vec[
                    -1 : -min(time - time_start, generation_time_max) - 1 : -1
                ]
            )
            incidence = poisson.rvs(mu=expected_incidence, random_state=rng)
            if incidence > 0:
                infectiousness_scaling = gamma.rvs(
                    a=incidence * dispersion_param,
                    scale=1 / dispersion_param,
                    random_state=rng,
                )
            else:
                infectiousness_scaling = 0
            time_vec = np.append(time_vec, time)
            incidence_vec = np.append(incidence_vec, incidence)
            infectiousness_scaled_incidence_vec = np.append(
                infectiousness_scaled_incidence_vec, infectiousness_scaling * incidence
            )
            if incidence >= incidence_cutoff:
                outbreak_cutoff_bool = True
                break
            if time - time_start > generation_time_max and np.all(
                incidence_vec[-1 : -generation_time_max - 1 : -1] == 0
            ):
                outbreak_cutoff_bool = False
                break
        output = {
            "time_vec": time_vec,
            "incidence_vec": incidence_vec,
            "outbreak_cutoff_bool": outbreak_cutoff_bool,
        }
        return output


class PeriodicHeterogeneousRenewalModel(HeterogeneousRenewalModel):
    """
    Class for renewal models in hetergeneous populations with periodic transmission.
    """

    def __init__(
        self,
        reproduction_no_func,
        generation_time_dist,
        dispersion_param=1.0,
        period=365,
    ):
        super().__init__(reproduction_no_func, generation_time_dist, dispersion_param)
        self._period = period
