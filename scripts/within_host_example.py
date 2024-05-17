import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import IndividualSusceptibilityModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(period)
    # Example of antibody and susceptibility dynamics following vaccination
    kwargs_individual_susceptibility_model = {
        "antibody_model_params": default_parameters["antibody_model_params_pop"],
        "susceptibility_func_params": default_parameters["susceptibility_func_params"],
        "vaccination_times": 0,
    }
    individual_susceptibility_model = IndividualSusceptibilityModel(
        **kwargs_individual_susceptibility_model
    )
    df = pd.DataFrame({"time": time_vec})
    df.set_index("time", inplace=True)
    df["antibodies"] = individual_susceptibility_model.antibodies(time_vec)
    df["susceptibility"] = individual_susceptibility_model.susceptibility(time_vec)
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results"
    results_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(results_dir / "within_host_example.csv")


if __name__ == "__main__":
    run_analyses()
