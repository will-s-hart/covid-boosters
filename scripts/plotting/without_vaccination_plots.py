import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

import matplotlib.pyplot as plt
import pandas as pd

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    results_dir = pathlib.Path(__file__).parents[2] / "results/without_vaccination"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/without_vaccination"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    outbreak_risk_df_methods = pd.read_csv(
        results_dir / "methods.csv", index_col="time"
    )
    outbreak_risk_df_dispersion = pd.read_csv(
        results_dir / "dispersion.csv", index_col="time"
    )
    period = get_default_parameters()["period"]
    # Plot instantaneous reproduction number
    _, ax = plotting_utils.setup_figure()
    outbreak_risk_df_methods["r"].plot(ax=ax)
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 3.01)
    ax.set_ylabel("Instantaneous reproduction number")
    plt.savefig(figure_dir / "reproduction_number.pdf")
    plt.savefig(figure_dir / "reproduction_number.svg")
    # Plot comparison of COR, IOR, and SOR for a single example with no vaccination
    _, ax = plotting_utils.setup_figure()
    outbreak_risk_df_methods["cor"].plot(ax=ax, label="Case outbreak risk")
    outbreak_risk_df_methods["ior"].plot(
        style="--", ax=ax, label="Instantaneous outbreak risk"
    )
    outbreak_risk_df_methods["sor"].plot(
        style="yo", ax=ax, label="Simulated outbreak risk"
    )
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Outbreak risk")
    ax.legend()
    plt.savefig(figure_dir / "outbreak_risk_methods.pdf")
    plt.savefig(figure_dir / "outbreak_risk_methods.svg")
    # Plot comparison of COR values for different values of the dispersion parameter
    _, ax = plotting_utils.setup_figure()
    for dispersion_param in outbreak_risk_df_dispersion.columns:
        outbreak_risk_df_dispersion[dispersion_param].plot(
            label="$\\it{k}$ = " + dispersion_param
        )
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Outbreak risk")
    ax.legend()
    plt.savefig(figure_dir / "outbreak_risk_dispersion.pdf")
    plt.savefig(figure_dir / "outbreak_risk_dispersion.svg")
    # Show plots
    plt.show()


if __name__ == "__main__":
    make_plots()
