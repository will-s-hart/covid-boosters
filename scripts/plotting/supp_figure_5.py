import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import make_figure

save_path = (
    pathlib.Path(__file__).parents[2] / "figures/paper_supp_figures/supp_figure_5.svg"
)
panel_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
panel_paths = [
    panel_dir / "susceptibility.svg",
    panel_dir / "default.svg",
    panel_dir / "best_0.svg",
    panel_dir / "best_1.svg",
]
make_figure(save_path, panel_paths)
