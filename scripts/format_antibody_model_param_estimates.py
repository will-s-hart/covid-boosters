from pathlib import Path

import numpy as np
import pandas as pd

data_dir = Path(__file__).parents[1] / "data"
results_dir = Path(__file__).parents[1] / "results"
results_dir.mkdir(exist_ok=True, parents=True)

df_hcw = pd.read_csv(data_dir / "12_HCWs_parameters.csv", index_col=0)
df_cohort = pd.read_csv(
    data_dir / "1618_FukushimaVaccineCohort_parameters.csv", index_col=0
)

df_params_individual = pd.DataFrame(
    {
        "mrna_dose": df_hcw["D"]["Fixed effect"],
        "mrna_decay_rate": df_hcw["delta"]["Fixed effect"],
        "delay_to_antibody_response": df_hcw["tau_d"]["Fixed effect"],
        "max_antibody_production_rate": df_cohort["H"],
        "mrna_response_steepness": df_cohort["m"],
        "half_maximal_response_mrna": df_hcw["K"]["Fixed effect"],
        "antibody_decay_rate": df_hcw["mu"]["Fixed effect"],
    }
)

df_params_individual_log = np.log(df_params_individual)
df_params_pop = np.exp(df_params_individual_log.mean())
df_params_random_effects = df_params_individual_log.std()

df_out = pd.concat(
    [df_params_pop, df_params_random_effects],
    axis=1,
)
df_out.columns = ["population_value", "random_effect"]
df_out.index.rename("parameter", inplace=True)

df_out.to_csv(results_dir / "antibody_model_params.csv")
