import pathlib
from math import ceil

import svgutils.transform as svgt

FIGURE_DIR = pathlib.Path(__file__).parents[2] / "figures/paper_figures"

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
    fig.save(save_path)


def make_fig1():
    save_path = FIGURE_DIR / "fig1.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures"
    panel_paths = [
        panel_dir / "without_vaccination/reproduction_number.svg",
        panel_dir / "superspreading/infectiousness_factors.svg",
        panel_dir / "model_input/generation_time.svg",
        "figures/simulation_examples/simulations.svg",
        None,
        panel_dir / "without_vaccination/outbreak_risk.svg",
    ]
    template_path = FIGURE_DIR / "templates/fig1_template.svg"
    panel_sz = (340, 364)
    panel_offset = (-15, -45)
    panel_positions = [
        (
            panel_offset[0] + panel_sz[0] * (i % 3),
            panel_offset[1] + panel_sz[1] * (i // 3),
        )
        for i in range(6)
    ]
    panel_positions[3] = (190, 250)
    panel_scalings = [1, 1, 1, 0.85 * 4 / 3, 1, 1]
    label_strings = [
        "A. Time-dependent transmission",
        "B. Heterogeneity in infectiousness",
        "C. Generation time distribution",
        "D. Outbreak risk calculation",
        "",
        "E. Outbreak risk values",
    ]
    label_size = 18
    label_offset = (10, 25)
    make_figure(
        save_path,
        panel_paths,
        template_path=template_path,
        panel_sz=panel_sz,
        panel_positions=panel_positions,
        panel_scalings=panel_scalings,
        label_strings=label_strings,
        label_size=label_size,
        label_offset=label_offset,
    )


def make_fig2():
    save_path = FIGURE_DIR / "fig2.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures"
    panel_paths = [
        panel_dir / "within_host_dynamics/antibodies.svg",
        panel_dir / "within_host_dynamics/susceptibility.svg",
        panel_dir / "vaccination_example/susceptibility.svg",
        panel_dir / "vaccination_example/unvaccinated_reproduction_number.svg",
        panel_dir / "vaccination_example/reproduction_number.svg",
        panel_dir / "vaccination_example/outbreak_risk.svg",
    ]
    panel_sz = (350, 335)
    panel_offset = (-12.5, DEFAULTS["panel_offset"][1])
    make_figure(
        save_path,
        panel_paths,
        panel_sz=panel_sz,
        panel_offset=panel_offset,
    )


def make_fig2_alt():
    save_path = FIGURE_DIR / "fig2_alt.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures"
    panel_paths = [
        panel_dir / "within_host_dynamics/antibodies.svg",
        panel_dir / "within_host_dynamics/susceptibility.svg",
        panel_dir / "vaccination_example/susceptibility.svg",
        panel_dir / "vaccination_example/unvaccinated_reproduction_number.svg",
        panel_dir / "vaccination_example/reproduction_number.svg",
        panel_dir / "vaccination_example/outbreak_risk.svg",
    ]
    template_path = FIGURE_DIR / "templates/fig2_alt_template.svg"
    panel_sz = (360, 340)
    panel_offset = (-12.5, DEFAULTS["panel_offset"][1])
    make_figure(
        save_path,
        panel_paths,
        template_path=template_path,
        panel_sz=panel_sz,
        panel_offset=panel_offset,
    )


def make_fig3():
    save_path = FIGURE_DIR / "fig3.svg"
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


def make_fig4():
    save_path = FIGURE_DIR / "fig4.svg"
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
    make_fig2_alt()
    make_fig3()
    make_fig4()
