import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts import sensitivity_vacc_effect
from scripts.default_parameters import get_default_parameters
from scripts.plotting import optimizing_vaccination_plots, plotting_utils


def make_plots():
    plotting_utils.set_sns_theme()
    color_palette = sns.color_palette()
    figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
    figure_dir.mkdir(exist_ok=True, parents=True)
    default_parameters = get_default_parameters()
    period = default_parameters["period"]
    r0_prop_variation = default_parameters[
        "unvaccinated_reproduction_no_prop_variation"
    ]
    peak_transmission_time = default_parameters["peak_transmission_time"]
    vaccination_time_range_default = default_parameters["vaccination_time_range"]
    fig_sus, ax_sus = plotting_utils.setup_figure()
    fig_cor_default, ax_cor_default = plotting_utils.setup_figure()
    for half_protection_antibody_index in [0, "baseline", 1]:
        if half_protection_antibody_index == "baseline":
            half_protection_antibody = default_parameters["susceptibility_func_params"][
                "half_protection_antibody"
            ]
            color = color_palette[0]
            results_dir = pathlib.Path(__file__).parents[2] / "results"
            load_path_within_host = results_dir / "within_host_dynamics.csv"
            load_path_default = results_dir / "vaccination_example.csv"
            load_path_grid_search = (
                results_dir / "optimizing_vaccination/grid_search.csv"
            )
            load_path_best = results_dir / "optimizing_vaccination/best.csv"
            load_path_vaccination_time_range_best = (
                results_dir / "optimizing_vaccination/vaccination_time_range_best.csv"
            )
        else:
            half_protection_antibody = (
                sensitivity_vacc_effect.half_protection_antibody_vals[
                    half_protection_antibody_index
                ]
            )
            color = color_palette[half_protection_antibody_index + 1]
            results_dir = (
                pathlib.Path(__file__).parents[2] / "results/sensitivity_vacc_effect"
            )
            load_path_within_host = (
                results_dir / f"within_host_{half_protection_antibody_index}.csv"
            )
            load_path_default = (
                results_dir / f"default_{half_protection_antibody_index}.csv"
            )
            load_path_grid_search = (
                results_dir / f"grid_search_{half_protection_antibody_index}.csv"
            )
            load_path_best = results_dir / f"best_{half_protection_antibody_index}.csv"
            load_path_vaccination_time_range_best = (
                results_dir
                / f"vaccination_time_range_best_{half_protection_antibody_index}.csv"
            )
        # Plot reproduction number without vaccination
        df = pd.read_csv(load_path_within_host, index_col="time")
        ax_sus.plot(
            df.index,
            df["susceptibility_mean"],
            label="$\\it{A_{1/2}}$ = " + f"{half_protection_antibody}",
            color=color,
        )
        # Plot COR without vaccination and with default vaccination
        df = pd.read_csv(load_path_default, index_col="time")
        df["cor"].plot(
            ax=ax_cor_default,
            label="$\\it{A_{1/2}}$ = " + f"{half_protection_antibody}",
            color=color,
        )
        if half_protection_antibody_index == "baseline":
            df["cor_unvacc"].plot(
                ax=ax_cor_default, label="", color="k", linestyle="--", alpha=0.75
            )
        # Make plots for optimization of vaccination
        optimizing_vaccination_plots.make_plots(
            load_path=load_path_grid_search,
            load_path_best=load_path_best,
            load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
            figure_path_heatmap=figure_dir
            / f"heatmap_{half_protection_antibody_index}.svg",
            figure_path_best=figure_dir / f"best_{half_protection_antibody_index}.svg",
            show_plots=False,
        )
    # Format and save susceptibility plot
    ax_sus.set_xlim(0, period)
    ax_sus.set_xticks(np.arange(0, period + 1, period / 6))
    ax_sus.set_ylim(0, 1)
    ax_sus.set_xlabel("Time since vaccination (days)")
    ax_sus.set_ylabel("Relative susceptibility")
    ax_sus.legend(loc="lower right")
    fig_sus.savefig(figure_dir / "susceptibility.pdf")
    fig_sus.savefig(figure_dir / "susceptibility.svg")
    # Format and save default COR plot
    plotting_utils.months_x_axis(ax_cor_default, period=period, no_periods=2)
    ax_cor_default.set_ylim(0, 0.5)
    plotting_utils.shade_vaccination_time_range(
        ax_cor_default, vaccination_time_range_default
    )
    ax_cor_default.set_ylabel("Case outbreak risk")
    ax_cor_default.legend(loc="lower right")
    fig_cor_default.savefig(figure_dir / "default.pdf")
    fig_cor_default.savefig(figure_dir / "default.svg")


if __name__ == "__main__":
    make_plots()
    if "snakemake" not in globals():
        plt.show()


# def make_plots():
#     plotting_utils.set_sns_theme()
#     results_dir = pathlib.Path(__file__).parents[2] / "results/sensitivity_vacc_effect"
#     figure_dir = pathlib.Path(__file__).parents[2] / "figures/sensitivity_vacc_effect"
#     figure_dir.mkdir(exist_ok=True, parents=True)

#     default_parameters = get_default_parameters()
#     half_protection_antibody_vals = np.concatenate(
#         (
#             sensitivity_vacc_effect.half_protection_antibody_vals,
#             [
#                 default_parameters["susceptibility_func_params"][
#                     "half_protection_antibody"
#                 ]
#             ],
#         ),
#     )
#     fig_susceptibility_all, ax_susceptibility_all = plotting_utils.setup_figure()
#     susceptibility_plot_list = []
#     for half_protection_antibody_index, half_protection_antibody in enumerate(
#         half_protection_antibody_vals
#     ):
#         if half_protection_antibody_index == 2:
#             load_path_within_host = results_dir / "../within_host_dynamics.csv"
#         else:
#             load_path_within_host = (
#                 results_dir / f"within_host_{half_protection_antibody_index}.csv"
#             )
#         df = pd.read_csv(load_path_within_host, index_col="time")
#         p = ax_susceptibility_all.plot(
#             df.index,
#             df["susceptibility_mean"],
#             label="$\\it{A_{1/2}}$ = " + f"{half_protection_antibody}",
#         )
#         susceptibility_plot_list.append(p[0])
#         if half_protection_antibody_index == 2:
#             continue
#         load_path_grid_search = (
#             results_dir / f"grid_search_{half_protection_antibody_index}.csv"
#         )
#         load_path_best = results_dir / f"best_{half_protection_antibody_index}.csv"
#         load_path_vaccination_time_range_best = (
#             results_dir
#             / f"vaccination_time_range_best_{half_protection_antibody_index}.csv"
#         )
#         figure_path_susceptibility = (
#             figure_dir / f"susceptibility_{half_protection_antibody_index}.svg"
#         )
#         figure_path_heatmap = (
#             figure_dir / f"heatmap_{half_protection_antibody_index}.svg"
#         )
#         figure_path_best = figure_dir / f"best_{half_protection_antibody_index}.svg"
#         fig, ax = plotting_utils.setup_figure()
#         df["susceptibility_mean"].plot(ax=ax)
#         ax.fill_between(
#             df.index,
#             df["susceptibility_95ci_lower"],
#             df["susceptibility_95ci_upper"],
#             alpha=0.5,
#         )
#         _format_susceptibility_plot(ax)
#         fig.savefig(figure_path_susceptibility)
#         fig.savefig(str(figure_path_susceptibility).replace(".svg", ".pdf"))
#         optimizing_vaccination_plots.make_plots(
#             load_path=load_path_grid_search,
#             load_path_best=load_path_best,
#             load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
#             figure_path_heatmap=figure_path_heatmap,
#             figure_path_best=figure_path_best,
#             show_plots=False,
#         )
#     susceptibility_plot_list = [
#         susceptibility_plot_list[0],
#         susceptibility_plot_list[2],
#         susceptibility_plot_list[1],
#     ]
#     _format_susceptibility_plot(ax_susceptibility_all)
#     ax_susceptibility_all.legend(
#         susceptibility_plot_list,
#         [p.get_label() for p in susceptibility_plot_list],
#         loc="lower right",
#     )
#     fig_susceptibility_all.savefig(figure_dir / "susceptibility.pdf")
#     fig_susceptibility_all.savefig(figure_dir / "susceptibility.svg")


# def _format_susceptibility_plot(ax):
#     period = get_default_parameters()["period"]
#     ax.set_xlim(0, period)
#     ax.set_xticks(np.arange(0, period + 1, period / 6))
#     ax.set_ylim(0, 1)
#     ax.set_xlabel("Time since vaccination (days)")
#     ax.set_ylabel("Relative susceptibility")


# if __name__ == "__main__":
#     make_plots()
#     if "snakemake" not in globals():
#         plt.show()
