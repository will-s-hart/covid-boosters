import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def set_sns_theme():
    rc_params = {
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.autolayout": True,
        "axes.autolimit_mode": "round_numbers",
        "savefig.transparent": True,
        "savefig.format": "pdf",
        "svg.fonttype": "none",
        "axes.titlesize": 16,
        "axes.labelsize": 16,
        "lines.linewidth": 2,
        "lines.markersize": 8,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "legend.fontsize": 14,
    }
    sns.set_theme(style="ticks", rc=rc_params)


def setup_figure():
    fig = plt.figure()
    ax = fig.add_subplot(box_aspect=1)
    return fig, ax


def months_x_axis(ax, period=360, no_periods=2):
    if period != 360:
        raise NotImplementedError("Only period=360 is currently supported.")
    month_starts = np.arange(0, period + 1, period / 12)
    month_list = ["Jan", "", "", "Apr", "", "", "Jul", "", "", "Oct", "", "", "Jan"]
    ax.set_xlim(0, no_periods * period)
    ax.set_xticks(
        (
            month_starts[:, np.newaxis].T
            + period * np.arange(no_periods)[:, np.newaxis]
        ).flatten(),
        labels=month_list * no_periods,
    )
    ax.set_xlabel("")


def shade_vaccination_time_range(ax, vaccination_time_range, period=360, no_periods=2):
    if (
        vaccination_time_range[0] >= vaccination_time_range[1]
        or vaccination_time_range[0] < 0
        or vaccination_time_range[1] > period
    ):
        raise NotImplementedError(
            "Only vaccination time ranges not including year ends are currently "
            "supported."
        )
    ylim = ax.get_ylim()
    for i in range(no_periods):
        ax.fill_betweenx(
            y=ylim,
            x1=period * i + vaccination_time_range[0],
            x2=period * i + vaccination_time_range[1],
            color="gray",
            alpha=0.5,
            linewidth=0,
        )
    ax.set_ylim(ylim)
