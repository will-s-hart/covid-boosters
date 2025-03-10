import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import DEFAULTS, make_figure

save_path = pathlib.Path(__file__).parents[2] / "figures/paper_figures/figure_2.svg"
panel_dir = pathlib.Path(__file__).parents[2] / "figures"
panel_paths = [
    panel_dir / "within_host_dynamics/antibodies.svg",
    panel_dir / "within_host_dynamics/susceptibility.svg",
    panel_dir / "vaccination_example/susceptibility_reproduction_number.svg",
    panel_dir / "vaccination_example/outbreak_risk.svg",
]
panel_sz = (350, 330)
panel_offset = (-12.5, DEFAULTS["panel_offset"][1])
make_figure(
    save_path,
    panel_paths,
    panel_sz=panel_sz,
    panel_offset=panel_offset,
)
