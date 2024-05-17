import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination

r0_mean_vals = [2, 3]


def run_analyses(r0_mean_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_r0_mean"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path = results_dir / f"grid_search_{r0_mean_index}.csv"
    save_path_best = results_dir / f"best_{r0_mean_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{r0_mean_index}.csv"
    )
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    optimizing_vaccination.run_analyses(
        save_path=save_path,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        unvaccinated_reproduction_no_mean=r0_mean_vals[r0_mean_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            r0_mean_index=int(snakemake.wildcards["r0_mean_index"]),  # noqa: F821
        )
    else:
        for _r0_mean_index in range(len(r0_mean_vals)):
            run_analyses(r0_mean_index=_r0_mean_index)
