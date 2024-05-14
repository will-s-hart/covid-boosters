import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parents[2]))

from scripts.plotting import optimizing_vaccination_plots

load_path = snakemake.input[2]  # noqa: F821
load_path_best = snakemake.input[3]  # noqa: F821
load_path_vaccination_time_range_best = snakemake.input[4]  # noqa: F821
figure_path_heatmap = snakemake.output[0]  # noqa: F821
figure_path_best = snakemake.output[1]  # noqa: F821

figure_dir = pathlib.Path(__file__).parents[2] / "figures/optimizing_vaccination"
figure_dir.mkdir(exist_ok=True, parents=True)

optimizing_vaccination_plots.make_plots(
    load_path=load_path,
    load_path_best=load_path_best,
    load_path_vaccination_time_range_best=load_path_vaccination_time_range_best,
    figure_path_heatmap=figure_path_heatmap,
    figure_path_best=figure_path_best,
)
