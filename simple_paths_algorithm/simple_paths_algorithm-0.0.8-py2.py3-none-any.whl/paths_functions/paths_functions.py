import pandas as pd
import networkx as nx
import numpy as np

def get_node_edge_data(nodes, edges, header=False):
    '''
    inputs:

    nodes, edges - csv or dataframe (headers optional):
        nodes need to be integers, node names can be any format
    header - if csv contains header (boolean)
    -------
    returns:
        dataframe in same format as csv inputs

    format of nodes:
    |Node|Node text name|

    format of edges:
    |Node A|value of A|Node B|value of B|
    '''

    if header is True:
        header = 0
    else:
        header = None

    if isinstance(nodes, str):
        nodes_df = pd.read_csv(nodes, header=header)
    elif isinstance(nodes, pd.DataFrame):
        nodes_df = nodes
    else:
        raise TypeError('node variable can only be path to csv or pandas dataframe')

    if isinstance(edges, str):
        edges_df = pd.read_csv(nodes, header=header)
    elif isinstance(edges, pd.DataFrame):
        edges_df = edges
    else:
        raise TypeError('node variable can only be path to csv or pandas dataframe')

    # rename cols
    edges_df.columns = ['node_a', 'a_value', 'node_b', 'b_value']
    nodes_df.columns = ['node', 'node_text']

    return nodes_df, edges_df

def get_node_edge_lists(node_df, edge_df):
    '''
    inputs:
        node and edge dataframe, format specifed in get_node_edge_data
    ---------
    returns:
        node_list - list of integers
        edge_tuple_list - list of tuples where each tuple is an edge of origin and
            terminal node
    '''

    node_list = [int(node) for node in node_df.node.tolist()]

    # construct tuple list
    edge_tuple_list = []
    for _, edge in edge_df.iterrows():
        # if tie then 2 edges will be added in either direction
        if edge.a_value == edge.b_value:
            edge_tuple_list.append((edge.node_a, edge.node_b))
            edge_tuple_list.append((edge.node_b, edge.node_a))
        elif edge.a_value > edge.b_value:
            edge_tuple_list.append((edge.node_a, edge.node_b))
        else:
            edge_tuple_list.append((edge.node_b, edge.node_a))

    return node_list, edge_tuple_list

# make function that creates the graph from the csv
def get_graph(nodes, edges, header=False):
    '''
    inputs:
        nodes, edges - csv or dataframe

        format of nodes:
        |Node|Node text name|

        format of edges:
        |Node A|value of A|Node B|value of B|

        header - if csv, specify if csv has a header
    -------
    returns:
        di_graph - directed graph, using networkx
        node_df - dataframe of nodes, see get_node_edge_data for format
    '''

    # load in csvs
    node_df, edge_df = get_node_edge_data(nodes, edges, header)
    # get node and edge lists
    node_list, edge_list = get_node_edge_lists(node_df, edge_df)

    # create graph and add attributes
    di_graph = nx.DiGraph()
    di_graph.add_nodes_from(node_list)
    di_graph.add_edges_from(edge_list)

    return di_graph, node_df

def get_node_simple_paths(graph, nodes, starting_node, depth):
    '''
    inputs:
        graph - directed graph, networkx object
        nodes - list of nodes to get paths for (all nodes in graph)
        starting_node - node for which paths are generated
        depth - maximum length of simple path
    -------
    returns:
        list of list where each list is a simple path from the starting_node,
        there will be len(nodes) - 1 elements in list
    '''

    node_paths_list = []

    for node in nodes:
        # we dont want the simple paths from origin node to itself so continue
        if node == starting_node:
            continue
        else:
            paths_temp = nx.all_simple_paths(graph, starting_node, node, cutoff=depth)
            node_paths_list += list(paths_temp)

    return node_paths_list

# change this function to return dictionary
def get_node_weights(graph, list_of_nodes):
    '''
    inputs:
        graph - directed networkx graph object
        list_of_nodes - list of nodes in graph
    -------
    returns:
        weight_dict - dictionary of node weights, format {node: node weight}
    '''

    node_all_dict = graph.degree(list_of_nodes)

    weight_dict = {}

    for i in node_all_dict:
        node_weight = 1 / float(node_all_dict[i])
        weight_dict[i] = node_weight

    return weight_dict

def get_node_score(node_paths_list, weight_dict):
    '''
    inputs:
        node_paths_list - list of lists of node paths from origin node_paths_list
        weight_dict - dictionary of weights of all nodes, format {node: node weight}
    --------
    returns:
        node_value - score of simple_path_algorithm for node (float)
    '''

    node_value = 0
    for path in node_paths_list:
        temp_path_value_list = []
        for i in range(len(path) - 1):
            temp_path_value_list.append(weight_dict[path[i]])

        node_value += np.prod(temp_path_value_list)

    return node_value

# make function to return dataframe
def get_graph_score(graph, depth):
    '''
    inputs:
        graph - directed networkx graph object
        depth - maximum length of simple path
    -------
    returns:
        node_score_df - dataframe of simple_path scores for all nodes
            in graph, format: |node|node score|
    '''

    node_list = graph.nodes()
    # get weight for each node
    node_weights = get_node_weights(graph, node_list)

    node_info_list = []

    for node in node_list:
        # get paths for node
        node_paths_list = get_node_simple_paths(graph, node_list, node, depth)
        #get score for node
        node_score = get_node_score(node_paths_list, node_weights)

        node_info_list.append([node, node_score])

    node_score_df = pd.DataFrame(node_info_list, columns=['node', 'node_score'])

    return node_score_df

def get_simple_paths_result(nodes, edges, depth, csv=False, header=False):
    '''
    inputs:
        nodes, edges - csv or dataframe

        format of nodes:
        |Node|Node text name|

        format of edges:
        |Node A|value of A|Node B|value of B|

        depth - maximum length of simple path

        csv - save results as csv (boolean)
        header - does csv of dataframe contain header (boolean)
    ------
    returns:
        results_df - dataframe of final results
        format:
            |node|node_text|node_score|
    '''

    graph, nodes_df = get_graph(nodes, edges, header)
    scores_df = get_graph_score(graph, depth)
    results_df = pd.merge(nodes_df, scores_df, on='node', how='left')
    # save results to csv
    if csv is True:
        results_df.to_csv('simple_paths_algo_results.csv', index=False)

    return results_df
    