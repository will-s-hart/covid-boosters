"""
Base module defining main classes and methods.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import newton
from scipy.stats import gamma, poisson


class AntibodyModel:
    """
    Class for modeling antibody dynamics following a single vaccination dose.
    """

    def __init__(self, params):
        self._params = params

    def run(self, time_init, antibody_init, time_vec, time_prev_vaccination=None):
        params = self._params
        log_mrna_dose = params["log_mrna_dose"]
        mrna_decay_rate = params["mrna_decay_rate"]
        delay_to_antibody_response = params["delay_to_antibody_response"]
        max_antibody_production_rate = params["max_antibody_production_rate"]
        mrna_response_steepness = params["mrna_response_steepness"]
        half_maximal_response_log_mrna = params["half_maximal_response_log_mrna"]
        antibody_decay_rate = params["antibody_decay_rate"]

        def ode_func(t, y):
            antibody = y[0]
            if t - time_init < delay_to_antibody_response:
                if time_prev_vaccination is not None:
                    log_mrna = log_mrna_dose - mrna_decay_rate * (
                        t - time_prev_vaccination
                    )
                else:
                    log_mrna = -np.inf
            else:
                log_mrna = log_mrna_dose - mrna_decay_rate * (t - time_init)
            antibody_production_rate = max_antibody_production_rate * (
                1
                / (
                    1
                    + np.exp(
                        -mrna_response_steepness
                        * (log_mrna - half_maximal_response_log_mrna)
                    )
                )
            )
            d_antibody_dt = antibody_production_rate - antibody_decay_rate * antibody
            return [d_antibody_dt]

        ode_solution = solve_ivp(
            ode_func,
            t_span=(time_init, time_vec[-1]),
            y0=[antibody_init],
            t_eval=time_vec,
        )

        antibody_vec = ode_solution.y[0]
        return antibody_vec


class IndividualSusceptibilityModel:
    """
    Class for calculating individual susceptibility based on an antibody dynamics model.
    """

    def __init__(
        self,
        antibody_model_params,
        susceptibility_func_params,
        vaccination_times,
    ):
        self._antibody_model = AntibodyModel(antibody_model_params)
        self._susceptibility_func_params = susceptibility_func_params
        if vaccination_times is None:
            vaccination_times = []
        else:
            vaccination_times = np.array(vaccination_times)
        self._vaccination_times = vaccination_times

    def susceptibility(self, time_vec):
        susceptibility_func_params = self._susceptibility_func_params
        antibody_response_steepness = susceptibility_func_params[
            "antibody_response_steepness"
        ]
        half_protection_antibody = susceptibility_func_params[
            "half_protection_antibody"
        ]
        antibody_vec = self.antibody_titers(time_vec)
        susceptibility_vec = 1 / (
            1 + (antibody_vec / half_protection_antibody) ** antibody_response_steepness
        )
        return susceptibility_vec

    def antibody_titers(self, time_vec):
        antibody_model = self._antibody_model
        vaccination_times = self._vaccination_times
        vaccination_times = vaccination_times[vaccination_times <= np.max(time_vec)]
        antibody_vec = np.zeros(len(time_vec), dtype=float)
        antibody_init_next = 0.0
        for vaccination_index_current, vaccination_time_current in enumerate(
            vaccination_times
        ):
            if vaccination_index_current > 0:
                time_prev_vaccination = vaccination_times[vaccination_index_current - 1]
            else:
                time_prev_vaccination = None
            if vaccination_index_current < len(vaccination_times) - 1:
                vaccination_time_next = vaccination_times[vaccination_index_current + 1]
            else:
                vaccination_time_next = (
                    max(vaccination_time_current, np.max(time_vec)) + 1
                )  # arbitrary
            current_indicator_vec = (time_vec >= vaccination_time_current) & (
                time_vec < vaccination_time_next
            )
            time_vec_current = time_vec[current_indicator_vec]
            antibody_init_current = antibody_init_next
            antibody_vec_current_plus_init_next = antibody_model.run(
                time_init=vaccination_time_current,
                antibody_init=antibody_init_current,
                time_vec=np.append(time_vec_current, vaccination_time_next),
                time_prev_vaccination=time_prev_vaccination,
            )
            antibody_vec_current = antibody_vec_current_plus_init_next[:-1]
            antibody_init_next = antibody_vec_current_plus_init_next[-1]
            antibody_vec[current_indicator_vec] = antibody_vec_current
        return antibody_vec


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
        infectiousness_scaled_incidence = gamma.rvs(
            a=incidence * dispersion_param,
            scale=1 / dispersion_param,
            random_state=rng,
        )
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
                infectiousness_scaled_incidence = gamma.rvs(
                    a=incidence * dispersion_param,
                    scale=1 / dispersion_param,
                    random_state=rng,
                )
            else:
                infectiousness_scaled_incidence = 0
            time_vec = np.append(time_vec, time)
            incidence_vec = np.append(incidence_vec, incidence)
            infectiousness_scaled_incidence_vec = np.append(
                infectiousness_scaled_incidence_vec, infectiousness_scaled_incidence
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
