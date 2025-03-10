import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

DEFAULTS = {
    "panel_sz": (340, 320),
    "panel_offset": (-25, -60),
    "label_offset": (5, 20),
    "label_size": 20,
}


def make_figure(
    save_path,
    panel_paths,
    template_path=None,
    sz=None,
    tiling=None,
    panel_sz=None,
    panel_offset=None,
    panel_positions=None,
    panel_scalings=None,
    label_strings=None,
    label_size=None,
    label_offset=None,
    label_positions=None,
):
    no_panels = len(panel_paths)
    if tiling is None:
        rows = 1 + (no_panels - 1) // 3
        cols = ceil(no_panels // rows)
    else:
        cols, rows = tiling
    if panel_sz is None:
        panel_sz = DEFAULTS["panel_sz"]
    if sz is None:
        sz = (panel_sz[0] * cols, panel_sz[1] * rows)
    if panel_offset is None:
        panel_offset = DEFAULTS["panel_offset"]
    if panel_positions is None:
        panel_positions = [
            (
                panel_offset[0] + panel_sz[0] * (i % cols),
                panel_offset[1] + panel_sz[1] * (i // cols),
            )
            for i in range(no_panels)
        ]
    if panel_scalings is None:
        panel_scalings = [1] * no_panels
    if label_strings is None:
        label_strings = [chr(65 + i) + "." for i in range(no_panels)]
    if label_size is None:
        label_size = DEFAULTS["label_size"]
    if label_offset is None:
        label_offset = DEFAULTS["label_offset"]
    if label_positions is None:
        label_positions = [
            (
                label_offset[0] + panel_sz[0] * (i % cols),
                label_offset[1] + panel_sz[1] * (i // cols),
            )
            for i in range(no_panels)
        ]
    # create new SVG figure
    if template_path is not None:
        fig = svgt.fromfile(template_path)
    else:
        fig = svgt.SVGFigure()
        fig.set_size((str(sz[0]) + "px", str(sz[1]) + "px"))
    # load matpotlib-generated figures
    panels = []
    for path in panel_paths:
        if path is not None:
            panel = svgt.fromfile(path).getroot()
        else:
            panel = svgt.TextElement(0, 0, "")
        panels.append(panel)
    for panel, position, scaling in zip(panels, panel_positions, panel_scalings):
        panel.moveto(position[0], position[1], scale_x=scaling)
    # add text labels
    labels = [
        svgt.TextElement(position[0], position[1], string, size=label_size)
        for string, position in zip(label_strings, label_positions)
    ]
    # append plots and labels to figure
    fig.append(panels + labels)
    # save generated SVG files
    save_path.mkdir(exist_ok=True, parents=True)
    fig.save(save_path)


def set_sns_theme():
    rc_params = {
        "figure.figsize": (6, 6),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.autolimit_mode": "round_numbers",
        "savefig.transparent": True,
        "savefig.format": "svg",
        "svg.fonttype": "none",
        "axes.titlesize": 16,
        "axes.labelsize": 16,
        "lines.linewidth": 2,
        "lines.markersize": 8,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "legend.fontsize": 14,
    }
    sns.set_theme(style="ticks", palette="colorblind", rc=rc_params)


def setup_figure():
    fig = plt.figure()
    ax = fig.add_axes([0.2, 0.2, 0.6, 0.6])
    return fig, ax


def setup_figure_subplots():
    fig = plt.figure()
    ax1 = fig.add_axes([0.2, 0.53, 0.6, 0.27])
    ax2 = fig.add_axes([0.2, 0.2, 0.6, 0.27])
    return fig, ax1, ax2


def setup_figure_with_cbar():
    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.2, 0.6, 0.6])
    cbar_ax = fig.add_axes([0.78, 0.2, 0.03, 0.6])
    return fig, ax, cbar_ax


def months_x_axis(ax, period=365, no_periods=2):
    if period == 365:
        month_starts = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30])
    elif period == 360:
        month_starts = np.arange(0, period, period // 12)
    else:
        raise NotImplementedError("Only periods of 365 or 360 are currently supported.")
    month_list = ["Jan", "", "", "Apr", "", "", "Jul", "", "", "Oct", "", ""]
    ax.set_xlim(0, no_periods * period)
    ax.set_xticks(
        (month_starts[:, np.newaxis].T + period * np.arange(no_periods)[:, np.newaxis])
        .flatten()
        .tolist()
        + [period * no_periods],
        labels=month_list * no_periods + ["Jan"],
    )
    ax.set_xlabel(" ")


def shade_vaccination_time_range(ax, vaccination_time_range, period=365, no_periods=2):
    if vaccination_time_range[1] > period:
        vaccination_time_range[0] -= period
        vaccination_time_range[1] -= period
    if vaccination_time_range[0] < 0:
        no_periods += 1
    if vaccination_time_range[0] >= vaccination_time_range[1]:
        raise ValueError("Attempting to shade empty time range.")
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
