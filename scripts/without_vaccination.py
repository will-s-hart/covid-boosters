import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import OutbreakRiskModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(2 * period)
    # Comparison of COR, IOR, and SOR for a single example with no vaccination
    kwargs_outbreak_risk_model_methods = {
        "period": default_parameters["period"],
        "peak_transmission_time": default_parameters["peak_transmission_time"],
        "generation_time_dist": default_parameters["generation_time_dist"],
        "unvaccinated_reproduction_no_mean": 2,
        "unvaccinated_reproduction_no_prop_variation": 0.5,
        "dispersion_param": 0.5,
        "rng_seed": 2,
    }
    outbreak_risk_model_methods = OutbreakRiskModel(
        **kwargs_outbreak_risk_model_methods
    )
    df_methods = pd.DataFrame({"time": time_vec})
    df_methods.set_index("time", inplace=True)
    df_methods["r"] = outbreak_risk_model_methods.reproduction_no(time_vec)
    df_methods["cor"] = outbreak_risk_model_methods.case_outbreak_risk(time_vec)
    df_methods["ior"] = outbreak_risk_model_methods.instantaneous_outbreak_risk(
        time_vec
    )
    time_vec_sor = np.arange(2 * period, step=30)
    kwargs_sor = {
        "incidence_cutoff": default_parameters["sim_incidence_cutoff"],
        "no_simulations": default_parameters["no_simulations"],
    }
    df_methods.loc[time_vec_sor, "sor"] = (
        outbreak_risk_model_methods.simulated_outbreak_risk(time_vec_sor, **kwargs_sor)
    )
    # Comparison of COR values for different values of the dispersion parameter
    dispersion_param_vals = [0.1, 0.5, 1, 10, 100]
    df_dispersion = pd.DataFrame({"time": time_vec})
    df_dispersion.set_index("time", inplace=True)
    for dispersion_param in dispersion_param_vals:
        outbreak_risk_model_curr = OutbreakRiskModel(
            **{
                **kwargs_outbreak_risk_model_methods,
                "dispersion_param": dispersion_param,
            }
        )
        df_dispersion[f"{dispersion_param}"] = (
            outbreak_risk_model_curr.case_outbreak_risk(time_vec)
        )
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results/without_vaccination"
    results_dir.mkdir(exist_ok=True, parents=True)
    df_methods.to_csv(results_dir / "methods.csv")
    df_dispersion.to_csv(results_dir / "dispersion.csv")


if __name__ == "__main__":
    run_analyses()
