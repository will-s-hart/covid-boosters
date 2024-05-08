from pathlib import Path

import numpy as np
import pandas as pd

data_dir = Path(__file__).parents[1] / "data"
results_dir = Path(__file__).parents[1] / "results"
results_dir.mkdir(exist_ok=True, parents=True)

df_hcw = pd.read_csv(data_dir / "12HCWs_NLMEM_parameters.csv", index_col=0)
df_cohort = pd.read_csv(
    data_dir / "1618_FukushimaVaccineCohorts_NLSM_parameters.csv", index_col=0
)

df_params_individual = pd.DataFrame(
    {
        "mrna_dose": 100,
        "mrna_decay_rate": np.log(2),
        "delay_to_antibody_response": df_hcw["eta_3"]["Fix effects"],
        "max_antibody_production_rate": df_cohort["M_b"],
        "mrna_response_steepness": df_cohort["m_b"],
        "half_maximal_response_mrna": df_hcw["K"]["Fix effects"],
        "antibody_decay_rate": df_hcw["mu"]["Fix effects"],
    }
)

df_params_individual_log = np.log(df_params_individual)
df_params_pop = np.exp(df_params_individual_log.mean())
df_params_random_effects = df_params_individual_log.std()

df_params_pop.to_csv(results_dir / "antibody_model_params_pop.csv")
df_params_random_effects.to_csv(
    results_dir / "antibody_model_params_random_effects.csv"
)
