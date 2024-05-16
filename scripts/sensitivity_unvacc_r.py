import itertools
import pathlib
import sys

# import snakemake

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination

unvacc_rep_no_mean_vals = [2, 2.5, 3]
unvacc_rep_no_prop_var_vals = [0.1, 0.2, 0.3]


def run_analyses(mean_index, prop_var_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_unvacc_r"
    results_dir.mkdir(exist_ok=True, parents=True)
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    save_path = results_dir / f"grid_search_{mean_index}_{prop_var_index}.csv"
    save_path_best = results_dir / f"best_{mean_index}_{prop_var_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{mean_index}_{prop_var_index}.csv"
    )
    optimizing_vaccination.run_analyses(
        save_path=save_path,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_mean=unvacc_rep_no_mean_vals[mean_index],
        unvaccinated_reproduction_no_prop_variation=unvacc_rep_no_prop_var_vals[
            prop_var_index
        ],
    )


if __name__ == "__main__":
    if "snakemake" in globals() and "mean_index" in snakemake.wildcards:  # noqa: F821
        run_analyses(
            mean_index=int(snakemake.wildcards["mean_index"]),  # noqa: F821
            prop_var_index=int(snakemake.wildcards["prop_var_index"]),  # noqa: F821
        )
    else:
        for _mean_index, _prop_var_index in itertools.product(
            range(len(unvacc_rep_no_mean_vals)), range(len(unvacc_rep_no_prop_var_vals))
        ):
            run_analyses(mean_index=_mean_index, prop_var_index=_prop_var_index)
