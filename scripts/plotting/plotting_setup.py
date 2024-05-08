import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from scripts.default_parameters import get_default_parameters

if get_default_parameters()["period"] != 360:
    raise ValueError(
        "The month start definitions in this script need to be updated"
        "for a non-360-day calendar"
    )
PERIOD = 360
month_starts = np.arange(0, PERIOD + 1, PERIOD / 12)
month_list = ["Jan", "", "", "Apr", "", "", "Jul", "", "", "Oct", "", "", "Jan"]

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


def setup_figure(months_x=False, no_periods=None):
    fig = plt.figure()
    ax = fig.add_subplot(box_aspect=1)
    if months_x:
        if no_periods is None:
            no_periods = 2
        ax.set_xlim(0, no_periods * PERIOD)
        ax.set_xticks(
            (
                month_starts[:, np.newaxis].T
                + PERIOD * np.arange(no_periods)[:, np.newaxis]
            ).flatten(),
            labels=month_list * no_periods,
        )
    return fig, ax
