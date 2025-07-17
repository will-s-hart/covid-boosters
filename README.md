[![DOI](https://zenodo.org/badge/776044303.svg)](https://doi.org/10.5281/zenodo.15800215)

Data and Python code accompanying the manuscript "Effects of individual variation and
seasonal vaccination on disease risks" by Hart *et al*.

To reproduce the figures, we recommend using `conda` to create a virtual environment
named 'covidboosters' with the required dependencies specified in `environment.yml`
(expected install time around 1 minute, tested on a 16 GB M2 Pro MacBook):
```
covid-boosters $ conda env create -f environment.yml
```
Note that version numbers of all dependencies are specified in the `environment.yml`
file. Alternatively, we provide a `pyproject.toml` file that can be used with the
[Pixi](https://pixi.sh/latest/) package manager to create an environment with the same
dependencies.

The workflows required to reproduce the figures in the paper can be executed using
`snakemake` (which is installed as part of the `conda` environment), and are
encapsulated in the provided `Snakefile`. For example, the workflow to create Figure 1
(in svg format) can be executed as follows (expected runtime around 20 minutes, tested
on a 16 GB M2 Pro MacBook):
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 --forceall figure_1
```
All tasks required to reproduce the main text figures can be executed as follows
(expected runtime around 4 hours, tested on a 16 GB M2 Pro MacBook):
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 --forceall figures
```
Reproduced figures will be saved into the `figures/paper_figures` directory.