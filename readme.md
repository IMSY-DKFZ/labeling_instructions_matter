# Labeling instructions matter
This work dealt with quantifying the effect of labeling instructions and different annotator types on annotating reference data.



## Structure


```bash
├── data_results # final metric table, survey result tables and generated tables
    ├── _tables_ # existing and generated tables
    ├── figures # generated statistical figures
    ├── expected_results # expected_results
    
├── statistics_and_figure_generators # scripts for generating figures and descriptive statistics
├── requirements.txt # requirements
```

## Installation

### Python 
The required Python 3 dependencies are located in the `requirements.txt`.

Initially, cd into your repo.

Then, use **Python 3.8**
```bash
sudo apt install python3-virtualenv # Optional

pip install virtualenv # (if you don't already have virtualenv installed)

virtualenv venv # to create your new environment (called 'venv' here)

source venv/bin/activate # to enter the virtual environment

pip install -r requirements.txt # to install the requirements in the current environment
```
Install time took less than 20 minutes.  
Note: The install time depends on the hardware and available bandwidth.

### R

Install both
```
- R version 4.0.2 
- brms version 2.16.0
```
Install time took less than 20 minutes.    
Note: The install time depends on the hardware and available bandwidth.

## Usage

### Statistics

Navigate to

```bash
├── statistics_and_figure_generators
    ├── _nat_mach_int_stats_002_key_metrics_per_metric_and_company_for_performance_comparison_table.py
    ├── _nat_mach_int_stats_003_invalid_annotations_per_company_for_per_stage_[output_table].py
```

Each script generates a single table and metric output on the command line.  
Each script uses a `data_results/_tables_` file as input.  
Parameters in the Config can be adjusted if needed.  

The default saving location for the generated figures is `data_results/_tables_`. 

The expected results after running the scripts and generating the output are located in `data_results/expected_results`.

### Figure Generation

Navigate to

```bash
├── statistics_and_figure_generators
    ├── _nat_mach_int_fig_01_001_NAT_dsc_average_companies_per_stage.py
    ├── _nat_mach_int_fig_02_survey_prof_annotator_results.py
    ├── _nat_mach_int_fig_04a_dsc_average_alle_firmen.py
    ├── _nat_mach_int_fig_04b_severe_annotation_errors_per_company.py
    ├── _nat_mach_int_fig_05_overview_survey_comparison_mturk_proff_annotator.py
    ├── _nat_mach_int_fig_10_appendix_dsc_scores_per_group.py
```

Each script generates a single figure / multiple figures.  
Each script uses a `data_results/_tables_` file as input.  
Parameters in the Config can be adjusted if needed.

The default saving location for the generated figures is `data_results/figures`. 


The computation of the figures takes less than one minute on a T480 ThinkPad (Ubuntu 20.04.4 LTS).
Thus, no smaller version of the dataset is provided. Tested on: OS: Ubuntu 20.04.4 LTS, Windows 10 (10.0.19044).

### Statistical Model (R)

**Main article mixed model:**


Navigate to

```bash
├── statistics_and_figure_generators
    ├── _nat_mach_int_two-part_zero-inflated_beta_mixed_model.R
```

Run `_nat_mach_int_two-part_zero-inflated_beta_mixed_model.R`.  
The script fits the two-part zero-inflated beta mixed model to the data.  
The output of the beta mixed model is returned to the console. 



Sample console output to identify if the model is started and working as intended. 
```bash
SAMPLING FOR MODEL 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' NOW (CHAIN 1).
Chain 1: 
Chain 1: Gradient evaluation took 0.006727 seconds
Chain 1: 1000 transitions using 10 leapfrog steps per transition would take 67.27 seconds.
Chain 1: Adjust your expectations accordingly!
Chain 1: 
Chain 1: 
Chain 1: Iteration:    1 / 4000 [  0%]  (Warmup)
```

The computation of the statistical model took around 6 hours on a working machine with an AMD R9-5900X and 
an Nvidia Geforce 3900. A performant CPU leads to a faster compute. Tested on: OS: Ubuntu 20.04.4 LTS, Windows 10 (10.0.19044). 


**Supplementary Information mixed model:**

Use either `R version 4.0.2` or `R version 4.0.3`

Navigate to

```bash
├── statistics_and_figure_generators
    ├── _nat_mach_int_supplementary_information_4_two-part_mixed_model.R
```

Same procedure as above.

## Licence
The code is under the GPLv2 or later version licence.

## Contact
For questions or feedback contact tim.raedsch@dkfz-heidelberg.de (backup: timraedsch.research@gmail.com).

