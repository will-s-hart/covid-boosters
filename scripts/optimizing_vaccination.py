import itertools
import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

import numpy as np
import pandas as pd
import tqdm

from covidboosters import OutbreakRiskModel
from scripts.default_parameters import get_default_parameters


def run_analyses():
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    step = 180
    vaccination_start_time_vals = np.arange(0, period + 1, step)
    vaccination_duration_vals = np.arange(step, period + 1, step)
    # Set up outbreak risk model
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
    outbreak_risk_model.load_susceptibility_all_0(
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    # Loop over vaccination start times and durations
    df_cor_max_vals = (
        pd.DataFrame(
            index=vaccination_start_time_vals,
            columns=vaccination_duration_vals,
            dtype=float,
        )
        .rename_axis("Start of campaign", axis=0)
        .rename_axis("Duration of campaign (days)", axis=1)
    )
    for vaccination_start_time, vaccination_duration in tqdm.tqdm(
        itertools.product(vaccination_start_time_vals, vaccination_duration_vals),
        total=len(vaccination_start_time_vals) * len(vaccination_duration_vals),
    ):
        vaccination_time_range = (
            vaccination_start_time,
            vaccination_start_time + vaccination_duration,
        )
        outbreak_risk_model.update_vaccination_params(
            vaccination_time_range=vaccination_time_range
        )
        cor_max = np.max(outbreak_risk_model.case_outbreak_risk(np.arange(period)))
        df_cor_max_vals.loc[vaccination_start_time, vaccination_duration] = cor_max
    # Determine optimal vaccination start time and duration
    start_time_best, duration_best = df_cor_max_vals.stack().idxmin()
    vaccination_time_range_best = (
        start_time_best,
        start_time_best + duration_best,
    )
    df_vaccination_time_range_best = pd.DataFrame(
        {
            "start": vaccination_time_range_best[0],
            "end": vaccination_time_range_best[1],
        },
        index=[0],
    )

    # COR with optimal and no vaccination
    time_vec = np.arange(2 * period)
    df_best = pd.DataFrame({"time": time_vec})
    df_best.set_index("time", inplace=True)
    outbreak_risk_model.update_vaccination_params(
        vaccination_time_range=vaccination_time_range_best
    )
    df_best["cor"] = outbreak_risk_model.case_outbreak_risk(time_vec)
    outbreak_risk_model_unvacc = OutbreakRiskModel(
        **{**kwargs_outbreak_risk_model, "proportion_vaccinated": 0}
    )
    df_best["cor_unvacc"] = outbreak_risk_model_unvacc.case_outbreak_risk(time_vec)
    # Save the results
    results_dir = pathlib.Path(__file__).parents[1] / "results/optimizing_vaccination"
    results_dir.mkdir(exist_ok=True, parents=True)
    df_cor_max_vals.to_csv(results_dir / "cor_max_vals.csv")
    df_vaccination_time_range_best.to_csv(
        results_dir / "vaccination_time_range_best.csv", index=False
    )
    df_best.to_csv(results_dir / "best.csv")


if __name__ == "__main__":
    run_analyses()
