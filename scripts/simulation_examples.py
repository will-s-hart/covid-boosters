import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import PeriodicHeterogeneousRenewalModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(period)
    peak_transmission_time = default_parameters["peak_transmission_time"]
    reproduction_no_vec = 2 * (
        1 + 0.5 * np.cos(2 * np.pi * (time_vec - peak_transmission_time) / period)
    )
    kwargs_renewal_model = {
        "time_vec": time_vec,
        "reproduction_no_vec": reproduction_no_vec,
        "generation_time_dist": default_parameters["generation_time_dist"],
        "dispersion_param": default_parameters["dispersion_param"],
    }
    renewal_model = PeriodicHeterogeneousRenewalModel(**kwargs_renewal_model)
    time_start = 90
    kwargs_sim = {
        "time_start": time_start,
        "incidence_start": 1,
        "incidence_cutoff": default_parameters["sim_incidence_cutoff"],
        "rng": np.random.default_rng(11),
    }
    no_simulations = 100
    # Reproduction number over time
    df_simulations = pd.DataFrame({"time": np.arange(50)}).set_index("time")
    for simulation in range(no_simulations):
        df_simulations[simulation] = np.zeros(len(df_simulations.index), dtype=int)
        output = renewal_model.simulate(**kwargs_sim)
        df_simulations.loc[output["time_vec"] - time_start, simulation] = output[
            "incidence_vec"
        ]
        if output["outbreak_cutoff_indicator"]:
            df_simulations.loc[
                output["time_vec"][-1] + 1 - time_start :, simulation
            ] = np.nan
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results/simulation_examples"
    results_dir.mkdir(exist_ok=True, parents=True)
    df_simulations.to_csv(results_dir / "simulations.csv")


if __name__ == "__main__":
    run_analyses()
