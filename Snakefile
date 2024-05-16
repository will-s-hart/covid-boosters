mean_index_vals = [0, 1, 2]
prop_var_index_vals = [0, 1, 2]


rule all:
    input:
        "results/antibody_model_params.csv",
        "results/without_vaccination/methods.csv",
        "results/without_vaccination/dispersion.csv",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
        "results/within_host_example.csv",
        "figures/within_host_example/antibodies.svg",
        "figures/within_host_example/susceptibility.svg",
        "results/vaccination_example.csv",
        "results/susceptibility_all_0.csv",
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.svg",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        "figures/optimizing_vaccination/heatmap.svg",
        "figures/optimizing_vaccination/best.svg",


rule results:
    input:
        "results/antibody_model_params.csv",
        "results/without_vaccination/methods.csv",
        "results/without_vaccination/dispersion.csv",
        "results/within_host_example.csv",
        "results/vaccination_example.csv",
        "results/susceptibility_all_0.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",


rule figures:
    input:
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
        "figures/within_host_example/antibodies.svg",
        "figures/within_host_example/susceptibility.svg",
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.svg",
        "figures/optimizing_vaccination/heatmap.svg",
        "figures/optimizing_vaccination/best.svg",


rule supp:
    input:
        expand(
            "results/sensitivity_unvacc_r/grid_search_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "results/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "results/sensitivity_unvacc_r/vaccination_time_range_best_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "figures/sensitivity_unvacc_r/heatmap_{mean_index}_{prop_var_index}.svg",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "figures/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.svg",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),


rule supp_results:
    input:
        expand(
            "results/sensitivity_unvacc_r/grid_search_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "results/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "results/sensitivity_unvacc_r/vaccination_time_range_best_{mean_index}_{prop_var_index}.csv",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),


rule supp_figures:
    input:
        expand(
            "figures/sensitivity_unvacc_r/heatmap_{mean_index}_{prop_var_index}.svg",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),
        expand(
            "figures/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.svg",
            mean_index=mean_index_vals,
            prop_var_index=prop_var_index_vals,
        ),


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
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
    script:
        "scripts/plotting/without_vaccination_plots.py"


rule within_host_example:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/within_host_example.csv",
    script:
        "scripts/within_host_example.py"


rule within_host_example_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/within_host_example.csv",
    output:
        "figures/within_host_example/antibodies.svg",
        "figures/within_host_example/susceptibility.svg",
    script:
        "scripts/plotting/within_host_example_plots.py"


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
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.svg",
    script:
        "scripts/plotting/vaccination_example_plots.py"


rule optimizing_vaccination:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
    output:
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
    script:
        "scripts/optimizing_vaccination.py"


rule optimizing_vaccination_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
    output:
        "figures/optimizing_vaccination/heatmap.svg",
        "figures/optimizing_vaccination/best.svg",
    script:
        "scripts/plotting/optimizing_vaccination_plots.py"


rule sensitivity_unvacc_r:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_unvacc_r/grid_search_{mean_index}_{prop_var_index}.csv",
        "results/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.csv",
        "results/sensitivity_unvacc_r/vaccination_time_range_best_{mean_index}_{prop_var_index}.csv",
    script:
        "scripts/sensitivity_unvacc_r.py"


rule sensitivity_unvacc_r_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/sensitivity_unvacc_r/grid_search_{mean_index}_{prop_var_index}.csv",
        "results/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.csv",
        "results/sensitivity_unvacc_r/vaccination_time_range_best_{mean_index}_{prop_var_index}.csv",
    output:
        "figures/sensitivity_unvacc_r/heatmap_{mean_index}_{prop_var_index}.svg",
        "figures/sensitivity_unvacc_r/best_{mean_index}_{prop_var_index}.svg",
    script:
        "scripts/plotting/sensitivity_unvacc_r_plots.py"
