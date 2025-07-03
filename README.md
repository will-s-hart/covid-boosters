[![DOI](https://zenodo.org/badge/776044303.svg)](https://doi.org/10.5281/zenodo.15800215)

Data and Python code accompanying the manuscript "Effects of individual variation and seasonal
vaccination on disease risks" by Hart *et al*.

To reproduce the figures, we recommend using `conda` to create a virtual environment
named 'covidboosters' with the required dependencies specified in `environment.yml`:
```
covid-boosters $ conda env create -f environment.yml
```

The workflows required to reproduce the figures in the paper can be executed using
`snakemake` (which is installed as part of the `conda` environment), and are
encapsulated in the provided `Snakefile`. For example, the workflow to create Figure 1
(in svg format) can be executed as follows:
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 figure_1
```
All tasks required to reproduce the main text figures can be (re-)executed as follows:
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 --forceall figures
```
