import pathlib
from math import ceil

import cairosvg
import svgutils.transform as svgt

FIGURE_DIR = pathlib.Path(__file__).parents[2] / "figures/paper_figures"

DEFAULTS = {
    "panel_sz": (340, 320),
    "panel_offset": (-25, -60),
    "label_offset": (5, 20),
}


def make_figure(
    save_path,
    panel_paths,
    tiling=None,
    panel_sz=None,
    sz=None,
    panel_positions=None,
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
    if panel_positions is None:
        panel_offset = DEFAULTS["panel_offset"]
        panel_positions = [
            (
                panel_offset[0] + panel_sz[0] * (i % cols),
                panel_offset[1] + panel_sz[1] * (i // cols),
            )
            for i in range(no_panels)
        ]
    if label_positions is None:
        label_offset = DEFAULTS["label_offset"]
        label_positions = [
            (
                label_offset[0] + panel_sz[0] * (i % cols),
                label_offset[1] + panel_sz[1] * (i // cols),
            )
            for i in range(no_panels)
        ]
    # create new SVG figure
    fig = svgt.SVGFigure()
    fig.set_size((str(sz[0]) + "px", str(sz[1]) + "px"))
    # load matpotlib-generated figures
    panels = [svgt.fromfile(path).getroot() for path in panel_paths]
    for panel, position in zip(panels, panel_positions):
        panel.moveto(position[0], position[1])
    # add text labels
    labels = [
        svgt.TextElement(position[0], position[1], chr(65 + i) + ".", size=20)
        for i, position in enumerate(label_positions)
    ]
    # append plots and labels to figure
    fig.append(panels + labels)
    # save generated SVG files
    fig.save(save_path)


def make_fig1():
    save_path = FIGURE_DIR / "fig1.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/without_vaccination"
    panel_paths = [
        panel_dir / "reproduction_number.svg",
        panel_dir / "outbreak_risk.svg",
    ]
    make_figure(save_path, panel_paths)


def make_fig2():
    save_path = FIGURE_DIR / "fig2.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/within_host_dynamics"
    panel_paths = [
        panel_dir / "antibodies.svg",
        panel_dir / "susceptibility.svg",
    ]
    panel_sz = (340, 335)
    make_figure(save_path, panel_paths, panel_sz=panel_sz)


def make_fig3():
    save_path = FIGURE_DIR / "fig3.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/vaccination_example"
    panel_paths = [
        panel_dir / "susceptibility.svg",
        panel_dir / "reproduction_number.svg",
        panel_dir / "outbreak_risk.svg",
    ]
    make_figure(save_path, panel_paths)


def make_fig4():
    save_path = FIGURE_DIR / "fig4.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/optimizing_vaccination"
    panel_paths = [
        panel_dir / "heatmap.svg",
        panel_dir / "best.svg",
    ]
    panel_sz = (410, 335)
    sz = (panel_sz[0] + DEFAULTS["panel_sz"][0], panel_sz[1])
    panel_offset_default = DEFAULTS["panel_offset"]
    panel_positions = [
        (0, panel_offset_default[1]),
        (panel_offset_default[0] + panel_sz[0], panel_offset_default[1]),
    ]
    make_figure(
        save_path,
        panel_paths,
        panel_sz=panel_sz,
        sz=sz,
        panel_positions=panel_positions,
    )


def make_fig5():
    save_path = FIGURE_DIR / "fig5.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures"
    panel_paths = [
        panel_dir / "sensitivity_k/default.svg",
        panel_dir / "sensitivity_k/best_0.svg",
        panel_dir / "sensitivity_k/best_1.svg",
        panel_dir / "sensitivity_prop_vacc/default.svg",
        panel_dir / "sensitivity_prop_vacc/best_0.svg",
        panel_dir / "sensitivity_prop_vacc/best_1.svg",
    ]
    make_figure(save_path, panel_paths)


if __name__ == "__main__":
    FIGURE_DIR.mkdir(exist_ok=True, parents=True)
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()
