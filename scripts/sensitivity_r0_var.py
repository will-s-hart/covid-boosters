import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination, vaccination_example

r0_var_vals = [0.1, 0.3]


def run_analyses(r0_var_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_r0_var"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_default = results_dir / f"default_{r0_var_index}.csv"
    save_path_grid_search = results_dir / f"grid_search_{r0_var_index}.csv"
    save_path_best = results_dir / f"best_{r0_var_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{r0_var_index}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    vaccination_example.run_analyses(
        save_path=save_path_default,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_prop_variation=r0_var_vals[r0_var_index],
    )
    optimizing_vaccination.run_analyses(
        save_path=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_prop_variation=r0_var_vals[r0_var_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            r0_var_index=int(snakemake.wildcards["index"]),  # noqa: F821
        )
    else:
        for _r0_var_index in range(len(r0_var_vals)):
            run_analyses(r0_var_index=_r0_var_index)
