"""Utility functions for plotting."""

from math import ceil

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import svgutils.transform as svgt

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
    """
    Create a figure from a set of panels.

    Parameters
    ----------
    save_path : pathlib.Path
        Path to save the figure.
    panel_paths : list of pathlib.Path
        Paths to the panels to include in the figure.
    template_path : pathlib.Path, optional
        Path to an SVG template file onto which the panels will be placed. If None, no
        template is used.
    sz : tuple of int, optional
        Size of the figure in pixels (width, height). If None, the size is calculated
        based on the number of panels and the panel size.
    tiling : tuple of int, optional
        Number of rows and columns to tile the panels in the figure. If None, the
        number of rows and columns is calculated automatically.
    panel_sz : tuple of int, optional
        Size of the panels in pixels (width, height). If note provided, the default
        value in plotting_utils.DEFAULTS is used.
    panel_offset : tuple of int, optional
        Offset of the panels from the top-left corner of the figure in pixels (x, y).
        If not provided, the default value in plotting_utils.DEFAULTS is used.
    panel_positions : list of tuple of int, optional
        Positions of the panels in the figure in pixels (x, y). Overrides other settings
        determining panel positions if provided.
    panel_scalings : list of float, optional
        Scaling factors for the panels. If not provided, the panels are not scaled.
    label_strings : list of str, optional
        Strings to use as labels for the panels. If not provided, labels are generated
        automatically as A., B., C., etc.
    label_size : int, optional
        Font size of the labels. If not provided, the default value in
        plotting_utils.DEFAULTS is used.
    label_offset : tuple of int, optional
        Offset of the labels from the top-left corner of the figure in pixels (x, y).
        If not provided, the default value in plotting_utils.DEFAULTS is used.
    label_positions : list of tuple of int, optional
        Positions of the labels in the figure in pixels (x, y). Overrides other settings
        determining label positions if provided.

    Returns
    -------
    None
    """
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
        svgt.TextElement(
            position[0], position[1], string, size=label_size, font="Arial"
        )
        for string, position in zip(label_strings, label_positions)
    ]
    # append plots and labels to figure
    fig.append(panels + labels)
    # save generated SVG files
    save_path.parent.mkdir(exist_ok=True, parents=True)
    fig.save(save_path)


def set_sns_theme():
    """
    Configure the Seaborn theme for plotting.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
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
        "font.family": "sans-serif",
        "font.sans-serif": "Arial",
    }
    sns.set_theme(style="ticks", palette="colorblind", rc=rc_params)


def setup_figure():
    """
    Set up a figure with a single set of axes.

    Parameters
    ----------
    None

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    ax : matplotlib.axes.Axes
        Axes object.
    """
    fig = plt.figure()
    ax = fig.add_axes([0.2, 0.2, 0.6, 0.6])
    return fig, ax


def setup_figure_subplots():
    """
    Set up a figure with two sets of axes, arranged vertically.

    Parameters
    ----------
    None

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    ax1 : matplotlib.axes.Axes
        First axes object.
    ax2 : matplotlib.axes.Axes
        Second axes object.
    """
    fig = plt.figure()
    ax1 = fig.add_axes([0.2, 0.53, 0.6, 0.27])
    ax2 = fig.add_axes([0.2, 0.2, 0.6, 0.27])
    return fig, ax1, ax2


def setup_figure_with_cbar():
    """
    Set up a figure with a main set of axes and a colorbar axis.

    Parameters
    ----------
    None

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    ax : matplotlib.axes.Axes
        Axes object.
    cbar_ax : matplotlib.axes.Axes
        Colorbar axis object.
    """
    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.2, 0.6, 0.6])
    cbar_ax = fig.add_axes([0.78, 0.2, 0.03, 0.6])
    return fig, ax, cbar_ax


def months_x_axis(ax, period=365, no_periods=2):
    """
    Set the x-axis of a plot to show month names as tick labels.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes on which to set the x-axis.
    period : int, optional
        Length of calendar year in days (365 or 360). Note leap years are not supported
        for simplicity to ensure periodicity.
    no_periods : int, optional
        Number of years for which to set x-axis tick labels.

    Returns
    -------
    None
    """
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
    """
    Shade the time range during which vaccination is ongoing.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes on which to shade the time range.
    vaccination_time_range : list of int
        Start and end times of the vaccination time range each period.
    period : int, optional
        Period between start times of vaccination campaigns.
    no_periods : int, optional
        Number of periods for which to shade the time range.

    Returns
    -------
    None
    """
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
