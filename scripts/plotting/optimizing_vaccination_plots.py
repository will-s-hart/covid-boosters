import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import interpolate

from scripts.default_parameters import get_default_parameters
from scripts.plotting import plotting_utils


def make_plots(
    load_path,
    load_path_best,
    load_path_vaccination_time_range_best,
    figure_path_heatmap,
    figure_path_best,
):
    plotting_utils.set_sns_theme()
    # Load the results
    df_grid_search = pd.read_csv(load_path, index_col=0).rename_axis("duration", axis=1)
    df_best = pd.read_csv(load_path_best, index_col="time")
    df_vaccination_time_range_best = pd.read_csv(load_path_vaccination_time_range_best)
    vaccination_time_range_best = [
        df_vaccination_time_range_best["start"][0],
        df_vaccination_time_range_best["end"][0],
    ]
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    # Plot heatmap of max COR for different vaccination start times and durations
    make_heatmap_plot(df_grid_search, vaccination_time_range_best, period=period)
    plt.savefig(figure_path_heatmap)
    plt.savefig(str(figure_path_heatmap).replace(".svg", ".pdf"))
    # Plot COR with and without vaccination
    _, ax = plotting_utils.setup_figure()
    df_best["cor_unvacc"].plot(ax=ax, label="Without vaccination")
    df_best["cor"].plot(ax=ax, label="With vaccination")
    plotting_utils.months_x_axis(ax, period=period, no_periods=2)
    ax.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(ax, vaccination_time_range_best)
    ax.set_ylabel("Case outbreak risk")
    ax.legend()
    plt.savefig(figure_path_best)
    plt.savefig(str(figure_path_best).replace(".svg", ".pdf"))
    # Show plots
    plt.show()


def make_heatmap_plot(df_grid_search, vaccination_time_range_best, period=360):
    if period != 360:
        raise NotImplementedError("Only period=360 is currently supported.")
    _, ax, cbar_ax = plotting_utils.setup_figure_with_cbar()
    sns.heatmap(
        df_grid_search.transpose(),
        ax=ax,
        cbar_ax=cbar_ax,
        rasterized=True,
        cmap="viridis",
        cbar_kws={"label": "Maximum case outbreak risk"},
    )
    ax.invert_yaxis()
    xticks = ax.get_xticks()
    xtick_labels = [int(x.get_text()) for x in ax.get_xticklabels()]
    xtick_label_inv = interpolate.interp1d(
        xtick_labels, xticks, fill_value="extrapolate"
    )
    yticks = ax.get_yticks()
    ytick_labels = [int(y.get_text()) for y in ax.get_yticklabels()]
    ytick_label_inv = interpolate.interp1d(
        ytick_labels, yticks, fill_value="extrapolate"
    )
    start_best = vaccination_time_range_best[0]
    duration_best = vaccination_time_range_best[1] - vaccination_time_range_best[0]
    ax.plot(
        xtick_label_inv(start_best),
        ytick_label_inv(duration_best),
        "wo",
    )
    month_starts = np.arange(0, period + 1, period // 12)
    month_list = ["Jan", "", "", "Apr", "", "", "Jul", "", "", "Oct", "", "", "Jan"]
    ax.set_xticks(xtick_label_inv(month_starts), labels=month_list, rotation=0)
    ax.set_yticks(ytick_label_inv(month_starts[1:]), labels=month_starts[1:])
    ax.set_xlabel("Start of campaign")
    ax.set_ylabel("Duration of campaign (days)")


if __name__ == "__main__":
    results_dir = pathlib.Path(__file__).parents[2] / "results/optimizing_vaccination"
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/optimizing_vaccination"
    figure_dir.mkdir(exist_ok=True, parents=True)
    make_plots(
        load_path=results_dir / "grid_search.csv",
        load_path_best=results_dir / "best.csv",
        load_path_vaccination_time_range_best=results_dir
        / "vaccination_time_range_best.csv",
        figure_path_heatmap=figure_dir / "heatmap.svg",
        figure_path_best=figure_dir / "best.svg",
    )
