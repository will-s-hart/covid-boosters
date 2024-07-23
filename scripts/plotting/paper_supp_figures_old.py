import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting.paper_figures_old import DEFAULTS, make_figure

FIGURE_DIR = pathlib.Path(__file__).parents[2] / "figures/paper_supp_figures"


def make_supp_fig1():
    save_path = FIGURE_DIR / "figS1.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/superspreading"
    panel_paths = [
        panel_dir / "infectiousness_factors.svg",
        panel_dir / "transmission_proportions.svg",
    ]
    panel_sz = (DEFAULTS["panel_sz"][0], 335)
    make_figure(save_path, panel_paths, panel_sz=panel_sz)


def make_supp_fig2():
    save_path = FIGURE_DIR / "figS2.svg"
    panel_paths = [
        pathlib.Path(__file__).parents[2] / "figures/model_input/generation_time.svg"
    ]
    panel_sz = (DEFAULTS["panel_sz"][0], 335)
    panel_offset = DEFAULTS["panel_offset"]
    panel_positions = [
        (-20, panel_offset[1]),
    ]
    make_figure(
        save_path, panel_paths, panel_sz=panel_sz, panel_positions=panel_positions
    )


def make_supp_fig3():
    save_path = FIGURE_DIR / "figS3.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_mean"
    panel_paths = [
        panel_dir / "reproduction_number.svg",
        panel_dir / "default.svg",
        panel_dir / "best_0.svg",
        panel_dir / "best_1.svg",
    ]
    make_figure(save_path, panel_paths)


def make_supp_fig4():
    save_path = FIGURE_DIR / "figS4.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_r0_var"
    panel_paths = [
        panel_dir / "reproduction_number.svg",
        panel_dir / "default.svg",
        panel_dir / "best_0.svg",
        panel_dir / "best_1.svg",
    ]
    make_figure(save_path, panel_paths)


def make_supp_fig5():
    save_path = FIGURE_DIR / "figS5.svg"
    panel_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
    panel_paths = [
        panel_dir / "susceptibility.svg",
        panel_dir / "default.svg",
        panel_dir / "best_0.svg",
        panel_dir / "best_1.svg",
    ]
    make_figure(save_path, panel_paths)


if __name__ == "__main__":
    FIGURE_DIR.mkdir(exist_ok=True, parents=True)
    make_supp_fig1()
    make_supp_fig2()
    make_supp_fig3()
    make_supp_fig4()
    make_supp_fig5()
