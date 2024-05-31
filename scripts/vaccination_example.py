import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from covidboosters import OutbreakRiskModel
from scripts.default_parameters import get_default_parameters


def run_analyses(
    save_path=None,
    save_path_susceptibility_all_0=None,
    load_path_susceptibility_all_0=None,
    **kwargs_outbreak_risk_model,
):
    default_parameters = get_default_parameters()
    kwargs_outbreak_risk_model_in = kwargs_outbreak_risk_model
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
    kwargs_outbreak_risk_model.update(kwargs_outbreak_risk_model_in)
    period = kwargs_outbreak_risk_model["period"]
    time_vec = np.arange(2 * period)
    # Example of COR and IOR with vaccination
    outbreak_risk_model = OutbreakRiskModel(**kwargs_outbreak_risk_model)
    if load_path_susceptibility_all_0 is not None:
        outbreak_risk_model.load_susceptibility_all_0(load_path_susceptibility_all_0)
    df = pd.DataFrame({"time": time_vec})
    df.set_index("time", inplace=True)
    df["r_unvacc"] = outbreak_risk_model.unvaccinated_reproduction_no(time_vec)
    df["r"] = outbreak_risk_model.reproduction_no(time_vec)
    df["susceptibility"] = outbreak_risk_model.susceptibility(time_vec)
    df["cor"] = outbreak_risk_model.case_outbreak_risk(time_vec)
    df["ior"] = outbreak_risk_model.instantaneous_outbreak_risk(time_vec)
    # Corresponding COR values with no vaccination
    outbreak_risk_model_unvacc = OutbreakRiskModel(
        **{**kwargs_outbreak_risk_model, "proportion_vaccinated": 0}
    )
    df["cor_unvacc"] = outbreak_risk_model_unvacc.case_outbreak_risk(time_vec)
    df["ior_unvacc"] = outbreak_risk_model_unvacc.instantaneous_outbreak_risk(time_vec)
    # Save the results
    if save_path is not None:
        df.to_csv(save_path)
    if save_path_susceptibility_all_0 is not None:
        outbreak_risk_model.save_susceptibility_all_0(save_path_susceptibility_all_0)
    return df


if __name__ == "__main__":
    results_dir = pathlib.Path(__file__).parents[1] / "results"
    results_dir.mkdir(exist_ok=True, parents=True)
    run_analyses(
        save_path=results_dir / "vaccination_example.csv",
        load_path_susceptibility_all_0=results_dir / "susceptibility_all_0.csv",
    )
