rule figures:
    input:
        expand(
            "figures/paper_figures/fig{fig_no}.{extension}",
            fig_no=range(1, 5),
            extension=["pdf", "png"],
        ),


rule supp_figures:
    input:
        expand(
            "figures/paper_supp_figures/figS{fig_no}.{extension}",
            fig_no=range(1, 5),
            extension=["pdf", "png"],
        ),


rule figures_svg:
    input:
        "figures/paper_figures/templates/fig1_template.svg",
        "figures/without_vaccination/reproduction_number.svg",
        "figures/superspreading/infectiousness_factors.svg",
        "figures/model_input/generation_time.svg",
        "figures/simulation_examples/simulations.svg",
        "figures/without_vaccination/outbreak_risk.svg",
        "figures/within_host_dynamics/antibodies.svg",
        "figures/within_host_dynamics/susceptibility.svg",
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/unvaccinated_reproduction_number.svg",
        "figures/vaccination_example/reproduction_number.svg",
        "figures/vaccination_example/outbreak_risk.svg",
        "figures/optimizing_vaccination/heatmap.svg",
        "figures/optimizing_vaccination/best.svg",
        "figures/sensitivity_k/default.svg",
        "figures/sensitivity_k/best_0.svg",
        "figures/sensitivity_k/best_1.svg",
        "figures/sensitivity_prop_vacc/default.svg",
        "figures/sensitivity_prop_vacc/best_0.svg",
        "figures/sensitivity_prop_vacc/best_1.svg",
    output:
        "figures/paper_figures/fig1.svg",
        "figures/paper_figures/fig2.svg",
        "figures/paper_figures/fig3.svg",
        "figures/paper_figures/fig4.svg",
    script:
        "scripts/plotting/paper_figures.py"


rule supp_figures_svg:
    input:
        "scripts/plotting/paper_figures.py",
        "figures/superspreading/transmission_proportions.svg",
        "figures/sensitivity_r0_mean/reproduction_number.svg",
        "figures/sensitivity_r0_mean/default.svg",
        "figures/sensitivity_r0_mean/best_0.svg",
        "figures/sensitivity_r0_mean/best_1.svg",
        "figures/sensitivity_r0_var/reproduction_number.svg",
        "figures/sensitivity_r0_var/default.svg",
        "figures/sensitivity_r0_var/best_0.svg",
        "figures/sensitivity_r0_var/best_1.svg",
        "figures/sensitivity_vacc_effect/susceptibility.svg",
        "figures/sensitivity_vacc_effect/default.svg",
        "figures/sensitivity_vacc_effect/best_0.svg",
        "figures/sensitivity_vacc_effect/best_1.svg",
    output:
        "figures/paper_supp_figures/figS1.svg",
        "figures/paper_supp_figures/figS2.svg",
        "figures/paper_supp_figures/figS3.svg",
        "figures/paper_supp_figures/figS4.svg",
    script:
        "scripts/plotting/paper_supp_figures.py"


rule fig_svg_to_pdf:
    input:
        "figures/paper_figures/fig{fig_no}.svg",
    output:
        "figures/paper_figures/fig{fig_no}.pdf",
    shell:
        "inkscape --export-type=pdf --export-filename={output} {input}"


rule fig_svg_to_png:
    input:
        "figures/paper_figures/fig{fig_no}.svg",
    output:
        "figures/paper_figures/fig{fig_no}.png",
    shell:
        "inkscape --export-type=png --export-filename={output} {input}"


rule supp_fig_svg_to_pdf:
    input:
        "figures/paper_supp_figures/fig{fig_no}.svg",
    output:
        "figures/paper_supp_figures/fig{fig_no}.pdf",
    shell:
        "inkscape --export-type=pdf --export-filename={output} {input}"


rule supp_fig_svg_to_png:
    input:
        "figures/paper_supp_figures/fig{fig_no}.svg",
    output:
        "figures/paper_supp_figures/fig{fig_no}.png",
    shell:
        "inkscape --export-type=png --export-filename={output} {input}"


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
        "results/without_vaccination/reproduction_number.csv",
        "results/without_vaccination/analytic.csv",
        "results/without_vaccination/simulated.csv",
    script:
        "scripts/without_vaccination.py"


rule without_vaccination_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/without_vaccination/reproduction_number.csv",
        "results/without_vaccination/analytic.csv",
        "results/without_vaccination/simulated.csv",
    output:
        "figures/without_vaccination/reproduction_number.svg",
        "figures/without_vaccination/outbreak_risk.svg",
    script:
        "scripts/plotting/without_vaccination_plots.py"


rule model_input_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
    output:
        "figures/model_input/generation_time.svg",
    script:
        "scripts/plotting/model_input_plots.py"


rule superspreading_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
    output:
        expand(
            "figures/superspreading/{figure}.svg",
            figure=["infectiousness_factors", "transmission_proportions"],
        ),
    script:
        "scripts/plotting/superspreading_plots.py"


rule simulation_examples:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/simulation_examples/simulations.csv",
    script:
        "scripts/simulation_examples.py"


rule simulation_examples_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/simulation_examples/simulations.csv",
    output:
        "figures/simulation_examples/simulations.svg",
    script:
        "scripts/plotting/simulation_examples_plots.py"


rule within_host_dynamics:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
    output:
        "results/within_host_dynamics.csv",
        "results/susceptibility_all_0.csv",
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


rule vaccination_example:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
    output:
        "results/vaccination_example.csv",
    script:
        "scripts/vaccination_example.py"


rule vaccination_example_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "results/vaccination_example.csv",
    output:
        "figures/vaccination_example/susceptibility.svg",
        "figures/vaccination_example/unvaccinated_reproduction_number.svg",
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


rule sensitivity_k:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_k/default_{index}.csv",
        "results/sensitivity_k/grid_search_{index}.csv",
        "results/sensitivity_k/best_{index}.csv",
        "results/sensitivity_k/vaccination_time_range_best_{index}.csv",
    script:
        "scripts/sensitivity_k.py"


rule sensitivity_k_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/vaccination_example.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_k/{result}_{index}.csv",
            result=["default", "grid_search", "best", "vaccination_time_range_best"],
            index=[0, 1],
        ),
    output:
        "figures/sensitivity_k/default.svg",
        expand(
            "figures/sensitivity_k/{figure}_{index}.svg",
            figure=["best", "heatmap"],
            index=[0, 1, "baseline"],
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
        "results/sensitivity_prop_vacc/default_{index}.csv",
        "results/sensitivity_prop_vacc/grid_search_{index}.csv",
        "results/sensitivity_prop_vacc/best_{index}.csv",
        "results/sensitivity_prop_vacc/vaccination_time_range_best_{index}.csv",
    script:
        "scripts/sensitivity_prop_vacc.py"


rule sensitivity_prop_vacc_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/vaccination_example.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_prop_vacc/{result}_{index}.csv",
            result=["default", "grid_search", "best", "vaccination_time_range_best"],
            index=[0, 1],
        ),
    output:
        "figures/sensitivity_prop_vacc/default.svg",
        expand(
            "figures/sensitivity_prop_vacc/{figure}_{index}.svg",
            figure=["best", "heatmap"],
            index=[0, 1, "baseline"],
        ),
    script:
        "scripts/plotting/sensitivity_prop_vacc_plots.py"


rule sensitivity_r0_mean:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "results/susceptibility_all_0.csv",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_r0_mean/default_{index}.csv",
        "results/sensitivity_r0_mean/grid_search_{index}.csv",
        "results/sensitivity_r0_mean/best_{index}.csv",
        "results/sensitivity_r0_mean/vaccination_time_range_best_{index}.csv",
    script:
        "scripts/sensitivity_r0_mean.py"


rule sensitivity_r0_mean_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/vaccination_example.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_r0_mean/{result}_{index}.csv",
            result=["default", "grid_search", "best", "vaccination_time_range_best"],
            index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_r0_mean/{figure}.svg",
            figure=["reproduction_number", "default"],
        ),
        expand(
            "figures/sensitivity_r0_mean/{figure}_{index}.svg",
            figure=["best", "heatmap"],
            index=[0, 1, "baseline"],
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
        "results/sensitivity_r0_var/default_{index}.csv",
        "results/sensitivity_r0_var/grid_search_{index}.csv",
        "results/sensitivity_r0_var/best_{index}.csv",
        "results/sensitivity_r0_var/vaccination_time_range_best_{index}.csv",
    script:
        "scripts/sensitivity_r0_var.py"


rule sensitivity_r0_var_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/vaccination_example.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_r0_var/{result}_{index}.csv",
            result=["default", "grid_search", "best", "vaccination_time_range_best"],
            index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_r0_var/{figure}.svg",
            figure=["reproduction_number", "default"],
        ),
        expand(
            "figures/sensitivity_r0_var/{figure}_{index}.svg",
            figure=["best", "heatmap"],
            index=[0, 1, "baseline"],
        ),
    script:
        "scripts/plotting/sensitivity_r0_var_plots.py"


rule sensitivity_vacc_effect:
    input:
        "results/antibody_model_params.csv",
        "scripts/default_parameters.py",
        "covidboosters/base.py",
        "scripts/within_host_dynamics.py",
        "scripts/vaccination_example.py",
        "scripts/optimizing_vaccination.py",
    output:
        "results/sensitivity_vacc_effect/within_host_{index}.csv",
        "results/sensitivity_vacc_effect/default_{index}.csv",
        "results/sensitivity_vacc_effect/grid_search_{index}.csv",
        "results/sensitivity_vacc_effect/best_{index}.csv",
        "results/sensitivity_vacc_effect/vaccination_time_range_best_{index}.csv",
    script:
        "scripts/sensitivity_vacc_effect.py"


rule sensitivity_vacc_effect_plots:
    input:
        "scripts/plotting/plotting_utils.py",
        "scripts/plotting/optimizing_vaccination_plots.py",
        "results/within_host_dynamics.csv",
        "results/vaccination_example.csv",
        "results/optimizing_vaccination/grid_search.csv",
        "results/optimizing_vaccination/best.csv",
        "results/optimizing_vaccination/vaccination_time_range_best.csv",
        expand(
            "results/sensitivity_vacc_effect/{result}_{index}.csv",
            result=[
                "within_host",
                "default",
                "grid_search",
                "best",
                "vaccination_time_range_best",
            ],
            index=[0, 1],
        ),
    output:
        expand(
            "figures/sensitivity_vacc_effect/{figure}.svg",
            figure=["susceptibility", "default"],
        ),
        expand(
            "figures/sensitivity_vacc_effect/{figure}_{index}.svg",
            figure=["best", "heatmap"],
            index=[0, 1],
        ),
    script:
        "scripts/plotting/sensitivity_vacc_effect_plots.py"
