rule all:
    input:
        "results/antibody_model_params.csv",
        "results/without_vaccination/methods.csv",
        "results/without_vaccination/dispersion.csv",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk_methods.svg",
        "figures/without_vaccination/outbreak_risk_dispersion.svg",
        "results/within_host_dynamics.csv",
        "figures/within_host_dynamics/antibodies.svg",
        "figures/within_host_dynamics/susceptibility.svg",
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
        "results/within_host_dynamics.csv",
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
        "figures/within_host_dynamics/antibodies.svg",
        "figures/within_host_dynamics/susceptibility.svg",
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
            "results/sensitivity_r0_mean/grid_search_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/vaccination_time_range_best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_mean/heatmap_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_mean/best_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/grid_search_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/vaccination_time_range_best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_var/heatmap_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_var/best_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/grid_search_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/best_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/vaccination_time_range_best_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_k/heatmap_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
        expand(
            "figures/sensitivity_k/best_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
        expand(
            "results/sensitivity_prop_vacc/grid_search_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/vaccination_time_range_best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_prop_vacc/heatmap_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_prop_vacc/best_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/within_host_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/grid_search_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/vaccination_time_range_best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/susceptibility_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/heatmap_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/best_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),


rule supp_results:
    input:
        expand(
            "results/sensitivity_r0_mean/grid_search_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/vaccination_time_range_best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/grid_search_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/vaccination_time_range_best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/grid_search_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/best_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/vaccination_time_range_best_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/grid_search_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/vaccination_time_range_best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/within_host_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/grid_search_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/vaccination_time_range_best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),


rule supp_figures:
    input:
        expand(
            "figures/sensitivity_r0_mean/heatmap_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_mean/best_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_var/heatmap_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_var/best_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_k/heatmap_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
        expand(
            "figures/sensitivity_k/best_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
        expand(
            "figures/sensitivity_prop_vacc/heatmap_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_prop_vacc/best_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/susceptibility_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/heatmap_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/best_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
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


rule within_host_dynamics:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/within_host_dynamics.csv",
    script:
        "scripts/within_host_dynamics.py"


rule within_host_dynamics_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/within_host_dynamics.csv",
    output:
        "figures/within_host_dynamics/antibodies.svg",
        "figures/within_host_dynamics/susceptibility.svg",
    script:
        "scripts/plotting/within_host_dynamics_plots.py"


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


rule sensitivity_r0_mean:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_r0_mean/grid_search_{r0_mean_index}.csv",
        "results/sensitivity_r0_mean/best_{r0_mean_index}.csv",
        "results/sensitivity_r0_mean/vaccination_time_range_best_{r0_mean_index}.csv",
    script:
        "scripts/sensitivity_r0_mean.py"


rule sensitivity_r0_mean_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        expand(
            "results/sensitivity_r0_mean/grid_search_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_mean/vaccination_time_range_best_{r0_mean_index}.csv",
            r0_mean_index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_r0_mean/heatmap_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_mean/best_{r0_mean_index}.svg",
            r0_mean_index=[0, 1],
        ),
    script:
        "scripts/plotting/sensitivity_r0_mean_plots.py"


rule sensitivity_r0_var:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_r0_var/grid_search_{r0_var_index}.csv",
        "results/sensitivity_r0_var/best_{r0_var_index}.csv",
        "results/sensitivity_r0_var/vaccination_time_range_best_{r0_var_index}.csv",
    script:
        "scripts/sensitivity_r0_var.py"


rule sensitivity_r0_var_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        expand(
            "results/sensitivity_r0_var/grid_search_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
        expand(
            "results/sensitivity_r0_var/vaccination_time_range_best_{r0_var_index}.csv",
            r0_var_index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_r0_var/heatmap_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_r0_var/best_{r0_var_index}.svg",
            r0_var_index=[0, 1],
        ),
    script:
        "scripts/plotting/sensitivity_r0_var_plots.py"


rule sensitivity_k:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_k/grid_search_{k_index}.csv",
        "results/sensitivity_k/best_{k_index}.csv",
        "results/sensitivity_k/vaccination_time_range_best_{k_index}.csv",
    script:
        "scripts/sensitivity_k.py"


rule sensitivity_k_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_k/grid_search_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/best_{k_index}.csv",
            k_index=[0, 1],
        ),
        expand(
            "results/sensitivity_k/vaccination_time_range_best_{k_index}.csv",
            k_index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_k/heatmap_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
        expand(
            "figures/sensitivity_k/best_{k_index}.svg",
            k_index=[0, 1, "default"],
        ),
    script:
        "scripts/plotting/sensitivity_k_plots.py"


rule sensitivity_prop_vacc:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_prop_vacc/grid_search_{prop_vacc_index}.csv",
        "results/sensitivity_prop_vacc/best_{prop_vacc_index}.csv",
        "results/sensitivity_prop_vacc/vaccination_time_range_best_{prop_vacc_index}.csv",
    script:
        "scripts/sensitivity_prop_vacc.py"


rule sensitivity_prop_vacc_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        expand(
            "results/sensitivity_prop_vacc/grid_search_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "results/sensitivity_prop_vacc/vaccination_time_range_best_{prop_vacc_index}.csv",
            prop_vacc_index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_prop_vacc/best_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_prop_vacc/heatmap_{prop_vacc_index}.svg",
            prop_vacc_index=[0, 1],
        ),
    script:
        "scripts/plotting/sensitivity_prop_vacc_plots.py"


rule sensitivity_vacc_effect:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "scripts/within_host_dynamics.py",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_vacc_effect/within_host_{half_protection_antibody_index}.csv",
        "results/sensitivity_vacc_effect/grid_search_{half_protection_antibody_index}.csv",
        "results/sensitivity_vacc_effect/best_{half_protection_antibody_index}.csv",
        "results/sensitivity_vacc_effect/vaccination_time_range_best_{half_protection_antibody_index}.csv",
    script:
        "scripts/sensitivity_vacc_effect.py"


rule sensitivity_vacc_effect_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        expand(
            "results/sensitivity_vacc_effect/within_host_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/grid_search_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "results/sensitivity_vacc_effect/vaccination_time_range_best_{half_protection_antibody_index}.csv",
            half_protection_antibody_index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_vacc_effect/susceptibility_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/heatmap_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
        expand(
            "figures/sensitivity_vacc_effect/best_{half_protection_antibody_index}.svg",
            half_protection_antibody_index=[0, 1],
        ),
    script:
        "scripts/plotting/sensitivity_vacc_effect_plots.py"
