import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.ticker as ticker
from _nat_mach_int_statistic_helpers import colors, colors_provider_type

'''
Goal: Generates an overview of the DSC metric scores
per stage and grouped by the companies.
Each stage is a separate figure.
'''

# Style Setting
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

### Config ###
metric = 'DSC_img'  # alternatives: 'Whole_image_instance_DSC' #Single_instrument_DSC
date = '2022-02-09'
title = 'figure_1_scores_per_labeling instruction_stage'
csv = '../data_results/_tables_/2021-12-08_labeling_instructions_table_v1.0.csv'
save_path = '../data_results/figures'
companies = ['Company 1', 'Company 2', 'Company 3', 'Company 4', 'MTurk']
label_y = 'DSC'
stages = ["first", "second", "third"]



# initate table and reduce to relevant data points
df = pd.read_csv(os.path.normpath(csv))
df.sort_values(by=['Stage'], inplace=True)
print('vorher', df.shape)
df = df[(df['QA'] == 'annotate')]
print('nach QA', df.shape)

if 'img' in metric:
    df = df[(df['Instance_ID'] == 1)]
    print("table reduced to only images")

# check for correct size
print('nach redu', df.shape)

for stage in stages:

    # initiate new figure
    fig = plt.figure(figsize=(3, 5))

    df_stage = df[(df['Stage'] == stage)]
    df_stage = df_stage.sort_values(by='Company')

    # create plots
    boxplot = sns.boxplot(y=metric, x='Company', data=df_stage, color=colors[stage], linewidth=2, fliersize=0)
    stripplot = sns.stripplot(y=metric, x='Company', data=df_stage, palette=colors_provider_type, alpha=0.5, dodge=True,
                              s=1)

    # modify coloring of the lines (does not include the lines of the box itself)
    for index, line in enumerate(boxplot.get_lines()):
        i = index
        line.set_color(colors[stage])

    # modify coloring of the box lines
    for box in boxplot.artists:
        box.set_edgecolor(colors[stage])

    # modify coloring of the patches
    for patch in boxplot.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor(colors[stage])
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .4))

    # define legend
    handles, labels = boxplot.get_legend_handles_labels()

    # modify x axis
    labelx = boxplot.xaxis.get_label_text()
    boxplot.set_xlabel('', loc='left', )
    plt.xticks(rotation=90)

    # modify y axis
    labely = boxplot.yaxis.get_label_text()
    labely = labely.replace('_', ' ')
    boxplot.set_ylabel(label_y)
    boxplot.yaxis.set_major_locator(ticker.FixedLocator([0, 0.5, 1]))

    # boxplot.get_legend().remove()

    # save file
    filename = date + '_' + title + '_' + stage + '.png'
    fig.tight_layout()
    figure_path = os.path.join(os.path.normpath(save_path), filename)
    boxplot.figure.show()
    boxplot.figure.savefig(figure_path, dpi=300, bbox_inches='tight')
    print(f'The generated figure is located at {os.path.abspath(figure_path)}')