import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import os
import warnings
from cmcrameri import cm

'''
Goal: Generates an figure with a comparative overview of the 
work characteristics for MTurk crowdworkers and professional annotators. 
'''

### Config ###
title_png = 'figure_5_comparison_prof_annotators_and_mturk_crowdworkers'
csv_prof = '../data_results/_tables_/survey_anonymized.csv'
csv_mturk = '../data_results/_tables_/survey_mturk_test.csv'
safe_loc = '../data_results/figures'
safe_date = '2022-01-18'

# Global Styling
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

# load df and remove invalid prof entries
df_prof = pd.read_csv(os.path.normpath(csv_prof))
df_prof = df_prof[df_prof['Entry'] == 'x']

# load df mturk and remove invalid prof entries
df_mturk = pd.read_csv(os.path.normpath(csv_mturk))

dfs = [df_prof, df_mturk]

# spawn figure with subplots
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 5))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.3)

# general setup
name = ['Prof. Annotator', 'MTurk']
colors = ['#d2d2d2ff', '#3c437b']

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    ####################
    # first chart: 'Is labeling your main source of income?'#
    # setup first chart
    sort_list = ['No', 'Yes']
    df_plot = pd.DataFrame(columns=sort_list)
    interest = ['Main source income']
    title = '(a) Is labeling your main source of income?'
    cmap = cm.batlow

    # get data and transform to percentage values
    for counter, df in enumerate(dfs):
        row_values = df[interest[0]].value_counts().reindex(sort_list).tolist()
        sum_r = sum(row_values)
        row_values_perc = [100 * x / sum_r for x in row_values]
        df_plot.loc[name[counter]] = row_values_perc

    # create plot
    stacked_bar = df_plot.plot.bar(stacked=True, colormap=cmap, ax=ax1, rot=0)
    stacked_bar.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())

    # set title and placement
    stacked_bar.text(0.5, 1.03, title,
                     horizontalalignment='center',
                     transform=stacked_bar.transAxes,
                     weight='bold')

    # modify legend
    handles, labels = stacked_bar.get_legend_handles_labels()
    stacked_bar.legend(handles, labels, bbox_to_anchor=(0.98, 0.6), loc='upper left', ncol=1, fontsize='x-small',
                       columnspacing=1)
    # grid
    stacked_bar.xaxis.grid(False)

    ####################
    # second chart
    # setup second chart
    sort_list = ['0 days',
                 '1 day',
                 '2 days',
                 '3 days',
                 '4 days',
                 '5 days',
                 '> 5 days']

    agg_dict = {'0 days per week': '0 days',
                '1 day per week': '1 day',
                '2 days per week': '2 days',
                '3 days per week': '3 days',
                '4 days per week': '4 days',
                '4  days per week': '4 days',
                '5 days per week': '5 days',
                'More than 5 days per week': '> 5 days'}

    df_plot = pd.DataFrame(columns=sort_list)
    interest = ['How often per week?']
    title = '(b) How often do you label per week?'


    # get data and transform to percentage values
    for counter, df in enumerate(dfs):
        df = df.replace({interest[0]: agg_dict})
        row_values = df[interest[0]].value_counts().reindex(sort_list).tolist()
        row_values = pd.Series(row_values).fillna(0).tolist()
        sum_r = sum(row_values)
        row_values_perc = [100 * x / sum_r for x in row_values]
        df_plot.loc[name[counter]] = row_values_perc


    # create plot
    stacked_bar2 = df_plot.plot.bar(stacked=True, colormap=cmap, ax=ax4, rot=0)
    stacked_bar2.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())

    # modify legend
    handles, labels = stacked_bar2.get_legend_handles_labels()
    stacked_bar2.legend(handles,
                        labels,
                        bbox_to_anchor=(0.98, 0.83),
                        loc='upper left',
                        ncol=1,
                        fontsize='x-small',
                        columnspacing=1)
    # grid
    stacked_bar2.xaxis.grid(False)

    # set title and placement
    stacked_bar2.text(0.5, 1.03,
                      title,
                      horizontalalignment='center',
                      transform=stacked_bar2.transAxes,
                      weight='bold')

    ####################
    # third chart
    # setup third chart
    sort_list = ['<= 2 hour',
                 '3-5 hours',
                 '6-10 hours',
                 '11-15 hours',
                 '16-20 hours',
                 '21-30 hours',
                 '31-40 hours',
                 '> 40 hours']

    agg_dict = {'less than 1 hour': '<= 2 hour',
                '1-2 hours': '<= 2 hour',
                '3-5 hours': '3-5 hours',
                '6-10 hours': '6-10 hours',
                '11-15 hours': '11-15 hours',
                '16-20 hours': '16-20 hours',
                '21-30 hours': '21-30 hours',
                '31-40 hours': '31-40 hours',
                'more than 40 hours': '> 40 hours'}
    df_plot = pd.DataFrame(columns=sort_list)
    interest = ['Hours per week']
    title = '(c) How many hours per week do \n you spend on labeling images?'



    # get data and transform to percentage values
    for counter, df in enumerate(dfs):
        df = df.replace({interest[0]: agg_dict})
        row_values = df[interest[0]].value_counts().reindex(sort_list).tolist()
        row_values = pd.Series(row_values).fillna(0).tolist()
        sum_r = sum(row_values)
        row_values_perc = [100 * x / sum_r for x in row_values]
        df_plot.loc[name[counter]] = row_values_perc

    # create plot
    df_plot = df_plot.T
    pie2, pie3 = df_plot.plot.pie(subplots=True, legend=False, colormap=cmap, labeldistance=None, ax=(ax2, ax3))
    pies = [pie2, pie3]

    for pie in pies:
        pie.set_xlabel(pie.get_ylabel())
        pie.set_ylabel('')

    # modify legend
    handles, labels = pie2.get_legend_handles_labels()
    pie2.legend(handles, labels, bbox_to_anchor=(1.1, 0.85), loc='upper left', ncol=1, fontsize='x-small', columnspacing=1)
    pie3.legend().remove()

    # set title and placement
    pie2.text(1.45, .91, title,
              horizontalalignment='center',
              transform=pie2.transAxes,
              weight='bold')

    ####################
    # fourth chart
    # setup fourth chart
    sort_list = ['<1 year',
                 '[1, 1.5] years',
                 '[1.6, 2] years',
                 '[2.1, 2.5] years',
                 '[2.6, 3] years',
                 '>3 years']
    agg_dict = {'Less than 1 year': '<1 year',
                'Between 1 and 1.5 years': '[1, 1.5] years',
                'Between 1.6 and 2 years': '[1.6, 2] years',
                'Between 2.1 and 2.5 years': '[2.1, 2.5] years',
                'Between 2.6 and 3 years': '[2.6, 3] years',
                'Between 3.1 and 4 years': '>3 years',
                'Between 4 and 5 years': '>3 years',
                'Between 6 and 7 years': '>3 years',
                'Between 8 and 9 years': '>3 years',
                'More than 10 years': '>3 years'}
    df_plot = pd.DataFrame(columns=sort_list)
    interest = ['How many years?']
    title = '(d) How long have you been \n labeling for?'


    # get data and transform to percentage values
    for counter, df in enumerate(dfs):
        df = df.replace({interest[0]: agg_dict})
        row_values = df[interest[0]].value_counts().reindex(sort_list).tolist()
        row_values = pd.Series(row_values).fillna(0).tolist()
        sum_r = sum(row_values)
        row_values_perc = [x / sum_r for x in row_values]
        df_plot.loc[name[counter]] = row_values_perc


    # create plot
    df_plot = df_plot.T
    pie5, pie6 = df_plot.plot.pie(subplots=True, colormap=cmap, labeldistance=None, ax=(ax5, ax6))
    pies = [pie5, pie6]

    for pie in pies:
        pie.set_xlabel(pie.get_ylabel())
        pie.set_ylabel('')

    # modify legend
    handles, labels = pie5.get_legend_handles_labels()
    pie5.legend(handles, labels, bbox_to_anchor=(1.05, 0.8), loc='upper left', ncol=1, fontsize='x-small', columnspacing=2)
    pie6.legend().remove()

    # set title and placement
    pie5.text(1.45, .91, title,
              horizontalalignment='center',
              transform=pie5.transAxes,
              weight='bold')

    # show complete figure
    stacked_bar.figure.show()

    # safe figure
    figure_path = os.path.join(os.path.normpath(safe_loc), safe_date + '_' + title_png + '.png')
    stacked_bar.figure.savefig(figure_path,
                               bbox_inches='tight', dpi=300)
    print(f'The generated figure is located at {os.path.abspath(figure_path)}')