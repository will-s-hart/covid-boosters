"""
Base module defining main classes and methods.
"""

import numpy as np
from scipy.optimize import newton
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
            a=incidence * dispersion_param,
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
                outbreak_cutoff_indicator = True
                break
            if time - time_start > generation_time_max and np.all(
                incidence_vec[-1 : -generation_time_max - 1 : -1] == 0
            ):
                outbreak_cutoff_indicator = False
                break
        output = {
            "time_vec": time_vec,
            "incidence_vec": incidence_vec,
            "outbreak_cutoff_indicator": outbreak_cutoff_indicator,
        }
        return output

    def simulated_outbreak_risk(
        self,
        time_vec,
        incidence_cutoff=1000,
        no_simulations=1000,
        rng=None,
        rng_seed=None,
    ):
        if rng is None:
            rng = np.random.default_rng(rng_seed)
        outbreak_risk_vec = np.zeros(len(time_vec))
        for i, time in enumerate(time_vec):
            major_outbreak_indicator_vec = np.zeros(no_simulations, dtype=bool)
            for j in range(no_simulations):
                output = self.simulate(
                    time_start=time,
                    incidence_start=1,
                    incidence_cutoff=incidence_cutoff,
                    rng=rng,
                )
                major_outbreak_indicator_vec[j] = output["outbreak_cutoff_indicator"]
            outbreak_risk = major_outbreak_indicator_vec.mean()
            outbreak_risk_vec[i] = outbreak_risk
        return outbreak_risk_vec

    def instantaneous_outbreak_risk(
        self,
        time_vec,
    ):
        reproduction_no_func = self._reproduction_no_func
        dispersion_param = self._dispersion_param
        reproduction_no_vec = reproduction_no_func(time_vec)
        multiplying_matrix = np.diag(reproduction_no_vec)

        def zero_func(outbreak_risk_vec):
            return (
                1
                - outbreak_risk_vec
                - (
                    1
                    + np.matmul(multiplying_matrix, outbreak_risk_vec)
                    / dispersion_param
                )
                ** (-dispersion_param)
            )

        outbreak_risk_vec_init = 1 - 1 / reproduction_no_vec
        outbreak_risk_vec_init = outbreak_risk_vec_init + zero_func(
            outbreak_risk_vec_init
        )
        outbreak_risk_vec = newton(zero_func, x0=outbreak_risk_vec_init)
        return outbreak_risk_vec


class PeriodicHeterogeneousRenewalModel(HeterogeneousRenewalModel):
    """
    Class for renewal models in hetergeneous populations with periodic transmission.
    """

    def __init__(
        self,
        time_vec,
        reproduction_no_vec,
        generation_time_dist,
        dispersion_param=1.0,
    ):
        def reproduction_no_func(time):
            return np.interp(time, time_vec, reproduction_no_vec, period=len(time_vec))

        super().__init__(reproduction_no_func, generation_time_dist, dispersion_param)
        self._time_vec = time_vec
        self._period = len(time_vec)
        self._reproduction_no_vec = reproduction_no_vec

    def case_outbreak_risk(self, time_vec, **kwargs):
        time_vec_all = self._time_vec
        period = self._period
        outbreak_risk_vec_all = self._case_outbreak_risk_all(**kwargs)
        outbreak_risk_vec = np.interp(
            time_vec, time_vec_all, outbreak_risk_vec_all, period=period
        )
        return outbreak_risk_vec

    def _case_outbreak_risk_all(self, **kwargs):
        reproduction_no_vec = self._reproduction_no_vec
        generation_time_dist = self._generation_time_dist
        dispersion_param = self._dispersion_param
        period = self._period

        if self._generation_time_max > period:
            raise NotImplementedError(
                "Currently, only a maximum generation time less "
                "than the period is supported"
            )
        generation_time_pmf_vec_periodic = generation_time_dist.pmf(
            np.arange(1, period + 1)
        )
        multiplying_matrix = np.zeros((period, period))
        for diagonal in range(-period + 1, period):
            multiplying_matrix = multiplying_matrix + np.diag(
                np.repeat(
                    generation_time_pmf_vec_periodic[diagonal - 1],
                    period - abs(diagonal),
                ),
                diagonal,
            )
        multiplying_matrix = np.matmul(multiplying_matrix, np.diag(reproduction_no_vec))

        def zero_func(outbreak_risk_vec):
            return (
                1
                - outbreak_risk_vec
                - (
                    1
                    + np.matmul(multiplying_matrix, outbreak_risk_vec)
                    / dispersion_param
                )
                ** (-dispersion_param)
            )

        outbreak_risk_vec_init = 1 - 1 / reproduction_no_vec
        for _ in range(50):
            outbreak_risk_vec_init = outbreak_risk_vec_init + zero_func(
                outbreak_risk_vec_init
            )
        outbreak_risk_vec = newton(zero_func, x0=outbreak_risk_vec_init, **kwargs)
        return outbreak_risk_vec
