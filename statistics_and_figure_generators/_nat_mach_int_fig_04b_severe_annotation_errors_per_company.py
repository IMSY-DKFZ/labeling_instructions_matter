import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from _nat_mach_int_statistic_helpers import adjust_box_widths, colors

'''
Goal: Generates a figure with an overview of the invalid annotations
per stage and grouped by the companies.
!Use stats scripts "_nat_mach_int_stats_*" prior to running this script.
The "_nat_mach_int_stats_*" scripts generate relevant tables.
'''

##############
### Config ###
metric = 'severe_errors'  # 'Whole_image_instance_DSC' #Single_instrument_DSC
date = '2022-01-25_severe_errors'


# Global Styling
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

### Config ###
title = 'figure_4_second_part_invalid_annotations_per_company_and_stage'
csv = '../data_results/_tables_/2022-01-18_Overview_severe_annotation_errors_per_provider_and_stage.csv'
save_path = '../data_results/figures'
companies = ['Company 1', 'Company 2', 'Company 3', 'Company 4', 'MTurk']
##############

# initate figure
fig = plt.figure(figsize=(8, 2))

# initiate df
df = pd.read_csv(os.path.normpath(csv))
df.sort_values(by=['Company'], inplace=True)
df = df[df['Company'].isin(companies)]

# initiate plot
boxplot = sns.barplot(y=metric,
                      x='Company',
                      data=df,
                      palette=colors,
                      hue='Stage',
                      hue_order=['first', 'second', 'third'],
                      linewidth=2)

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

# style title
boxplot.set_title('')

# define legend
handles, labels = boxplot.get_legend_handles_labels()
replace_dict = {'first': 'first stage',
                'second': 'second stage',
                'third': 'third stage'}
for counter, label in enumerate(labels):
    labels[counter] = replace_dict[label]

# modify x axis
labelx = boxplot.xaxis.get_label_text()
boxplot.set_xlabel('', loc='left')

# modify y axis
labely = boxplot.yaxis.get_label_text()
labely = labely.replace('_', ' ').capitalize()
boxplot.set_ylabel(labely)

# modify legend
boxplot.get_legend().remove()

# safe figure
boxplot.figure.show()
figure_path = os.path.join(os.path.normpath(save_path), date + title + '.png')
boxplot.figure.savefig(figure_path, dpi=300, bbox_inches='tight')
print(f'The generated figure is located at {os.path.abspath(figure_path)}')