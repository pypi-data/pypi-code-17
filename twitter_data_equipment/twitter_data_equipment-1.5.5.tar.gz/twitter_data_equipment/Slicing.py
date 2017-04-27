"""
Takes a Csv-File and splits it up into a specified number of time-windows. Creates Csv-Files for each window and saves
them into older 'Csv-Slices'.
Contains two methods: slice_dataset and create_overview. Create overview should only be called after slice_dataset has
been called at least once.
"""

import os
import pandas as pd
import pytz
from twitter_data_equipment.GraphFactory import GraphFactory


def slice_dataset(input_path, number_of_ranges):
    """
    Slices up the Csv-File from the given path into specified number of windows. The windows have an overlap of a third 
    of the timerange each window has
    
    :param str input_path: Path to Csv-File
    
    :param int number_of_ranges: Number of windows and Csv-Files that should be generated
        
    """

    print('Creating Directories')

    # Create all neccessary directories
    try:
        dir_name = os.path.dirname(input_path)
        path_name_csv = os.path.join(dir_name, 'Csv_Slices')
        os.makedirs(path_name_csv, exist_ok=True)
        path_name_graphml = os.path.join(dir_name, 'Slices_Graphml')
        os.makedirs(path_name_graphml, exist_ok=True)
        path_name_png = os.path.join(dir_name, 'Slices_PNG')
        os.makedirs(path_name_png, exist_ok=True)
        path_name_info = os.path.join(dir_name, 'Slices_Info')
        os.makedirs(path_name_info, exist_ok=True)
    except:
        print('Problem Creating Folders...Exiting')
        exit(1)

    print('Loading CSV ... ')

    # Load Csv-File
    df = pd.read_csv(input_path)

    # Create index over time
    df.set_index(pd.DatetimeIndex(df['created_at'], tz=pytz.UTC), inplace=True)

    # Sort index
    df.sort_index(inplace=True, ascending=True)

    # Evaluate length of time slices
    first = df.first_valid_index()
    last = df.last_valid_index()
    date_range = pd.date_range(first, last, freq='1S', tz=pytz.UTC)
    number_of_slices = number_of_ranges
    period = int(round(len(date_range) / number_of_slices, 0))
    third_of_period = int(round(period / 3, 0))
    run = 0
    list_of_ranges = []

    print('Creating ' + str(number_of_ranges) + ' time ranges ...')

    # Evaluate start and end-points for each time-slice
    while run <= len(date_range):
        if run - third_of_period < 0:
            list_of_ranges.append((date_range[run], date_range[run + period]))
        else:
            if not run + period > len(date_range):
                list_of_ranges.append((date_range[run], date_range[run + period]))
            else:
                list_of_ranges.append((date_range[run], date_range[len(date_range) - 1]))
                break
        run += period - third_of_period

    print('Creating CSV-Slices ...')

    # Create time slices from Csv-Input-File
    for (start, end) in list_of_ranges:
        df_temp = df[start:end]
        name_of_slice = str(start) + ' - ' + str(end) + ".csv"
        total_name = os.path.join(path_name_csv, name_of_slice)
        df_temp.reset_index(inplace=True, drop=True)
        df_temp.to_csv(open(total_name, 'w'), index=False)


def create_overview(input_path,node_degree_threshold = 100,edge_weight_minimum = 0, graph_identifier = 'QT',
                    draw_edges = True,
                    ):
    """
    Procedure to produce several overview files out of a given Csv-File containing tweet-data.
    Generates:
    
    - Graph-file according to graph_identifier and saving it in the folder 'Slices_Graphml'
    
    - PNG-File plotting graph to 'Slices_PNG' 
    
    - TXT-File containing information on the graph and its communities and saving it in the folder 'Slices-Info'
    
    
    :param str input_path: Path to directory containing folder of Csv-Files.
    
    :param int node_degree_threshold: Percentage of nodes that should be kept in the graph, after pruning them by the degree of the node
    
    :param int edge_weight_minimum: Minimum weight each node in th graph should have to be kept
    
    :param str graph_identifier: Defines what graph should be drawn on the file. Can be either 'hashtag', 'QT' or 'RT'
    
    :param boolean draw_edges: Should the edges on the graph be drawn or not
    
    """
    print('Creating Graphml, CSV, PNG and Info-Files ...')

    # Get path to CSV-Slices-Folder from input path
    path_name_csv = os.path.join(input_path, 'Csv_Slices')
    for filename in os.listdir(path_name_csv):
        if filename.endswith('csv'):

            # Get filename of Csv-File
            total_file_dest = os.path.join(path_name_csv, filename)

            # Instantiate GraphFactory
            gf = GraphFactory(str(filename))

            # Create a graph according to graph_identifier
            gf.create_graphs_from_dataframe(graph_identifier, total_file_dest)

            # Change directory
            total_file_dest = os.path.abspath(os.path.join(path_name_csv, os.pardir))
            total_file_dest = os.path.join(total_file_dest, 'Slices_Graphml')
            temp = os.path.join(total_file_dest, filename.rstrip('.csv') + '.graphml')

            # Prune graph according to specified parameters
            gf.prune_graph(edge_weight=edge_weight_minimum, degree_thresh=0, weight_thresh=0, remove_isolates=False)
            threshold = gf.get_threshold(node_degree_threshold, 2, 'degree_thresh')
            gf.prune_graph(edge_weight=0, degree_thresh=threshold, weight_thresh=0, remove_isolates=True)

            # Write graph to graphml-file
            gf.write_graphml(temp)

            # Change directory
            total_file_dest = os.path.abspath(os.path.join(path_name_csv, os.pardir))
            total_file_dest = os.path.join(total_file_dest, 'Slices_PNG')
            temp = os.path.join(total_file_dest, filename.rstrip('.csv') + '.png')

            # Draw Graph according to specified parameters
            gf.draw_graph(temp, 100, 5, layout_algorithm='graphviz', draw_edges=draw_edges)

            # Change directory
            total_file_dest = os.path.abspath(os.path.join(path_name_csv, os.pardir))
            total_file_dest = os.path.join(total_file_dest, 'Slices_Info')
            temp = os.path.join(total_file_dest, filename.rstrip('.csv') + '.txt')

            # Write out graph and community information
            gf.write_out_community_user_info(temp)
