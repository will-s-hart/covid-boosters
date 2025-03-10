"""Script to combine the panels of Figure 3 and save the figure in SVG format."""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import DEFAULTS, make_figure

save_path = pathlib.Path(__file__).parents[2] / "figures/paper_figures/figure_3.svg"
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
