import pandas as pd
import os


################
'''
Goal: 
Creates a table with 
'Metric', 'Company', 'Median', 'IQR_max', 'IQR_min', 'IQR', 'Max', 'Min'
for the selected metrics and companies for every single stage.
Furthermore adds absolute and relative changes between the different stages to the table.
Lastly, outputs median, max and min of relevant changes for
a) across all providers
b) separate for the type of annotation provider.
'''
################

safe_name = '2022-01-18_Overview_metrics_mean_quantiles_table'
save_path = '../data_results//_tables_'
csv = '../data_results//_tables_/2021-12-08_labeling_instructions_table_v1.0.csv'
round_decimel = 2

df = pd.read_csv(os.path.normpath(csv))
# levels = ['image', 'instrument']
metrics = ['DSC_img']
stages = ['first', 'second', 'third'] # inc
companies = df['Company'].unique() # inc


# initiate df with target columns
df_results = pd.DataFrame(
    columns=['Metric', 'Company', 'Stage', 'Median', 'IQR_max', 'IQR_min', 'IQR', 'Max', 'Min'])

# iterate over metrics to get raw metric scores
for metric in metrics:
    test_size_pre_filter = df.shape
    df = df[df['QA'] == 'annotate']
    test_size_post_filter = df.shape
    df = df[(df['Instance_ID'] == 1)]
    print(f"Pre fiter size = {test_size_pre_filter} and post filter size = {test_size_post_filter}. Same size is the intended outcome.")

    # iterate over companies
    for company in companies:
        df_company = df[df['Company'] == company]

        # interate over stages
        for counter, stage in enumerate(stages):
            # initiate row with metric_name company and stage
            new_row = [metric, company, stage]
            df_stage = df_company[df_company['Stage'] == stage]

            target_column  = df_stage[metric]
            median = round(target_column.describe()['50%'], round_decimel)
            IQR_min = round(target_column.describe()['25%'], round_decimel)
            IQR_max = round(target_column.describe()['75%'], round_decimel)
            IQR = round(IQR_max-IQR_min, round_decimel)
            min = round(target_column.min(), round_decimel)
            max = round(target_column.max(), round_decimel)
            stage_package_metrics = [median, IQR_max, IQR_min, IQR, max, min]
            new_row.extend(stage_package_metrics)

            # append new row to df
            print(new_row)
            df_results.loc[len(df_results)] = new_row

# get metric changes abs and relative
dfs = []
for number in [-1, 0]:
    filtered_df = df_results[df_results['Stage'] != stages[number]]


    for company in companies:
        filtered_df_comp_clean = filtered_df[filtered_df['Company'] == company]
        stage_transfer = '-to-'.join(filtered_df_comp_clean['Stage'].unique())
        filtered_df_comp = filtered_df_comp_clean.drop(columns = ['Company','Metric', 'Stage'])

        diff_abs = filtered_df_comp.diff().iloc[[1]]
        diff_abs[['Metric', 'Company', 'Stage']] = [['absolute change', company, stage_transfer]]

        diff_rel = round(filtered_df_comp.pct_change().iloc[[1]],4)
        diff_rel[['Metric', 'Company', 'Stage']] = [['relative change [in %]', company, stage_transfer]]

        df_company_with_abs_and_rel_change = pd.concat([filtered_df_comp_clean, diff_abs, diff_rel])
        dfs.append(df_company_with_abs_and_rel_change)

df_final_results = pd.concat(dfs).sort_values(by= ['Metric', 'Company', 'Stage'])
df_final_results = df_final_results.drop_duplicates()





# safe metric results to csv
file_path = os.path.join(os.path.normpath(save_path), safe_name) + '.csv'
df_final_results.to_csv(file_path, index=False)




# AGGREGATED: generate the medians, max and min values for comparing the three labeling instructions
for metric in df_final_results['Metric'].unique():
    if metric == 'DSC_img':
        continue
    df_met = df_final_results[df_final_results['Metric'] == metric]

    for stage_transfer in df_met['Stage'].unique():

        df_stage_transfer = round(df_met[df_met['Stage'] == stage_transfer],3)
        med_med = df_stage_transfer['Median'].median()
        med_max = df_stage_transfer['Median'].max()
        med_min = df_stage_transfer['Median'].min()
        iqr_med = df_stage_transfer['IQR'].median()
        iqr_max = df_stage_transfer['IQR'].max()
        iqr_min = df_stage_transfer['IQR'].min()

        print(f"ACROSS ALL ANN. PROVIDERS | For {metric} | {stage_transfer} Median DSC change, we obtain a Median of {med_med}, Max {med_max}, Min {med_min}")
        print(f"ACROSS ALL ANN. PROVIDERS | For {metric} | {stage_transfer} IQR change, we obtain a Median of {iqr_med}, Max {iqr_max}, Min {iqr_min}")


# COMPANIES vs MTURK: generate the medians, max and min values for comparing the three labeling instructions
for metric in df_final_results['Metric'].unique():
    df_met = df_final_results[df_final_results['Metric'] == metric]
    df_met = df_met[df_met['Company'] != 'MTurk']

    for stage_transfer in df_met['Stage'].unique():

        df_stage_transfer = round(df_met[df_met['Stage'] == stage_transfer],3)
        med_med = df_stage_transfer['Median'].median()
        med_max = df_stage_transfer['Median'].max()
        med_min = df_stage_transfer['Median'].min()
        iqr_med = round(df_stage_transfer['IQR'].median(),3)
        iqr_max = df_stage_transfer['IQR'].max()
        iqr_min = df_stage_transfer['IQR'].min()

        print(f"ACROSS COMPANIES| For {metric} | for {stage_transfer} Median DSC change, we obtain a Median of {med_med}, Max {med_max}, Min {med_min}")
        print(f"ACROSS COMPANIES| For {metric} | for {stage_transfer} IQR change, we obtain a Median of {iqr_med}, Max {iqr_max}, Min {iqr_min}")

# Output file location
print(f'The generated file is located at {os.path.abspath(file_path)}')