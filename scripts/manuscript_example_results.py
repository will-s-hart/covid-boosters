import pathlib
import sys
from datetime import timedelta

import cftime
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts.default_parameters import get_default_parameters


def day_to_date(day):
    period = get_default_parameters()["period"]
    if period == 365:
        day_0_date = cftime.DatetimeNoLeap(2024, 1, 1)
    elif period == 360:
        day_0_date = cftime.Datetime360Day(2024, 1, 1)
    else:
        raise NotImplementedError("Only periods of 365 or 360 are currently supported.")
    return (day_0_date + timedelta(days=int(day))).strftime("%d %B")


# Get maximum vaccine protection against infection
df_wh = pd.read_csv(
    pathlib.Path(__file__).parents[1] / "results/within_host_dynamics.csv",
    index_col="time",
)
max_protection_percent = 100 * (1 - df_wh["susceptibility_mean"].min())
print(f"Maximum vaccine protection against infection: {max_protection_percent:.0f}%")

# Get COR values with no vaccination, default vaccination, and optimized vaccination
df_default = pd.read_csv(
    pathlib.Path(__file__).parents[1] / "results/vaccination_example.csv",
    index_col="time",
)
df_best = pd.read_csv(
    pathlib.Path(__file__).parents[1] / "results/optimizing_vaccination/best.csv",
    index_col="time",
)
df_cor_unvacc = df_default["cor_unvacc"]
df_cor_default = df_default["cor"]
df_cor_best = df_best["cor"]

# Get default and optimized vaccination time ranges
vaccination_time_range_default = get_default_parameters()["vaccination_time_range"]
df_vaccination_time_range_best = pd.read_csv(
    pathlib.Path(__file__).parents[1]
    / "results/optimizing_vaccination/vaccination_time_range_best.csv"
)
vaccination_time_range_best = [
    df_vaccination_time_range_best["start"][0],
    df_vaccination_time_range_best["end"][0],
]

# Dates of default and optimised vaccine time ranges (note that the input end day is
# exclusive)
print(
    "Default vaccination time range:",
    day_to_date(vaccination_time_range_default[0]),
    "to",
    day_to_date(vaccination_time_range_default[1] - 1),
)
print(
    "Optimized vaccination time range:",
    day_to_date(vaccination_time_range_best[0]),
    "to",
    day_to_date(vaccination_time_range_best[1] - 1),
)

# Values and dates of maximum annual COR
day_max_unvacc = df_cor_unvacc.idxmax()
day_max_default = df_cor_default.idxmax()
day_max_best = df_cor_best.idxmax()
print(
    "Maximum annual COR with no vaccination:",
    f"{df_cor_unvacc[day_max_unvacc]:.2f}",
    "on",
    day_to_date(day_max_unvacc),
)
print(
    "Maximum annual COR with default vaccination:",
    f"{df_cor_default[day_max_default]:.2f}",
    "on",
    day_to_date(day_max_default),
)
print(
    "Maximum annual COR with optimized vaccination:",
    f"{df_cor_best[day_max_best]:.2f}",
    "on",
    day_to_date(day_max_best),
)

# Unvaccinated COR on date of maximum annual COR with basline vaccination
print(
    "COR with no vaccination on",
    day_to_date(day_max_default),
    "(date of max COR under default vaccination):",
    f"{df_cor_unvacc[day_max_default]:.2f}",
)

# Check that dispersion parameter and mean transmissibility do not affect the optimal
# vaccination time range
for ext in [
    "sensitivity_k/vaccination_time_range_best_0.csv",
    "sensitivity_r0_mean/vaccination_time_range_best_1.csv",
    "sensitivity_k/vaccination_time_range_best_0.csv",
    "sensitivity_r0_mean/vaccination_time_range_best_1.csv",
]:
    df_vaccination_time_range_best_curr = pd.read_csv(
        pathlib.Path(__file__).parents[1] / "results" / ext
    )
    vaccination_time_range_best_curr = [
        df_vaccination_time_range_best["start"][0],
        df_vaccination_time_range_best["end"][0],
    ]
    assert vaccination_time_range_best_curr == vaccination_time_range_best, (
        "Optimal vaccination time range is affected by changes in the dispersion "
        "parameter or mean transmissibility."
    )
print(
    "Optimal vaccination time range is not affected by changes in the dispersion "
    "parameter or mean transmissibility."
)
