from django.shortcuts import render

from media.graph_1.files.growth_curve import growthCurve, growthCurve2
from .models import File
import pandas as pd
import matplotlib as plt1
import matplotlib.pyplot as plt, mpld3
import matplotlib.colors as mcolors  # Import Matplotlib colors

def home(request):
    if request.method == "POST":
        plt1.pyplot.switch_backend('Agg')
        file = request.FILES["myFile"]
        df = pd.read_excel(file)
        # Get unique values from the second column
        unique_values = df[df.columns[1]].unique()

        # Customize graph title and axes labels
        graph_title_prefix = 'X concentration (mM) '  # Prefix for the graph title
        x_label = 'time (h)'  # Replace with the desired x-axis label
        y_label = '$OD_{580}$'  # Replace with the desired y-axis label r'$OD_{580}$'

        # Extract x-axis values from the first row starting from the third column
        x_values = df.columns[2:]

        # Define a list of custom colors
        custom_colors = list(mcolors.TABLEAU_COLORS.values())  # Use Tableau colors

        # Calculate the number of rows and columns for subplots
        num_rows = (len(unique_values) + 1) // 2  # Round up division
        num_cols = 2

        # Create a single figure with subplots
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 10))

        # Initialize the maximum y-axis value
        max_y_value = 0

        for idx, value in enumerate(unique_values):
            row_idx = idx // num_cols
            col_idx = idx % num_cols
            ax = axes[row_idx, col_idx]

            # Filter data for the current unique value
            value_data = df[df[df.columns[1]] == value]

            # Grouping by the first column (group names)
            grouped_data = value_data.groupby([df.columns[0], df.columns[1]])

            # Calculate the means and standard deviations for each group
            mean_values = grouped_data.mean()
            std_values = grouped_data.std()

            for group_names, group_means in mean_values.iterrows():
                group_stds = std_values.loc[group_names]

                # Update the maximum y-axis value
                max_y_value = max(max_y_value, max(group_means + group_stds))

                # Use x_values for the x-axis
                ax.errorbar(x=x_values, y=group_means, yerr=group_stds, label=str(group_names))

            ax.set_title(graph_title_prefix + str(value))
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

            # Set the axes limits to start with 0 and stop at 24 and use the maximum y-value
            ax.set_xlim(left=0, right=24)
            ax.set_ylim(bottom=0, top=max_y_value)

            # Set the x-axis ticks
            ax.set_xticks(range(0, 25, 4))  # Adjust the step as needed

        # Create a single legend for all subplots
        handles, labels = ax.get_legend_handles_labels()
        new_labels = []
        for label in labels:
            label = label[1:-1].split(',')[0][1:-1]
            new_labels.append(label)

        legend = fig.legend(handles, new_labels, loc='lower right')

        # Remove the last subplot (empty graph)
        fig.delaxes(axes[-1, -1])

        # Adjust the position of the legend
        fig.canvas.draw()
        legend.set_bbox_to_anchor((0.85, 0.18))  # Position the legend in the center of the right edge of the figure

        plt.tight_layout()
        mpld3.show()

        return render(request, "graph_1/home.html", {"something": True, "file": file})
    files = File.objects.all()
    return render(request, "graph_1/home.html", {"files": files})
