# covid-boosters
Python code accompanying the manuscript "Effects of individual variation and seasonal
vaccination on disease risks by Hart *et al.*

To reproduce the figures, we recommend using `conda` to create a virtual environment
named 'covidboosters' with the required dependencies specified in `environment.yml`:
```
covid-boosters $ conda env create -f environment.yml
```

The workflows required to reproduce the figures in the paper can be executed using
`snakemake` (which is installed as part of the `conda` environment), and are
encapsulated in the provided `Snakefile`. For example, Figure 1 can be reproduced (in
svg format) as follows:
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 --forceall figure_1
```
All the main text figures can be reproduced by running
```
covid-boosters $ conda activate covidboosters
(covidboosters) covid-boosters $ snakemake --cores 1 --forceall figures
```