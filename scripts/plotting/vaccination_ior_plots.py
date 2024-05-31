import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/vaccination_ior"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    df = pd.read_csv(results_dir / "vaccination_example.csv", index_col="time")
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    vaccination_time_range = default_parameters["vaccination_time_range"]
    # Plot COR and IOR with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df["cor_unvacc"].plot(ax=ax, label="", color="tab:blue", alpha=0.5)
    df["cor"].plot(ax=ax, label="Case outbreak risk", color="tab:blue")
    df["ior_unvacc"].plot(
        ax=ax, label="", color="tab:orange", linestyle="--", alpha=0.5
    )
    df["ior"].plot(
        ax=ax, label="Instantaneous outbreak risk", color="tab:orange", linestyle="--"
    )
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range)
    ax.set_ylabel("Outbreak risk")
    ax.legend()
    plt.savefig(figure_dir / "outbreak_risk.pdf")
    plt.savefig(figure_dir / "outbreak_risk.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
