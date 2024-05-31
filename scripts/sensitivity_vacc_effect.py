import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

from scripts import optimizing_vaccination, vaccination_example, within_host_dynamics
from scripts.default_parameters import get_default_parameters

half_protection_antibody_vals = [500, 2000]


def run_analyses(half_protection_antibody_index):
    results_dir = pathlib.Path(__file__).parents[1] / "results/sensitivity_vacc_effect"
    results_dir.mkdir(exist_ok=True, parents=True)
    save_path_within_host = (
        results_dir / f"within_host_{half_protection_antibody_index}.csv"
    )
    save_path_default = results_dir / f"default_{half_protection_antibody_index}.csv"
    save_path_grid_search = (
        results_dir / f"grid_search_{half_protection_antibody_index}.csv"
    )
    save_path_best = results_dir / f"best_{half_protection_antibody_index}.csv"
    save_path_vaccination_time_range_best = (
        results_dir
        / f"vaccination_time_range_best_{half_protection_antibody_index}.csv"
    )
    save_path_susceptibility_all_0 = (
        results_dir / f"susceptibility_all_0_{half_protection_antibody_index}.csv"
    )
    susceptibility_func_params = {
        **get_default_parameters()["susceptibility_func_params"],
        "half_protection_antibody": half_protection_antibody_vals[
            half_protection_antibody_index
        ],
    }
    within_host_dynamics.run_analyses(
        save_path=save_path_within_host,
        susceptibility_func_params=susceptibility_func_params,
        save_path_susceptibility_all_0=save_path_susceptibility_all_0,
    )
    vaccination_example.run_analyses(
        save_path=save_path_default,
        load_path_susceptibility_all_0=save_path_susceptibility_all_0,
        susceptibility_func_params=susceptibility_func_params,
    )
    optimizing_vaccination.run_analyses(
        save_path=save_path_grid_search,
        save_path_best=save_path_best,
        save_path_vaccination_time_range_best=save_path_vaccination_time_range_best,
        load_path_susceptibility_all_0=save_path_susceptibility_all_0,
        susceptibility_func_params=susceptibility_func_params,
    )


if __name__ == "__main__":
    if "snakemake" in globals():
        run_analyses(
            half_protection_antibody_index=int(
                snakemake.wildcards["index"]  # noqa: F821
            ),
        )
    else:
        for _half_protection_antibody_index in range(
            len(half_protection_antibody_vals)
        ):
            run_analyses(half_protection_antibody_index=_half_protection_antibody_index)
