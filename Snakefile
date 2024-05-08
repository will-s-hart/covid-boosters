rule all:
    input:
        "figures/without_vaccination/reproduction_number.pdf",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.pdf",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.pdf",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",


rule format_parameter_estimates:
    input:
        "data/12HCWs_NLMEM_parameters.csv",
        "data/1618_FukushimaVaccineCohorts_NLSM_parameters.csv",
    output:
        "results/antibody_model_params_pop.csv",
        "results/antibody_model_params_random_effects.csv",
    script:
        "scripts/format_parameter_estimates.py"


rule without_vaccination:
    input:
        "results/antibody_model_params_pop.csv",
        "results/antibody_model_params_random_effects.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/without_vaccination_methods.csv",
        "results/without_vaccination_dispersion.csv",
    script:
        "scripts/without_vaccination.py"


rule without_vaccination_plots:
    input:
        "scripts/plotting/plotting_setup.py",
        "results/without_vaccination_methods.csv",
        "results/without_vaccination_dispersion.csv",
    output:
        "figures/without_vaccination/reproduction_number.pdf",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.pdf",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.pdf",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
    script:
        "scripts/plotting/without_vaccination_plots.py"
