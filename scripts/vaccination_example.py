import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

import numpy as np
import pandas as pd

from covidboosters import OutbreakRiskModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    time_vec = np.arange(2 * period)
    # Example of COR with vaccination
    kwargs_outbreak_risk_model = {
        key: default_parameters[key]
        for key in [
            "period",
            "unvaccinated_reproduction_no_mean",
            "unvaccinated_reproduction_no_prop_variation",
            "peak_transmission_time",
            "generation_time_dist",
            "dispersion_param",
            "vaccination_time_range",
            "proportion_vaccinated",
            "antibody_model_params_pop",
            "susceptibility_func_params",
            "antibody_model_params_random_effects",
            "population_size",
        ]
    }
    kwargs_outbreak_risk_model["rng_seed"] = 2
    outbreak_risk_model = OutbreakRiskModel(**kwargs_outbreak_risk_model)
    df = pd.DataFrame({"time": time_vec})
    df.set_index("time", inplace=True)
    df["r_unvacc"] = outbreak_risk_model.unvaccinated_reproduction_no(time_vec)
    df["r"] = outbreak_risk_model.reproduction_no(time_vec)
    df["susceptibility"] = outbreak_risk_model.susceptibility(time_vec)
    df["cor"] = outbreak_risk_model.case_outbreak_risk(time_vec)
    # Corresponding COR values with no vaccination
    outbreak_risk_model_unvacc = OutbreakRiskModel(
        **{**kwargs_outbreak_risk_model, "proportion_vaccinated": 0}
    )
    df["cor_unvacc"] = outbreak_risk_model_unvacc.case_outbreak_risk(time_vec)
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results"
    results_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(results_dir / "vaccination_example.csv")
    outbreak_risk_model.save_susceptibility_all_0(
        results_dir / "susceptibility_all_0.csv"
    )


if __name__ == "__main__":
    run_analyses()
