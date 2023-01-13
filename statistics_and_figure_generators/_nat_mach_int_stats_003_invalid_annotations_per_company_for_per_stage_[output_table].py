import pandas as pd
import os
import numpy as np
import warnings

################
'''
Goal: 
Creates a table with 
the amount of invalid annotations (= metric score of 0)
for each annotation provider and for every single stage.
'''
################

safe_name = '2022-01-18_Overview_severe_annotation_errors_per_provider_and_stage'
save_path = '../data_results//_tables_'
csv = '../data_results/_tables_/2021-12-08_labeling_instructions_table_v1.0.csv'

df = pd.read_csv(os.path.normpath(csv))
metric = 'DSC_tool' # metric value zero equals invalid annotation
stages = ['first', 'second', 'third']
companies = sorted(df['Company'].unique())


# initiate df with target columns
df_results = pd.DataFrame(columns=['Company', 'Stage', 'invalid_annotations',
                                   'diff_to_prev_stage_absolute',
                                   'diff_to_prev_stage_relative [in %]'])

# iterate over metrics
test_size_pre_filter = df.shape
df = df[df['QA'] == 'annotate']
test_size_post_filter = df.shape
print(f"Pre fiter size = {test_size_pre_filter} and post filter size = {test_size_post_filter}. Same size is the intended outcome.")


# iterate over companies
for company in companies:
    df_company = df[df['Company'] == company]

    list_invalid_annotations = []
    # iterate over stages
    for stage in stages:
        df_stage = df_company[df_company['Stage'] == stage]

        number_of_invalid = df_stage[metric].value_counts()[0] # default returns smallest number at location 0

        # get changes absolute and relative to former stage
        if len(list_invalid_annotations) == 0:
            diff_to_prev_abs = np.nan
            diff_to_prev_rel = np.nan
        else:
            diff_to_prev_abs = number_of_invalid - list_invalid_annotations[-1]
            diff_to_prev_rel = round(diff_to_prev_abs / list_invalid_annotations[-1] * 100, 1)

        list_invalid_annotations.append(number_of_invalid)
        new_row = (company, stage, number_of_invalid, diff_to_prev_abs, diff_to_prev_rel)
        print(new_row)
        df_results.loc[len(df_results)] = new_row

# sort by stage for easier interpretability
df_results = df_results.sort_values(by=['Stage'])

# report median, max and min per annotation provider
for stage in stages:
    prev_stage = stages[stages.index(stage)-1]
    if stage == 'first':
        continue
    df_analyse = df_results[df_results['Stage'] == stage]
    max_abs = df_analyse['diff_to_prev_stage_absolute'].max()
    min_abs = df_analyse['diff_to_prev_stage_absolute'].min()
    med_abs = df_analyse['diff_to_prev_stage_absolute'].median()
    med_rel = df_analyse['diff_to_prev_stage_relative [in %]'].median()
    max_rel = df_analyse['diff_to_prev_stage_relative [in %]'].max()
    min_rel = df_analyse['diff_to_prev_stage_relative [in %]'].min()

    print(f"Change stage {prev_stage} to {stage} | ABSOLUTE -> Median: {med_abs}, Max: {max_abs}, Min: {min_abs}")
    print(f"Change stage {prev_stage} to {stage} | RELATIVE[in %] -> Median: {med_rel}, Max: {max_rel}, Min: {min_rel}")

# add medians for the overall companies
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for stage in stages:
        df_stag_prov = df_results[df_results['Stage'] == stage]
        df_stag_prov = df_stag_prov[df_stag_prov['Company'] != 'MTurk']
        med_number_of_invalid = df_stag_prov['invalid_annotations'].median()
        med_diff_to_prev_abs = df_stag_prov['diff_to_prev_stage_absolute'].median()
        med_diff_to_prev_rel = df_stag_prov['diff_to_prev_stage_relative [in %]'].median()
        new_row = ('Median Companies', stage, med_number_of_invalid, med_diff_to_prev_abs, med_diff_to_prev_rel)
        df_results.loc[len(df_results)] = new_row

# save
file_path = os.path.join(os.path.normpath(save_path), safe_name +'.csv')
df_results.to_csv(file_path, na_rep= 'not applicable', index=False)
print(f'The generated file is located at {os.path.abspath(file_path)}')