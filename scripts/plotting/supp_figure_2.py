"""Script to combine the panels of Supplementary Figure 2 and save in SVG format."""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import make_figure

save_path = (
    pathlib.Path(__file__).parents[2] / "figures/paper_supp_figures/supp_figure_2.svg"
)
panel_dir = pathlib.Path(__file__).parents[2] / "figures/vaccination_example"
panel_paths = [panel_dir / "reproduction_number.svg"]
make_figure(save_path, panel_paths)
