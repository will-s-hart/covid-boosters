import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.plotting_utils import make_figure

save_path = pathlib.Path(__file__).parents[2] / "figures/paper_figures/figure_4.svg"
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
