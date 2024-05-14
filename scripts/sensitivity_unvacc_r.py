import pathlib
import sys

# import snakemake

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination

unvacc_rep_no_mean_vals = [2, 2.5, 3]
unvacc_rep_no_prop_var_vals = [0.1, 0.2, 0.3]

unvacc_rep_no_mean = unvacc_rep_no_mean_vals[
    int(snakemake.wildcards["mean_index"])  # noqa: F821
]
unvacc_rep_no_prop_var = unvacc_rep_no_prop_var_vals[
    int(snakemake.wildcards["prop_var_index"])  # noqa: F821
]
save_path = snakemake.output[0]  # noqa: F821
save_path_best = snakemake.output[1]  # noqa: F821
save_path_vaccination_time_range_best = snakemake.output[2]  # noqa: F821

results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_unvacc_r"
results_dir.mkdir(exist_ok=True, parents=True)

optimizing_vaccination.run_analyses(
    save_path=save_path,
    save_path_best=save_path_best,
    save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
    load_path_susceptibility_all_0=pathlib.Path(__file__).parents[1]
    / "results/susceptibility_all_0.csv",
    unvaccinated_reproduction_no_mean=unvacc_rep_no_mean,
    unvaccinated_reproduction_no_prop_variation=unvacc_rep_no_prop_var,
)
