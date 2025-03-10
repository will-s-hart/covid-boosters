"""Script to combine the panels of Supplementary Figure 4 and save in SVG format."""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import make_figure

save_path = (
    pathlib.Path(__file__).parents[2] / "figures/paper_supp_figures/supp_figure_4.svg"
)
panel_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_var"
panel_paths = [
    panel_dir / "reproduction_number.svg",
    panel_dir / "default.svg",
    panel_dir / "best_0.svg",
    panel_dir / "best_1.svg",
]
make_figure(save_path, panel_paths)
