rule all:
    input:
        "figures/without_vaccination/reproduction_number.pdf",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.pdf",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.pdf",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
        "figures/vaccination_example/susceptibility.pdf",
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/reproduction_number.pdf",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.pdf",
        "figures/vaccination_example/outbreak_risk.svg",


rule format_antibody_model_param_estimates:
    input:
        "data/12HCWs_NLMEM_parameters.csv",
        "data/1618_FukushimaVaccineCohorts_NLSM_parameters.csv",
    output:
        "results/antibody_model_params.csv",
    script:
        "scripts/format_antibody_model_param_estimates.py"


rule without_vaccination:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/without_vaccination/methods.csv",
        "results/without_vaccination/dispersion.csv",
    script:
        "scripts/without_vaccination.py"


rule without_vaccination_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/without_vaccination/methods.csv",
        "results/without_vaccination/dispersion.csv",
    output:
        "figures/without_vaccination/reproduction_number.pdf",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.pdf",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.pdf",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
    script:
        "scripts/plotting/without_vaccination_plots.py"


rule vaccination_example:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/vaccination_example.csv",
        "results/susceptibility_all_0.csv",
    script:
        "scripts/vaccination_example.py"


rule vaccination_example_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/vaccination_example.csv",
    output:
        "figures/vaccination_example/susceptibility.pdf",
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/reproduction_number.pdf",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.pdf",
        "figures/vaccination_example/outbreak_risk.svg",
    script:
        "scripts/plotting/vaccination_example_plots.py"
