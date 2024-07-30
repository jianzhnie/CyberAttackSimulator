"""Plot showing as singular or multiple the results of the extension
exploration."""

import glob
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.getcwd())
from nasimulator.utils.df_utils import get_summary_statistics, process_df
from nasimulator.utils.plotting_utils import \
    plot_multi_extension_comparison_size


def main():
    # staging
    current_dir = os.getcwd()
    figures = os.path.join(current_dir, 'work_dir', 'figures')
    figure_name = os.path.join(figures, 'summary_plot_extensions.png')
    data_dir = os.path.join(current_dir, 'work_dir', 'results_data')
    plt.style.use(
        os.path.join(current_dir, 'nasimulator/utils/figure_style.mplstyle'))

    network_size = ['18', '50', '100']

    # load all the agents data
    all_files = glob.glob(data_dir + r'\agents_*.csv')

    # load the random agent
    random_data = pd.read_csv(os.path.join(
        data_dir, 'random_agents_performances_training.csv'),
                              header=0)

    print(random_data)
    # Plotting order
    order = [
        'noscenario',
        'compromise',
        'isolate',
        'mix',
        'low_connection',
        'high_connection',
        'low_red',
        'high_red',
    ]
    order_label = [
        'standard',
        'compromise',
        'isolate',
        'mix',
        '-edges',
        '+edges',
        'low-skill',
        'high-skill',
    ]
    algorithm_order = ['std', 'df075', 'lr001']

    # generate the location for the datapoints
    xlocs = [i * 3 + 1 for i in range(24)]
    xlow, xmid, xhigh = [], [], []
    for i in xlocs:
        xlow.append(i - 0.3)
        xmid.append(i - 0.0)
        xhigh.append(i + 0.3)

    # create the full summary to pass
    full_summary = {}

    for item in order:  # loop on the various items
        for index, i in enumerate(all_files):  # loop in the data
            if item in i:
                data = pd.read_csv(i, header=0)  # load the data

                cleaned = process_df(data)  # clean the df
                new_df = cleaned.drop(columns='model').copy()  # process the df

                sum_stat = get_summary_statistics(new_df)
                full_summary[item] = sum_stat

    # Call the plotter
    plot_multi_extension_comparison_size(
        network_size,
        order,
        algorithm_order,
        order_label,
        full_summary,
        random_data,
        xlow,
        xmid,
        xhigh,
    )

    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
    plt.savefig(figure_name)


if __name__ == '__main__':
    main()
