import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.ticker as ticker
from _nat_mach_int_statistic_helpers import adjust_box_widths, colors, dict_image_package_with_image_names

'''
Goal: Generates a figure for each image category where the metric values 
are depicted per company and per stage. 
If manuscript_mode = True, only the figures of the manuscript will be generated. 
'''

### Config ###
title_file = 'metric_scores_on_instrument_level'
file_prefix = '2022-01-18_figure_appendix_for_category_'
metric = 'DSC_tool'  # insert metric of choice
show_only_annotate = True
csv = '../data_results/_tables_/2021-12-08_labeling_instructions_table_v1.0.csv'
save_path = '../data_results/figures'
companies = ['Company 1', 'Company 2', 'Company 3', 'Company 4', 'MTurk']
manuscript_mode = True


# Global Styling
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

# assign relevant keys
if manuscript_mode:
    keys = ('01_chaos', '05_simple')
else:
    key = dict_image_package_with_image_names

for key in keys:
    title = key + '_' + title_file
    images_in_the_package = dict_image_package_with_image_names[key]
    df = pd.read_csv(os.path.normpath(csv))
    df = df[df['Image_name'].isin(images_in_the_package)]

    df = df[df['QA'] == 'annotate']
    if 'img' in metric:
        df = df[(df['Instance_ID'] == 1)]
        print("table reduced to only images")
    fig = plt.figure(figsize=(3.5, 4))

    boxplot = sns.boxplot(y=metric, x='Company', data=df, palette=colors, hue='Stage',
                          hue_order=['first', 'second', 'third'], linewidth=2, fliersize=0)
    stripplot = sns.stripplot(y=metric, x='Company', data=df, palette=colors, alpha=0.5, hue='Stage',
                              hue_order=['first', 'second', 'third'], dodge=True, s=2)

    adjust_box_widths(fig, 0.83)

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

    labelx = boxplot.xaxis.get_label_text()
    boxplot.set_xlabel(labelx, loc='left')

    labely = boxplot.yaxis.get_label_text()
    if 'tool' in labely:
        labely = 'DSC per instrument'
    if 'img' in labely:
        labely = 'DSC per image'
    boxplot.set_ylabel(labely)

    # boxplot.legend([],[], frameon=False)
    boxplot.legend(handles[0:3], ['text minimal', 'text extended', 'picture'], bbox_to_anchor=(-0.19, -0.14),
                   loc='upper left', ncol=3, fontsize='x-small')
    boxplot.yaxis.set_major_locator(ticker.FixedLocator([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
    boxplot.set_xlabel('')

    # locs, labels = boxplot.xticks()  # Get the current locations and labels.
    boxplot.set_xticklabels(['Comp. \n 1', 'Comp. \n 2', 'Comp. \n 3', 'Comp. \n 4', 'MTurk'])
    boxplot.set_title('')

    # save file
    boxplot.figure.show()
    print(f"For category{key}:")
    figure_path = os.path.join(os.path.normpath(save_path), file_prefix + title + '.png' )
    boxplot.figure.savefig(figure_path, dpi=300, bbox_inches='tight')
    print(f'The generated figure is located at {os.path.abspath(figure_path)}')