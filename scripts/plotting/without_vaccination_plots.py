import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

import matplotlib.pyplot as plt
import pandas as pd

from scripts.plotting import plotting_setup


def make_plots():
    results_dir = pathlib.Path(__file__).parents[2] / "results"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/without_vaccination"
    figure_dir.mkdir(exist_ok=True, parents=True)
    # Load the results
    outbreak_risk_df_methods = pd.read_csv(
        results_dir / "without_vaccination_methods.csv", index_col="time"
    )
    outbreak_risk_df_dispersion = pd.read_csv(
        results_dir / "without_vaccination_dispersion.csv", index_col="time"
    )
    # Plot comparison of COR, IOR, and SOR for a single example with no vaccination
    _, ax = plotting_setup.setup_figure(months_x=True, no_periods=2)
    outbreak_risk_df_methods["R"].plot(ax=ax)
    ax.set_ylim(0, 3.01)
    ax.set_xlabel("")
    ax.set_ylabel("Instantaneous reproduction number")
    plt.savefig(figure_dir / "reproduction_number.pdf")
    plt.savefig(figure_dir / "reproduction_number.svg")
    # Plot comparison of COR, IOR, and SOR for a single example with no vaccination
    _, ax = plotting_setup.setup_figure(months_x=True, no_periods=2)
    outbreak_risk_df_methods["COR"].plot(ax=ax, label="Case outbreak risk")
    outbreak_risk_df_methods["IOR"].plot(
        style="--", ax=ax, label="Instantaneous outbreak risk"
    )
    outbreak_risk_df_methods["SOR"].plot(
        style="yo", ax=ax, label="Simulated outbreak risk"
    )
    ax.set_ylim(0, 1)
    ax.set_xlabel("")
    ax.set_ylabel("Outbreak risk")
    ax.legend()
    plt.savefig(figure_dir / "outbreak_risk_methods.pdf")
    plt.savefig(figure_dir / "outbreak_risk_methods.svg")
    # Plot comparison of COR values for different values of the dispersion parameter
    _, ax = plotting_setup.setup_figure(months_x=True, no_periods=2)
    for dispersion_param in outbreak_risk_df_dispersion.columns:
        outbreak_risk_df_dispersion[dispersion_param].plot(
            label="$\\it{k}$ = " + dispersion_param
        )
    ax.set_ylim(0, 1)
    ax.set_xlabel("")
    ax.set_ylabel("Outbreak risk")
    ax.legend()
    plt.savefig(figure_dir / "outbreak_risk_dispersion.pdf")
    plt.savefig(figure_dir / "outbreak_risk_dispersion.svg")
    # Show plots
    plt.show()


if __name__ == "__main__":
    make_plots()
