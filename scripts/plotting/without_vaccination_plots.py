import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results/without_vaccination"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/without_vaccination"
    figure_dir.mkdir(exist_ok=True, parents=True)
    colors = [sns.color_palette("colorblind")[i] for i in [3, 0, 2, 1, 9]]
    # Load the results
    df_reproduction_number = pd.read_csv(
        results_dir / "reproduction_number.csv", index_col="time"
    )
    df_analytic = pd.read_csv(results_dir / "analytic.csv", index_col="time")
    df_simulated = pd.read_csv(results_dir / "simulated.csv", index_col="time")
    period = get_default_parameters()["period"]
    # Plot instantaneous reproduction number
    _, ax = plotting_utils.setup_figure()
    df_reproduction_number["r"].plot(ax=ax)
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 3.02)
    ax.set_ylabel("Instantaneous reproduction number")
    plt.savefig(figure_dir / "reproduction_number.pdf")
    plt.savefig(figure_dir / "reproduction_number.svg")
    # Plot comparison of COR/SOR values for different values of the dispersion parameter
    _, ax = plotting_utils.setup_figure()
    for dispersion_param, color in zip(df_analytic.columns, colors):
        df_analytic[dispersion_param].plot(
            color=color, label="$\\it{k}$ = " + dispersion_param
        )
        df_simulated[dispersion_param].plot(
            color=color, style="o", markersize=5, alpha=0.5, label=""
        )
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Outbreak risk")
    ax.legend(loc="upper right")
    plt.savefig(figure_dir / "outbreak_risk.pdf")
    plt.savefig(figure_dir / "outbreak_risk.svg")
    # Show plots
    if "snakemake" not in globals():
        plt.show()


if __name__ == "__main__":
    make_plots()
