import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import make_figure

save_path = pathlib.Path(__file__).parents[2] / "figures/paper_figures/figure_1.svg"
panel_dir = pathlib.Path(__file__).parents[2] / "figures"
panel_paths = [
    panel_dir / "without_vaccination/reproduction_number.svg",
    panel_dir / "superspreading/infectiousness_factors.svg",
    panel_dir / "model_input/generation_time.svg",
    "figures/simulation_examples/simulations.svg",
    None,
    panel_dir / "without_vaccination/outbreak_risk.svg",
]
template_path = (
    pathlib.Path(__file__).parents[2] / "figures/templates/fig1_template.svg"
)
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
