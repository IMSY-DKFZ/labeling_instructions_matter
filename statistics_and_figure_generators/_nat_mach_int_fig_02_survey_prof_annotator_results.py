import os.path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from cmcrameri import cm
import warnings
from _nat_mach_int_statistic_helpers import get_continuous_cmap

'''
Goal: Generates a figure with results from the professional annotator survey.
'''

### Config ###
csv = '../data_results/_tables_/survey_anonymized.csv'
safe_path = '../data_results/figures'
figure_name = 'figure_2_survey_prof_annotators_results'
save_date = '2022-04-26'

# Styling settings
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})
sns.set_style("whitegrid")


# initiate df
df = pd.read_csv(os.path.normpath(csv))
df = df[df['Entry'] == 'x']

# define colors
colors_coding_statements = ['#000000',
                            '#aa1529',
                            '#eb9072',
                            '#e5eef3',
                            '#7ab6d6',
                            '#1E60A4']
colors = ['#D41159', '#1A85FF']
cmap = get_continuous_cmap(colors)
cmap_2 = cm.batlow

# initiate figure with subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={'width_ratios': [2, 2]})

#######################
# overview chart first#
df_plot = pd.DataFrame(columns=['Do not understand statement', 'Never', 'Rarely', 'Sometimes', 'Often', 'Always'])
sort_list = ['Do not understand statement',
             'Never',
             'Rarely',
             'Sometimes',
             'Often',
             'Always']
interest = [
    'Pictures improve understanding?',
    'Extended text improves understanding?',
    'Unclear instructions cause rework?',
    'Unclear instructions cause delay?']
title = '(a) Annotation-related statements'


for col in interest:
    row_values = df[str(col)].value_counts().reindex(sort_list).tolist()
    if len(row_values) == 5 or row_values[0] == np.nan:
        row_values.insert(0, 0)
    row_values = np.nan_to_num(row_values)
    sum_r = sum(row_values)
    row_values_perc = [100 * x / sum_r for x in row_values]
    df_plot.loc[col] = row_values_perc
df_plot.index = df_plot.index.map(lambda x: x[:len(x) - 10])

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    stacked_bar = df_plot.plot.barh(stacked=True, color=colors_coding_statements, ax=axs[0])
    stacked_bar.set_yticklabels(interest, ha='left', verticalalignment='baseline')
    stacked_bar.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())

    dx = 40 / 72.;
    dy = 15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)

    # apply offset transform to all x ticklabels
    for label in stacked_bar.yaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    # modify legend
    handles, labels = stacked_bar.get_legend_handles_labels()
    stacked_bar.legend(handles,
                       labels,
                       bbox_to_anchor=(-0.001, -0.08),
                       loc='upper left',
                       ncol=3,
                       fontsize='x-small')

    # grid
    stacked_bar.yaxis.grid(False)

    # set title and placement
    stacked_bar.text(0.5, 1.03,
                     title,
                     horizontalalignment='center',
                     transform=stacked_bar.transAxes,
                     weight='bold')

    ###########################################
    # bar chart problems daily annotation work#
    df_plot = pd.DataFrame(columns=['Training', 'Instructions', 'Tooling', 'Data', 'Concentration', 'Infrastructure'])
    conds = [
        'Unclear labeling instructions / Unclear labeling guide',
        'Concentration issues (due to monotonous work)',
        'Poor data (e.g. image quality or sensor fusion)',
        'Tooling issues / Tooling restrictions (e.g. not able to save annotations)',
        'Missing training',
        'Infrastructure']
    title_barplot = '(b) Problem causes in the daily annotation work'
    row = []
    for cond in conds:
        amount = sum(df['What causes problem in the annotation work?'].str.contains(cond, regex=False) / 298 * 100)
        row.append(amount)

    df_plot.loc[len(df_plot)] = row
    barplot = df_plot.plot.bar(ax=axs[1], cmap=cmap_2)
    barplot.set_xticklabels([])
    barplot.set_xlabel('')
    barplot.legend(['Instructions', 'Concentration', 'Data', 'Tooling', 'Training', 'Infrastructure'], )
    barplot.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())

    # modify legend
    handles, labels = barplot.get_legend_handles_labels()
    barplot.legend(handles, ['Instructions', 'Concentration', 'Data', 'Tooling', 'Training', 'Infrastructure'],
                   bbox_to_anchor=(0, -0.02), loc='upper left', ncol=3, fontsize='x-small')

    # set title and placement
    barplot.text(0.5,
                 1.03,
                 title_barplot,
                 horizontalalignment='center',
                 transform=barplot.transAxes,
                 weight='bold')

    # grid
    barplot.xaxis.grid(False)

    # safe figure
    stacked_bar.figure.show()
    figure_path = os.path.join(os.path.normpath(safe_path), save_date + '_' + figure_name + '.png')
    stacked_bar.figure.savefig(figure_path, bbox_inches='tight', dpi=300)
    print(f'The generated figure is located at {os.path.abspath(figure_path)}')