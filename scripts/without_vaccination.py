"""
Script to run simple illustrative analysis of outbreak risk with periodic transmission.

A sinusoidally varying reproduction number is assumed, with no vaccination. Outbreak
risk values are calculated analytically and via simulation for different values of the
dispersion parameter of the negative binomial offspring distribution. The results are
saved in the `results/without_vaccination` directory.
"""

import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import OutbreakRiskModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    """Run the analyses."""
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(2 * period)
    if period == 365:
        month_starts = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30])
        time_vec_sor = np.concatenate((month_starts, month_starts + period))
    elif period == 360:
        time_vec_sor = np.arange(2 * period, step=30)
    else:
        raise NotImplementedError("Only periods of 365 or 360 are currently supported.")
    kwargs_outbreak_risk_model = {
        "period": period,
        "peak_transmission_time": default_parameters["peak_transmission_time"],
        "generation_time_dist": default_parameters["generation_time_dist"],
        "unvaccinated_reproduction_no_mean": 2,
        "unvaccinated_reproduction_no_prop_variation": 0.5,
        "rng_seed": 2,
    }
    kwargs_sor = {
        "incidence_cutoff": default_parameters["sim_incidence_cutoff"],
        "no_simulations": default_parameters["no_simulations"],
    }
    # Reproduction number over time
    df_reproduction_number = pd.DataFrame({"time": time_vec})
    df_reproduction_number.set_index("time", inplace=True)
    df_reproduction_number["r"] = OutbreakRiskModel(
        dispersion_param=1, **kwargs_outbreak_risk_model
    ).reproduction_no(time_vec)
    # Comparison of COR/SOR values for different values of the dispersion parameter
    dispersion_param_vals = [
        0.1,
        default_parameters["dispersion_param"],
        1,
        10,
        100,
        1000000,
    ]
    df_analytic = pd.DataFrame({"time": time_vec})
    df_analytic.set_index("time", inplace=True)
    df_simulated = pd.DataFrame({"time": time_vec_sor})
    df_simulated.set_index("time", inplace=True)
    for dispersion_param in dispersion_param_vals:
        print(f"Dispersion parameter: {dispersion_param}")
        outbreak_risk_model_curr = OutbreakRiskModel(
            dispersion_param=dispersion_param,
            **kwargs_outbreak_risk_model,
        )
        df_analytic[f"{dispersion_param}"] = (
            outbreak_risk_model_curr.case_outbreak_risk(time_vec)
        )
        print(
            f"Running {kwargs_sor['no_simulations']} simulations starting at each of "
            f"{len(time_vec_sor)} time points"
        )
        df_simulated[f"{dispersion_param}"] = (
            outbreak_risk_model_curr.simulated_outbreak_risk(time_vec_sor, **kwargs_sor)
        )
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results/without_vaccination"
    results_dir.mkdir(exist_ok=True, parents=True)
    df_reproduction_number.to_csv(results_dir / "reproduction_number.csv")
    df_analytic.to_csv(results_dir / "analytic.csv")
    df_simulated.to_csv(results_dir / "simulated.csv")


if __name__ == "__main__":
    run_analyses()
