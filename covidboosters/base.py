"""Base module defining classes and methods."""

import numpy as np
import pandas as pd
import tqdm
from scipy.integrate import solve_ivp
from scipy.optimize import root
from scipy.stats import gamma, poisson


class AntibodyModel:
    """
    Class for modeling antibody dynamics following a single vaccine dose.

    Parameters
    ----------
    params : dict
        Dictionary of parameters for the antibody dynamics model with the following
        keys: "mrna_dose", "mrna_decay_rate", "delay_to_antibody_response",
        "max_antibody_production_rate", "mrna_response_steepness",
        "half_maximal_response_mrna", "antibody_decay_rate".

    """

    def __init__(self, params):
        """Initialize the antibody dynamics model."""
        self._params = params

    def run(self, time_init, antibody_init, time_vec, time_prev_vaccination=None):
        """Run the model to calculate antibody dynamics following a vaccine dose.

        Parameters
        ----------
        time_init : int
            Time of vaccination.
        antibody_init : float
            Initial antibody titer prior to vaccination.
        time_vec : array-like of int
            Time points at which to calculate antibody titer.
        time_prev_vaccination : int, optional
            Time of the previous vaccination, if any (used for determining antibody
            dynamics during the delay period before the antibody response to the current
            vaccination).

        Returns
        -------
        antibody_vec : array-like
            Antibody titer at each time point in `time_vec`.

        """
        params = self._params
        log_mrna_dose = np.log(params["mrna_dose"])
        mrna_decay_rate = params["mrna_decay_rate"]
        delay_to_antibody_response = params["delay_to_antibody_response"]
        max_antibody_production_rate = params["max_antibody_production_rate"]
        mrna_response_steepness = params["mrna_response_steepness"]
        half_maximal_response_log_mrna = np.log(params["half_maximal_response_mrna"])
        antibody_decay_rate = params["antibody_decay_rate"]

        def _ode_func(t, y):
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
            _ode_func,
            t_span=(time_init, time_vec[-1]),
            y0=[antibody_init],
            t_eval=time_vec,
        )

        antibody_vec = ode_solution.y[0]
        return antibody_vec


class IndividualSusceptibilityModel:
    """
    Individual susceptibility model.

    Class for calculating individual susceptibility under (potentially) multiple
    vaccine doses, based on an antibody dynamics model.

    Parameters
    ----------
    vaccination_times : array-like of int, or None
        Times of vaccination. If set to None, no vaccination is assumed.
    antibody_model_params : dict
        Dictionary of parameters for the antibody dynamics model (see `AntibodyModel`).
    susceptibility_func_params : dict
        Dictionary of parameters for the susceptibility function with the following
        keys: "antibody_response_steepness", "half_protection_antibody".

    """

    def __init__(
        self,
        vaccination_times,
        antibody_model_params,
        susceptibility_func_params,
    ):
        """Initialize the individual susceptibility model."""
        if vaccination_times is None:
            vaccination_times = np.array([])
        else:
            vaccination_times = np.array(vaccination_times)
        self._vaccination_times = vaccination_times
        self._antibody_model_params = antibody_model_params
        self._antibody_model = AntibodyModel(antibody_model_params)
        self._susceptibility_func_params = susceptibility_func_params

    def antibodies(self, time_vec, **_):
        """
        Calculate antibody titer over time.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate antibody titer.

        Returns
        -------
        antibody_vec : array-like of float
            Antibody titer at each time point in `time_vec`.

        """
        antibody_model = self._antibody_model
        vaccination_times = self._vaccination_times
        vaccination_times = vaccination_times[vaccination_times <= np.max(time_vec)]
        antibody_vec = np.zeros(len(time_vec), dtype=float)
        antibody_init_next = 0.0
        # Loop through times between vaccine doses
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

    def susceptibility(self, time_vec, **_):
        """
        Calculate susceptibility over time.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate susceptibility.

        Returns
        -------
        susceptibility_vec : array-like of float
            Susceptibility at each time point in `time_vec`.

        """
        susceptibility_func_params = self._susceptibility_func_params
        antibody_response_steepness = susceptibility_func_params[
            "antibody_response_steepness"
        ]
        half_protection_antibody = susceptibility_func_params[
            "half_protection_antibody"
        ]
        antibody_vec = self.antibodies(time_vec, **_)
        susceptibility_vec = 1 / (
            1 + (antibody_vec / half_protection_antibody) ** antibody_response_steepness
        )
        return susceptibility_vec


class PeriodicIndividualSusceptibilityModel(IndividualSusceptibilityModel):
    """
    Individual susceptibility model in a periodic setting.

    Class for calculating individual susceptibility based on an antibody dynamics model
    in a periodic setting.

    Extends `IndividualSusceptibilityModel`.

    Parameters
    ----------
    period : int
        Period of repeating dynamics.
    vaccination_times : array-like of int
        Times of vaccination within each period.
    antibody_model_params : dict
        Dictionary of parameters for the antibody dynamics model (see `AntibodyModel`).
    susceptibility_func_params : dict
        Dictionary of parameters for the susceptibility function with the following
        keys: "antibody_response_steepness", "half_protection_antibody".

    """

    def __init__(
        self,
        period,
        vaccination_times,
        antibody_model_params,
        susceptibility_func_params,
    ):
        """Initialize the periodic individual susceptibility model."""
        super().__init__(
            vaccination_times=vaccination_times,
            antibody_model_params=antibody_model_params,
            susceptibility_func_params=susceptibility_func_params,
        )
        if np.any(self._vaccination_times < 0) or np.any(
            self._vaccination_times >= period
        ):
            raise ValueError("Vaccination times must be between 0 and the period")
        self._period = period

    def antibodies(self, time_vec, **kwargs):
        """
        Calculate antibody titer over time (after convergence to a periodic pattern).

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate antibody titer.
        initial_periods : int, optional
            Number of periods to simulate before time 0 to ensure convergence to a
            periodic pattern. Default is 5.

        Returns
        -------
        antibody_vec : array-like of float
            Antibody titer at each time point in `time_vec`.

        """
        initial_periods = kwargs.get("initial_periods", 5)
        period = self._period
        vaccination_times = (
            self._vaccination_times
            + np.arange(-initial_periods * period, np.max(time_vec), period)[
                np.newaxis
            ].T
        ).flatten()
        antibody_vec = IndividualSusceptibilityModel(
            vaccination_times=vaccination_times,
            antibody_model_params=self._antibody_model_params,
            susceptibility_func_params=self._susceptibility_func_params,
        ).antibodies(time_vec)
        return antibody_vec


class PopulationSusceptibilityModel:
    """
    Population susceptibility model.

    Class for simulating susceptibility under periodic booster vaccination in a
    population with heterogeneous antibody dynamics.

    Parameters
    ----------
    period : int
        Period of repeating dynamics.
    vaccination_time_range : list of int, int, or None, optional
        Time range for vaccination in each period. If a list, vaccines are distributed
        uniformly within the range (excluding the right end point). If an int, all
        vaccines are given at the single time point. If None (default), no vaccination
        is assumed.
    proportion_vaccinated : float, optional
        Proportion of the population vaccinated each period. Default is 0.
    antibody_model_params_pop : dict, optional
        Dictionary of population median parameters for the antibody dynamics model.
        Keys are as for the `params` argument of `AntibodyModel`. If not provided,
        individuals are assumed to have constant susceptibility over time.
    susceptibility_func_params : dict
        Dictionary of parameters for the susceptibility function with the following
        keys: "antibody_response_steepness", "half_protection_antibody".
    antibody_model_params_random_effects : dict, optional
        Dictionary of random effects on the antibody model parameters. Keys are the
        same as for `antibody_model_params_pop`. If not provided, no random effects
        are assumed.
    population_size : int, optional
        Number of individuals to simulate antibody dynamics for in order to calculate
        population susceptibility. Default is 1.
    rng : numpy.random.Generator, optional
        Random number generator. If not provided, a new generator is created.
    rng_seed : int, optional
        Seed for the random number generator. Only used if `rng` is not provided. If
        neither `rng` nor `rng_seed` are provided, a generator is created with default
        settings.

    """

    def __init__(
        self,
        period,
        vaccination_time_range=None,
        proportion_vaccinated=0,
        antibody_model_params_pop=None,
        susceptibility_func_params=None,
        antibody_model_params_random_effects=None,
        population_size=1,
        rng=None,
        rng_seed=None,
    ):
        if (
            antibody_model_params_random_effects is None
            and antibody_model_params_pop is not None
        ):
            antibody_model_params_random_effects = {
                param_name: 0 for param_name in antibody_model_params_pop
            }
        if rng is None:
            rng = np.random.default_rng(rng_seed)
        if np.issubdtype(type(vaccination_time_range), np.number):
            vaccination_time_range = [
                vaccination_time_range,
                vaccination_time_range + 1,
            ]
        self._period = period
        self._vaccination_time_range = vaccination_time_range
        self._proportion_vaccinated = proportion_vaccinated
        self._susceptibility_func_params = susceptibility_func_params
        self._population_size = population_size
        if antibody_model_params_pop is not None:
            self._susceptibility_vec_all_0 = None
            self._susceptibility_vec_all_0_kwargs = None
            antibody_model_params_by_indiv = []
            for _ in range(population_size):
                # Sample individual-specific antibody model parameters
                antibody_model_params = {}
                for param_name, param_pop in antibody_model_params_pop.items():
                    param_random_effect = antibody_model_params_random_effects[
                        param_name
                    ]
                    antibody_model_params[param_name] = param_pop * np.exp(
                        param_random_effect * rng.standard_normal()
                    )
                antibody_model_params_by_indiv.append(antibody_model_params)
            self._antibody_model_params_by_indiv = antibody_model_params_by_indiv
        else:
            self._susceptibility_vec_all_0 = np.ones(period)
            self._susceptibility_vec_all_0_kwargs = {}
            self._antibody_model_params_by_indiv = None

    def susceptibility(self, time_vec, **kwargs):
        """
        Calculate population susceptibility over time.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate susceptibility.

        Returns
        -------
        susceptibility_vec : array-like of float
            Susceptibility at each time point in `time_vec`.

        """
        period = self._period
        time_vec_all = np.arange(period)
        susceptibility_vec_all = self._susceptibility_all(**kwargs)
        susceptibility_vec = np.interp(
            time_vec, time_vec_all, susceptibility_vec_all, period=period
        )
        return susceptibility_vec

    def update_vaccination_params(
        self, vaccination_time_range=None, proportion_vaccinated=None
    ):
        """
        Update time range of vaccination and/or proportion of vaccinated individuals.

        This allows different vaccination strategies to be compared without needing to
        resimulate individual antibody dynamics.

        Parameters
        ----------
        vaccination_time_range : list of int, int, or None, optional
            Time range for vaccination in each period (see class docstring for details).
            If None, the current value is retained.
        proportion_vaccinated : float, optional
            Proportion of the population vaccinated each period. If None, the current
            value is retained.

        Returns
        -------
        None

        """
        if vaccination_time_range is not None:
            if isinstance(vaccination_time_range, (int, float)):
                vaccination_time_range = [
                    vaccination_time_range,
                    vaccination_time_range + 1,
                ]
            self._vaccination_time_range = vaccination_time_range
        if proportion_vaccinated is not None:
            self._proportion_vaccinated = proportion_vaccinated

    def save_susceptibility_all_0(self, file_path):
        """
        Save susceptibility values assuming all individuals are vaccinated at time 0.

        Saves the population susceptibility values assuming all individuals are
        vaccinated at time 0 to a CSV file. The susceptiblity values are calculated
        before saving if necessary. Note that these values are then used to compare
        different vaccination strategies without needing to store or resimulate
        individual antibody dynamics.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to save the susceptibility values to.

        Returns
        -------
        None

        """
        if self._susceptibility_vec_all_0 is None:
            self._calculate_susceptibility_all_0()
        time_vec_all = np.arange(self._period)
        susceptibility_vec_all_0 = self._susceptibility_vec_all_0
        susceptibility_all_0_df = pd.DataFrame(
            {"time": time_vec_all, "susceptibility": susceptibility_vec_all_0},
        )
        susceptibility_all_0_df.set_index("time", inplace=True)
        susceptibility_all_0_df.to_csv(file_path)

    def load_susceptibility_all_0(self, file_path, kwargs_used=None):
        """
        Load susceptibility values assuming all individuals are vaccinated at time 0.

        Loads the population susceptibility values assuming all individuals are
        vaccinated at time 0 from a CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to load the susceptibility values from.
        kwargs_used : dict, optional
            Keyword arguments that were used in the calculation of the susceptibility
            values (i.e., keyword arguments passed to the last call to the
            `susceptibility` method, if any).

        Returns
        -------
        None

        """
        susceptibility_all_0_df = pd.read_csv(file_path, index_col="time")
        if not np.array_equal(
            susceptibility_all_0_df.index.to_numpy(), np.arange(self._period)
        ):
            raise ValueError("Time indices in the file do not match the period")
        self._susceptibility_vec_all_0 = susceptibility_all_0_df[
            "susceptibility"
        ].to_numpy()
        self._susceptibility_vec_all_0_kwargs = kwargs_used or {}

    def _susceptibility_all(self, **kwargs):
        # Calculate population susceptibility at each time point in the period
        period = self._period
        vaccination_time_range = self._vaccination_time_range
        proportion_vaccinated = self._proportion_vaccinated
        time_vec_all = np.arange(period)
        if (
            vaccination_time_range in [None, []]
            or vaccination_time_range[1] == vaccination_time_range[0]
            or proportion_vaccinated == 0
        ):
            return np.ones(period)
        if (
            self._susceptibility_vec_all_0 is None
            or kwargs != self._susceptibility_vec_all_0_kwargs
        ):
            self._calculate_susceptibility_all_0(**kwargs)
        susceptibility_vec_all_0 = self._susceptibility_vec_all_0
        shifted_time_mat = (
            time_vec_all[:, np.newaxis]
            - np.arange(vaccination_time_range[0], vaccination_time_range[1])[
                :, np.newaxis
            ].T
        )
        susceptibility_vec_all_vaccinated = np.mean(
            np.interp(
                shifted_time_mat, time_vec_all, susceptibility_vec_all_0, period=period
            ),
            axis=1,
        )
        susceptibility_vec_all = (
            proportion_vaccinated * susceptibility_vec_all_vaccinated
            + (1 - proportion_vaccinated)
        )
        return susceptibility_vec_all

    def _calculate_susceptibility_all_0(self, **kwargs):
        # Get susceptibility assuming all individuals are vaccinated at time 0
        period = self._period
        susceptibility_func_params = self._susceptibility_func_params
        antibody_model_params_by_indiv = self._antibody_model_params_by_indiv
        population_size = self._population_size
        time_vec_all = np.arange(period)
        cumulative_susceptibility_vec = np.zeros(len(time_vec_all))
        for antibody_model_params in antibody_model_params_by_indiv:
            susceptibility_vec = PeriodicIndividualSusceptibilityModel(
                vaccination_times=0,
                antibody_model_params=antibody_model_params,
                susceptibility_func_params=susceptibility_func_params,
                period=period,
            ).susceptibility(time_vec_all, **kwargs)
            cumulative_susceptibility_vec += susceptibility_vec
        susceptibility_vec = cumulative_susceptibility_vec / population_size
        self._susceptibility_vec_all_0 = susceptibility_vec
        self._susceptibility_vec_all_0_kwargs = kwargs


class HeterogeneousRenewalModel:
    """
    Base class for generalised renewal models incorporating individual heterogeneity.

    Parameters
    ----------
    reproduction_no_func : callable
        Function that returns the reproduction number at each time point.
    generation_time_dist : scipy.stats.rv_discrete
        Discrete distribution of the generation time. Must have a finite support.
    dispersion_param : float, optional
        Dispersion parameter for the negative binomial offspring distribution. Default
        is 1.0.

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
        incidence_cutoff=100,
        rng=None,
        rng_seed=None,
    ):
        """
        Simulate an outbreak.

        Parameters
        ----------
        time_start : int, optional
            Time at which the outbreak starts. Default is 0.
        incidence_start : int, optional
            Incidence of new infections at time `time_start`. Default is 1.
        incidence_cutoff : int, optional
            Incidence threshold at which to stop the simulation. Default is 100.
        rng : numpy.random.Generator, optional
            Random number generator. If not provided, a new generator is created.
        rng_seed : int, optional
            Seed for the random number generator. Only used if `rng` is not provided. If
            neither `rng` nor `rng_seed` are provided, a generator is created with
            default settings.

        Returns
        -------
        output : dict
            Dictionary with keys "time_vec" (time points), "incidence_vec" (incidence
            at each time point), and "outbreak_cutoff_indicator" (boolean indicating
            whether the outbreak was stopped due to the incidence threshold being
            reached).

        """
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
        **kwargs,
    ):
        """
        Calculate the outbreak risk at each time point by simulating multiple outbreaks.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the outbreak risk.
        incidence_cutoff : int, optional
            Incidence threshold above which an outbreak is considered major. Default is
            100.
        no_simulations : int, optional
            Number of simulations to run at each time point. Default is 1000.
        rng : numpy.random.Generator, optional
            Random number generator. If not provided, a new generator is created.
        rng_seed : int, optional
            Seed for the random number generator. Only used if `rng` is not provided. If
            neither `rng` nor `rng_seed` are provided, a generator is created with
            default settings.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Outbreak risk at each time point in `time_vec`.

        """
        incidence_cutoff = kwargs.get("incidence_cutoff", 100)
        no_simulations = kwargs.get("no_simulations", 1000)
        rng = kwargs.get("rng", None)
        rng_seed = kwargs.get("rng_seed", None)
        if rng is None:
            rng = np.random.default_rng(rng_seed)
        outbreak_risk_vec = np.zeros(len(time_vec))
        pbar = tqdm.tqdm(total=len(time_vec) * no_simulations)
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
                pbar.update()
            outbreak_risk = major_outbreak_indicator_vec.mean()
            outbreak_risk_vec[i] = outbreak_risk
        pbar.close()
        return outbreak_risk_vec

    def instantaneous_outbreak_risk(
        self,
        time_vec,
        **kwargs,
    ):
        """
        Calculate the instantaneous outbreak risk at each time point.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the instantaneous outbreak risk.
        **kwargs
            Keyword arguments to pass to the `scipy.optimize.root` function used to
            solve the nonlinear system satisfied by the outbreak risk values.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Instantaneous outbreak risk at each time point in `time_vec`.

        """
        reproduction_no_func = self._reproduction_no_func
        dispersion_param = self._dispersion_param
        reproduction_no_vec = reproduction_no_func(time_vec)
        multiplying_matrix = np.diag(reproduction_no_vec)

        def _zero_func(outbreak_risk_vec):
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

        outbreak_risk_vec_init = np.ones(len(time_vec))
        outbreak_risk_vec = root(
            _zero_func,
            x0=outbreak_risk_vec_init,
            **kwargs,
        ).x
        return outbreak_risk_vec


class PeriodicHeterogeneousRenewalModel(HeterogeneousRenewalModel):
    """
    Periodic generalised renewal model incorporating individual heterogeneity.

    Extends `HeterogeneousRenewalModel`.

    Parameters
    ----------
    time_vec : array-like of int
        Array of consecutive integers defining all time points over a single period.
    reproduction_no_vec : array-like of float
        Array of reproduction numbers at each time point in `time_vec`.
    generation_time_dist : scipy.stats.rv_discrete
        Discrete distribution of the generation time. Must have a finite support.
    dispersion_param : float, optional
        Dispersion parameter for the negative binomial offspring distribution. Default
        is 1.0.

    """

    def __init__(
        self,
        time_vec,
        reproduction_no_vec,
        generation_time_dist,
        dispersion_param,
    ):
        def reproduction_no_func(time):
            return np.interp(time, time_vec, reproduction_no_vec, period=len(time_vec))

        super().__init__(reproduction_no_func, generation_time_dist, dispersion_param)
        self._time_vec = time_vec
        self._period = len(time_vec)
        self._reproduction_no_vec = reproduction_no_vec

    def case_outbreak_risk(self, time_vec, **kwargs):
        """
        Calculate the outbreak risk at each time point.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the outbreak risk.
        **kwargs
            Keyword arguments to pass to the `scipy.optimize.root` function used to
            solve the nonlinear system satisfied by the outbreak risk values.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Outbreak risk at each time point in `time_vec`.

        """
        time_vec_all = self._time_vec
        period = self._period
        outbreak_risk_vec_all = self._case_outbreak_risk_all(**kwargs)
        outbreak_risk_vec = np.interp(
            time_vec, time_vec_all, outbreak_risk_vec_all, period=period
        )
        return outbreak_risk_vec

    def simulated_outbreak_risk(self, time_vec, **kwargs):
        """
        Calculate the outbreak risk at each time point by simulating multiple outbreaks.

        Overrides the method in the base class to avoid recalculating the outbreak risk
        after multiples of the period.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the outbreak risk.
        incidence_cutoff : int, optional
            Incidence threshold at/above which an outbreak is considered major. Default
            is 100.
        no_simulations : int, optional
            Number of simulations to run at each time point. Default is 1000.
        rng : numpy.random.Generator, optional
            Random number generator. If not provided, a new generator is created.
        rng_seed : int, optional
            Seed for the random number generator. Only used if `rng` is not provided. If
            neither `rng` nor `rng_seed` are provided, a generator is created with
            default settings.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Outbreak risk at each time point in `time_vec`.

        """
        period = self._period
        time_vec_reduced = np.unique(time_vec % period)
        outbreak_risk_vec_reduced = super().simulated_outbreak_risk(
            time_vec_reduced, **kwargs
        )
        outbreak_risk_vec = np.interp(
            time_vec, time_vec_reduced, outbreak_risk_vec_reduced, period=period
        )
        return outbreak_risk_vec

    def _case_outbreak_risk_all(self, **kwargs):
        # Calculate the outbreak risk at each time point in the period
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

        def _zero_func(outbreak_risk_vec):
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

        outbreak_risk_vec_init = np.ones(period)
        outbreak_risk_vec = root(
            _zero_func,
            x0=outbreak_risk_vec_init,
            **kwargs,
        ).x
        return outbreak_risk_vec


class OutbreakRiskModel:
    """
    Class for outbreak risk calculations with periodic transmission and vaccination.

    Parameters
    ----------
    period : int
        Period of repeating dynamics.
    unvaccinated_reproduction_no_mean : float
        Temporal mean of the reproduction number before vaccination (which is assumed
        to follow a sinusoidal pattern).
    unvaccinated_reproduction_no_prop_variation : float
        Proportion by which the reproduction number before vaccination varies from its
        temporal mean.
    peak_transmission_time : int
        Time at which the reproduction number before vaccination peaks (in the period).
    generation_time_dist : scipy.stats.rv_discrete
        Discrete distribution of the generation time. Must have a finite support.
    dispersion_param : float
        Dispersion parameter for the negative binomial offspring distribution.
    vaccination_time_range : list of int, int, or None, optional
        Time range for vaccination in each period. If a list, vaccines are distributed
        uniformly within the range (excluding the right end point). If an int, all
        vaccines are given at the single time point. If None (default), no vaccination
        is assumed.
    proportion_vaccinated : float, optional
        Proportion of the population vaccinated each period. Default is 0.
    antibody_model_params_pop : dict, optional
        Dictionary of population median parameters for the antibody dynamics model.
        Keys are as for the `params` argument of `AntibodyModel`. If not provided,
        individuals are assumed to have constant susceptibility over time.
    susceptibility_func_params : dict
        Dictionary of parameters for the susceptibility function with the following
        keys: "antibody_response_steepness", "half_protection_antibody".
    antibody_model_params_random_effects : dict, optional
        Dictionary of random effects on the antibody model parameters. Keys are the
        same as for `antibody_model_params_pop`. If not provided, no random effects
        are assumed.
    population_size : int, optional
        Number of individuals to simulate antibody dynamics for in order to calculate
        population susceptibility. Default is 1.
    rng : numpy.random.Generator, optional
        Random number generator. If not provided, a new generator is created.
    rng_seed : int, optional
        Seed for the random number generator. Only used if `rng` is not provided. If
        neither `rng` nor `rng_seed` are provided, a generator is created with default
        settings.

    """

    def __init__(
        self,
        period,
        unvaccinated_reproduction_no_mean,
        unvaccinated_reproduction_no_prop_variation,
        peak_transmission_time,
        generation_time_dist,
        dispersion_param,
        vaccination_time_range=None,
        proportion_vaccinated=0,
        antibody_model_params_pop=None,
        susceptibility_func_params=None,
        antibody_model_params_random_effects=None,
        population_size=1,
        rng=None,
        rng_seed=None,
    ):
        if rng is None:
            rng = np.random.default_rng(rng_seed)
        self._susceptibility_model = PopulationSusceptibilityModel(
            period=period,
            vaccination_time_range=vaccination_time_range,
            proportion_vaccinated=proportion_vaccinated,
            antibody_model_params_pop=antibody_model_params_pop,
            antibody_model_params_random_effects=antibody_model_params_random_effects,
            susceptibility_func_params=susceptibility_func_params,
            population_size=population_size,
            rng=rng,
        )
        time_vec = np.arange(period)
        unvaccinated_reproduction_no_vec = unvaccinated_reproduction_no_mean * (
            1
            + unvaccinated_reproduction_no_prop_variation
            * np.cos(2 * np.pi * (time_vec - peak_transmission_time) / period)
        )
        self._period = period
        self._time_vec = time_vec
        self._unvaccinated_reproduction_no_vec = unvaccinated_reproduction_no_vec
        self._generation_time_dist = generation_time_dist
        self._dispersion_param = dispersion_param
        self._rng = rng
        self._susceptibility_vec = None
        self._reproduction_no_vec = None
        self._renewal_model = None

    def reproduction_no(self, time_vec):
        """
        Calculate the reproduction number at the specified time points.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the reproduction number.

        Returns
        -------
        reproduction_no_vec : array-like of float
            Reproduction number at each time point in `time_vec`.

        """
        if self._renewal_model is None:
            self._build_renewal_model()
        time_vec_all = self._time_vec
        reproduction_no_vec_all = self._reproduction_no_vec
        period = self._period
        reproduction_no_vec = np.interp(
            time_vec, time_vec_all, reproduction_no_vec_all, period=period
        )
        return reproduction_no_vec

    def unvaccinated_reproduction_no(self, time_vec):
        """
        Calculate the reproduction number without vaccination at the specified time points.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the reproduction number.

        Returns
        -------
        unvaccinated_reproduction_no_vec : array-like of float
            Reproduction number in the absence of vaccination at each time point in
            `time_vec`.

        """
        if self._renewal_model is None:
            self._build_renewal_model()
        time_vec_all = self._time_vec
        unvaccinated_reproduction_no_vec_all = self._unvaccinated_reproduction_no_vec
        period = self._period
        unvaccinated_reproduction_no_vec = np.interp(
            time_vec, time_vec_all, unvaccinated_reproduction_no_vec_all, period=period
        )
        return unvaccinated_reproduction_no_vec

    def susceptibility(self, time_vec):
        """
        Calculate population average susceptibility at the specified time points.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate susceptibility.

        Returns
        -------
        susceptibility_vec : array-like of float
            Susceptibility at each time point in `time_vec`.

        """
        if self._renewal_model is None:
            self._build_renewal_model()
        time_vec_all = self._time_vec
        susceptibility_vec_all = self._susceptibility_vec
        period = self._period
        susceptibility_vec = np.interp(
            time_vec, time_vec_all, susceptibility_vec_all, period=period
        )
        return susceptibility_vec

    def case_outbreak_risk(self, time_vec, **kwargs):
        """
        Calculate the outbreak risk at the specified time points.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the outbreak risk.
        **kwargs
            Keyword arguments to pass to the `scipy.optimize.root` function used to
            solve the nonlinear system satisfied by the outbreak risk values.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Outbreak risk at each time point in `time_vec`.

        """
        if self._renewal_model is None:
            self._build_renewal_model()
        return self._renewal_model.case_outbreak_risk(time_vec, **kwargs)

    def instantaneous_outbreak_risk(self, time_vec, **kwargs):
        """
        Calculate the instantaneous outbreak risk at the specified time points.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the instantaneous outbreak risk.

        Returns
        -------
        outbreak_risk_vec : array-like of float
            Instantaneous outbreak risk at each time point in `time_vec`.

        """
        if self._renewal_model is None:
            self._build_renewal_model()
        return self._renewal_model.instantaneous_outbreak_risk(time_vec, **kwargs)

    def simulated_outbreak_risk(self, time_vec, **kwargs):
        """
        Calculate the outbreak risk at the specified time points via simulation.

        Parameters
        ----------
        time_vec : array-like of int
            Time points at which to calculate the outbreak risk.
        incidence_cutoff : int, optional
            Incidence threshold at/above which an outbreak is considered major. Default
            is 100.
        no_simulations : int, optional
            Number of simulations to run at each time point. Default is 1000.
        rng : numpy.random.Generator, optional
            Random number generator. If not provided, a new generator is created.
        rng_seed : int, optional
            Seed for the random number generator. Only used if `rng` is not provided. If
            neither `rng` nor `rng_seed` are provided, a generator is created with
            default settings.

        """
        rng = self._rng
        if self._renewal_model is None:
            self._build_renewal_model()
        if "rng" not in kwargs and "rng_seed" not in kwargs:
            kwargs["rng"] = rng
        return self._renewal_model.simulated_outbreak_risk(time_vec, **kwargs)

    def update_vaccination_params(
        self, vaccination_time_range=None, proportion_vaccinated=None
    ):
        """
        Update time range of vaccination and/or proportion of vaccinated individuals.

        This allows different vaccination strategies to be compared without needing to
        resimulate individual antibody dynamics.

        Parameters
        ----------
        vaccination_time_range : list of int, int, or None, optional
            Time range for vaccination in each period (see class docstring for details).
            If None, the current value is retained.
        proportion_vaccinated : float, optional
            Proportion of the population vaccinated each period. If None, the current
            value is retained.

        Returns
        -------
        None

        """
        self._susceptibility_model.update_vaccination_params(
            vaccination_time_range=vaccination_time_range,
            proportion_vaccinated=proportion_vaccinated,
        )
        self._susceptibility_vec = None
        self._reproduction_no_vec = None
        self._renewal_model = None

    def save_susceptibility_all_0(self, file_path):
        """
        Save susceptibility values assuming all individuals are vaccinated at time 0.

        Saves the population susceptibility values assuming all individuals are
        vaccinated at time 0 to a CSV file. The susceptiblity values are calculated
        before saving if necessary. Note that these values are then used to compare
        different vaccination strategies without needing to store or resimulate
        individual antibody dynamics.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to save the susceptibility values to.

        Returns
        -------
        None

        """
        self._susceptibility_model.save_susceptibility_all_0(file_path)

    def load_susceptibility_all_0(self, file_path):
        """
        Load susceptibility values assuming all individuals are vaccinated at time 0.

        Loads the population susceptibility values assuming all individuals are
        vaccinated at time 0 from a CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to load the susceptibility values from.

        Returns
        -------
        None

        """
        self._susceptibility_model.load_susceptibility_all_0(
            file_path, kwargs_used=None
        )

    def _build_renewal_model(self):
        # Helper method to compute the susceptibility and reproduction number values
        # under vaccination and create a PeriodicHeterogeneousRenewalModel object
        time_vec = self._time_vec
        unvaccinated_reproduction_no_vec = self._unvaccinated_reproduction_no_vec
        generation_time_dist = self._generation_time_dist
        dispersion_param = self._dispersion_param
        susceptibility_vec = self._susceptibility_model.susceptibility(time_vec)
        reproduction_no_vec = unvaccinated_reproduction_no_vec * susceptibility_vec
        renewal_model = PeriodicHeterogeneousRenewalModel(
            time_vec=time_vec,
            reproduction_no_vec=reproduction_no_vec,
            generation_time_dist=generation_time_dist,
            dispersion_param=dispersion_param,
        )
        self._susceptibility_vec = susceptibility_vec
        self._reproduction_no_vec = reproduction_no_vec
        self._renewal_model = renewal_model
