"""Script to combine the panels of Supplementary Figure 1 and save in SVG format."""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import DEFAULTS, make_figure

save_path = (
    pathlib.Path(__file__).parents[2] / "figures/paper_supp_figures/supp_figure_1.svg"
)
panel_dir = pathlib.Path(__file__).parents[2] / "figures/superspreading"
panel_paths = [panel_dir / "transmission_proportions.svg"]
panel_sz = (DEFAULTS["panel_sz"][0], 335)
make_figure(save_path, panel_paths, panel_sz=panel_sz)
