import itertools
import pathlib
import sys

# import snakemake

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination

prop_vacc_vals = [0.25, 0.5, 0.75]


def run_analyses(prop_vacc_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_prop_vacc"
    results_dir.mkdir(exist_ok=True, parents=True)
    load_path_susceptibility_all_0 = (
        pathlib.Path(__file__).parents[1] / "results/susceptibility_all_0.csv"
    )
    save_path = results_dir / f"grid_search_{prop_vacc_index}.csv"
    save_path_best = results_dir / f"best_{prop_vacc_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir / f"vaccination_time_range_best_{prop_vacc_index}.csv"
    )
    optimizing_vaccination.run_analyses(
        save_path=save_path,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=load_path_susceptibility_all_0,
        proportion_vaccinated=prop_vacc_vals[prop_vacc_index],
    )


if __name__ == "__main__":
    if "snakemake" in globals() and "mean_index" in snakemake.wildcards:  # noqa: F821
        run_analyses(
            prop_vacc_index=int(snakemake.wildcards["prop_vacc_index"]),  # noqa: F821
        )
    else:
        for _prop_vacc_index in range(len(prop_vacc_vals)):
            run_analyses(prop_vacc_index=_prop_vacc_index)
