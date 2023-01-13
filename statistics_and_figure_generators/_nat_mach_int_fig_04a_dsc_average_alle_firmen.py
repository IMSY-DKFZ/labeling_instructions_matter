import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.ticker as ticker
from _nat_mach_int_statistic_helpers import adjust_box_widths, colors

'''
Goal: Generates a figure with an overview of the DSC metric scores
per stage and grouped by the companies.
'''

##############
### Config ###
metric = 'DSC_img'  # 'Whole_image_instance_DSC' #Single_instrument_DSC
date = '2022-01-18'

# Global Styling
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

fig = plt.figure(figsize=(8, 3))
title = 'figure_4_first_part_dsc_scores_per_company_and_stage'
csv = '../data_results/_tables_/2021-12-08_labeling_instructions_table_v1.0.csv'
save_path = '../data_results/figures'
companies = ['Company 1', 'Company 2', 'Company 3', 'Company 4', 'MTurk']
##############

# initiate df
df = pd.read_csv(os.path.normpath(csv))
df.sort_values(by=['Company'], inplace=True)
print('vorher', df.shape)
df = df[(df['QA'] == 'annotate')]
print('nach QA', df.shape)

if 'img' in metric:  # reduce
    df = df[(df['Instance_ID'] == 1)]
    print("table reduced to only images")

print('nach redu', df.shape)

boxplot = sns.boxplot(y=metric, x='Company', data=df, palette=colors, hue='Stage',
                      hue_order=['first', 'second', 'third'], linewidth=2, fliersize=0)
stripplot = sns.stripplot(y=metric, x='Company', data=df, palette=colors, alpha=0.5, hue='Stage',
                          hue_order=['first', 'second', 'third'], dodge=True, s=2)

# style plot
adjust_box_widths(fig, 0.94)

for index, line in enumerate(boxplot.get_lines()):
    i = index % 18
    if i < 6:
        line.set_color(colors['first'])
    elif i < 12:
        line.set_color(colors['second'])
    elif i < 18:
        line.set_color(colors['third'])

for box in boxplot.artists[0::3]:
    box.set_edgecolor(colors['first'])
for box in boxplot.artists[1::3]:
    box.set_edgecolor(colors['second'])
for box in boxplot.artists[2::3]:
    box.set_edgecolor(colors['third'])

for patch in boxplot.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, .4))

boxplot.set_title(title.replace('_', ' '))

# define legend
handles, labels = boxplot.get_legend_handles_labels()
replace_dict = {'first': 'first stage', 'second': 'second stage', 'third': 'third stage'}
for counter, label in enumerate(labels):
    labels[counter] = replace_dict[label]

# modify x axis
labelx = boxplot.xaxis.get_label_text()
boxplot.set_xlabel('', loc='left')

# modify y axis
labely = boxplot.yaxis.get_label_text()
labely = labely.replace('_', ' ')
boxplot.set_ylabel(labely)

boxplot.legend(handles[0:3], ['text minimal', 'text extended', 'picture'], bbox_to_anchor=(0.25, -0.09),
               loc='upper left', ncol=3, fontsize='x-small')
boxplot.yaxis.set_major_locator(ticker.FixedLocator([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))

# safe file
boxplot.figure.show()
figure_path = os.path.join(os.path.normpath(save_path), date + '_' + title + '.png')
boxplot.figure.savefig(figure_path, dpi=300, bbox_inches='tight')
print(f'The generated figure is located at {os.path.abspath(figure_path)}')
