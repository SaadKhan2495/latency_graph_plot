# Usage

- Copy the raw_stats file (txt file which contains only the numbers) into the repo.
- Run the python script using the following command

```python3
python3 plot_graph.py raw_stats_txt_file display_graph
```

Value of display_graph should be either 0 or 1. 1 displays the graph at end of script whereas 0 doesn't display the graph.

Once the script is executed, a folder with same name as the raw_stats_txt file will be generated which will contain all files (i.e graph_png_image, histogram file, sorted_data and graph_plot_data ) related to that specific run.
