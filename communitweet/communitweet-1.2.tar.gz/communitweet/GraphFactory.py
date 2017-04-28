"""
A Factory to handle and cluster all networkx-based graph activities. Contains methods for creating, pruning, 
plotting and information-gathering.
"""

import itertools
import operator
from collections import OrderedDict
from itertools import islice
from multiprocessing import Pool
import community
import matplotlib

matplotlib.use('Agg')
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.drawing.nx_agraph import graphviz_layout
from communitweet.ForceAtlas2 import *
from communitweet.Summarize import *

class GraphFactory:
    """
    GraphFactory-Class contains all relevant class-variables and methods. Represents a nx.Graph()-object
    """
    def __init__(self, name_of_graph):
        """
        Initializes graph and gives name to graph
        
        :param str name_of_graph: Name of graph needs to be specified here
        
        """
        print('Start Creating Graph "' + name_of_graph + '"')
        self.graph = nx.Graph()
        self.name_of_graph = name_of_graph
        self.pruning_information = self._PruningInfo()
        self.community_partitions = dict()
        self.dataframe = None

    def add_node(self, node, label):
        """
        Method to add node and its label to the graph-object. Handles increasing of 'weight' attribute of each node
        automatically each time a node gets added multiple times
        
        :param int node: Node in the form of a twitter user-id or a hashtag
        
        :param str label: Label of node, either screen_name of a user or the name of the hashtag
        
        """
        node = int(node)
        label = str(label)
        if not self.graph.has_node(node):
            self.graph.add_node(node, attr_dict={'weight': 1, 'label': label})
        else:
            self.graph.node[node]['weight'] += 1
            self.graph.node[node]['label'] = label

    def add_edge(self, node_1, label_1, node_2, label_2):
        """
        Method to add edge to the graph-object. Handles increasing of 'weight' attribute of each edge and the related 
        nodes automatically each time an edge gets added multiple times.
        
        :param int node_1: First node or edge start node
        
        :param str label_1: Label of first node
        
        :param int node_2: Second node or edge end node
        
        :param str label_2: Label of second node
        
        """
        node_1 = int(node_1)
        node_2 = int(node_2)
        label_1 = str(label_1)
        label_2 = str(label_2)

        if not self.graph.has_edge(node_1, node_2):
            if not self.graph.has_node(node_1):
                self.graph.add_node(node_1, attr_dict={'weight': 1, 'label': label_1})
            if not self.graph.has_node(node_2):
                self.graph.add_node(node_2, attr_dict={'weight': 1, 'label': label_2})
            self.graph.add_edge(node_1, node_2, attr_dict={'weight': 1})
        else:
            self.graph[node_1][node_2]['weight'] += 1

    def write_graphml(self, output_path):
        """
        Writes the graph-object to file in the form of a Graphml-File
        
        :param str output_path: Path to destination of Graphml-File
        
        """
        print("Writing Graph to " + str(output_path))
        nx.write_graphml(self.graph, output_path)

    def load_graph(self, input_path):
        """
        Loads a graph-object from a Graphml-File
        
        :param str input_path: path to Graphml-File
        
        """
        print("Loading Graph from " + str(input_path))
        with open(input_path) as inp:
            self.graph = nx.read_graphml(inp)

    def print_info(self):
        """
        Prints a short overview of the graph including the amount of nodes, edges, the average degree and the average 
        weight
        """
        print('--------------------------------------')
        print('Information on ' + '"' + self.name_of_graph + '"' + '-Graph')
        print('Number of nodes: ' + str(self.graph.number_of_nodes()))
        print('Number of edges: ' + str(self.graph.number_of_edges()))
        print('Average degree: ' + str(round(float(sum(self.graph.degree().values())) / float(self.graph.number_of_nodes()),2)))

        avg_sum = 0
        for _, data in self.graph.nodes(data=True):
            avg_sum += data['weight']

        print('Average weight: ' + str(round(float(avg_sum) / float(self.graph.number_of_nodes()),2)))
        print('--------------------------------------')

    def get_threshold(self, total_percentage_of_nodes_remaining, blur, name_of_measure):
        """
        Calculates the threshold for a given name_of_measure such that, when specified measure is pruned according to 
        that threshold, the percentage of nodes remaining in the graph is equal to the parameter total_percentage_of_nodes_remaining.
        Calculated threshold is only right, when pruning option remove_isolated is applied separately.
        
        :param int total_percentage_of_nodes_remaining: Percentage of nodes to keep in the graph after pruning
        
        :param int blur: How many percentage-points can the threshold be wrong
        
        :param str name_of_measure: On what node measure should the algorithm be applied. So far only 'weight_thresh' or 'degree_thresh' are possible
        
        :return int: 
        """
        total_node_count = self.graph.number_of_nodes()
        if total_node_count == 0:
            return 0
        if name_of_measure == 'weight_thresh':
            temp_threshold = 2
            continue_eval = True
            nodes_to_remove = []

            error_count_minus = 0
            error_count_plus = 0
            while continue_eval:
                for node, data in self.graph.nodes(data=True):
                    if data['weight'] < temp_threshold:
                        nodes_to_remove.append(node)
                temp_remaining = 100 - len(nodes_to_remove) / total_node_count * 100
                if total_percentage_of_nodes_remaining + blur > temp_remaining > total_percentage_of_nodes_remaining - blur:
                    continue_eval = False
                elif total_percentage_of_nodes_remaining - blur < temp_remaining:
                    temp_threshold = temp_threshold + 1
                    error_count_plus += 1
                elif temp_remaining < total_percentage_of_nodes_remaining - blur:
                    temp_threshold = temp_threshold - 1
                    error_count_minus += 1
                if error_count_plus > 2 and error_count_minus > 2:
                    error_count_plus = 0
                    error_count_minus = 0
                    continue_eval = False
                nodes_to_remove = []
            return temp_threshold
        if name_of_measure == 'degree_thresh':
            temp_threshold = 2
            continue_eval = True
            nodes_to_remove = []

            error_count_minus = 0
            error_count_plus = 0
            while continue_eval:
                for node, data in self.graph.nodes(data=True):
                    if 'Degree' not in data:
                        print('Graph has no attribute "degree" - please use "add_stats"-function')
                        exit(1)
                    if data['Degree'] < temp_threshold:
                        nodes_to_remove.append(node)
                temp_remaining = 100 - len(nodes_to_remove) / total_node_count * 100
                if total_percentage_of_nodes_remaining + blur > temp_remaining > total_percentage_of_nodes_remaining - blur:
                    continue_eval = False
                elif total_percentage_of_nodes_remaining - blur < temp_remaining:
                    temp_threshold = temp_threshold + 1
                    error_count_plus += 1
                elif temp_remaining < total_percentage_of_nodes_remaining - blur:
                    temp_threshold = temp_threshold - 1
                    error_count_minus += 1
                if error_count_plus > 2 and error_count_minus > 2:
                    error_count_plus = 0
                    error_count_minus = 0
                    continue_eval = False
                nodes_to_remove = []
            return temp_threshold

    def prune_graph(self, edge_weight, degree_thresh, weight_thresh, remove_isolates):
        """
        Prunes the graph-object on the specified measurements.
        
        :param int edge_weight: minimum weight an edge can have to remain in the graph
        
        :param int degree_thresh: minimum degree an node can have to remain in the graph
        
        :param int weight_thresh: minimum weight an node can have to remain in the graph
        
        :param bool remove_isolates: should isolated nodes be removed?
        
        """
        print("Pruning Graph")
        print(".......... Removing self refering edges")

        if edge_weight != 0:
            self.pruning_information.edge_weight = edge_weight
        if degree_thresh != 0:
            self.pruning_information.node_degree = degree_thresh
        if weight_thresh != 0:
            self.pruning_information.node_weight = weight_thresh
        if remove_isolates:
            self.pruning_information.isolated = remove_isolates

        edges_to_remove = []
        for edge in self.graph.edges(data=True):
            if edge[0] == edge[1]:
                edges_to_remove.append(edge)
            if edge[2]['weight'] < edge_weight:
                edges_to_remove.append(edge)

        self.graph.remove_edges_from(edges_to_remove)
        print(".......... Removing nodes according to degree and weight")

        nodes_to_remove = []
        for node, data in self.graph.nodes(data=True):
            if data['weight'] < weight_thresh:
                nodes_to_remove.append(node)
            elif data['Degree'] < degree_thresh:
                nodes_to_remove.append(node)

        self.graph.remove_nodes_from(nodes_to_remove)

        if remove_isolates:
            print(".......... Removing isolated nodes")
            self.graph.remove_nodes_from(nx.isolates(self.graph))

        # components = sorted(nx.connected_component_subgraphs(self.graph),key=len,reverse=True)
        # self.graph = self.graph.subgraph(components[0:10],inplace=True)

        print("Pruning Done")

    class _PruningInfo():
        """
        Class to pack all the Information on the applied Pruning that has been done on current graph-object.
        """
        def __init__(self):
            """
            Sets all pruning-info to 0.
            """
            self.node_weight = 0
            self.node_degree = 0
            self.edge_weight = 0
            self.isolated = False

        def to_string(self):
            """
            Returns all the info contained in _PruningInfo in one string.
            """
            output = 'Minimum Edge Weight = ' + str(self.edge_weight) + '\n'
            output += 'Minimum Degree of Nodes = ' + str(self.node_degree) + '\n'
            output += 'Minimum Weight of Nodes = ' + str(self.node_weight) + '\n'
            output += 'Isolated Nodes were removed = ' + str(self.isolated)
            return output

    def add_stats(self, degree, closeness, betweenness):
        """
        Calculates measures and statistics such as degree, closeness and betweenness to the graph-object and to its
        nodes.
        
        :param bool degree: If set to true, the degree of each node is added as an attribute
        
        :param bool closeness: If set to true, the closeness of each node is added as an attribute
        
        :param bool betweenness: If set to true, the betweeness of each node is added as an attribute. ATTENTION: Takes a long time
        
        """
        print("Calculating Stats")
        if degree:
            print(".......... Degree")
            deg = self.graph.degree()
            nx.set_node_attributes(self.graph, 'Degree', deg)
        if closeness:
            print(".......... Closeness")
            close = nx.closeness_centrality(self.graph)
            nx.set_node_attributes(self.graph, 'Closeness_centrality', close)
        if betweenness:
            print(".......... Betweeness")
            betwe = calculate_betweenness(self.graph)
            nx.set_node_attributes(self.graph, 'Betweenness_centrality', betwe)
        print("Calculating Degree")

    def _get_communities(self):
        """
        Helper method to calculate communities with the help of the 'community'-package
        """
        self.community_partitions = community.best_partition(self.graph)

    def write_out_community_user_info(self, path_to_file):
        """
        Calculates communities - if not already done - and sorts each community by weight as well as all communities 
        by size, analyzes the graph and prints all information to TXT-file.
        The generated file contains information on the whole graph - including the top 10 hashtags, locations, urls and media-urls
        of all users of the graph as welll as of the users of each community.
        
        :param str path_to_file: Path to destination for Information-File.
        """
        print('Evaluating communites')
        if not self.community_partitions:
            self._get_communities()

        all_communities_sorted = dict()
        communities = set([comm for comm in self.community_partitions.values()])
        for comm in communities:
            temp_user_list = []
            for k, v in self.community_partitions.items():
                if v == comm:
                    temp_user_list.append(k)
            all_communities_sorted[comm] = temp_user_list

        # sort communities according to size
        print('Sorting communites')
        all_communities_sorted = OrderedDict(
            sorted(all_communities_sorted.items(), key=lambda x: len(x[1]), reverse=True))

        # get top 10 of users according to weight
        list_of_nodes_with_weights = dict(
            [(node, (data['weight'], data['label'])) for (node, data) in self.graph.nodes(data=True)])

        all_communities_sorted_with_weight = OrderedDict()
        for comm, users_of_communities in all_communities_sorted.items():
            temp_list = []
            for user in users_of_communities:
                temp_list.append((user, list_of_nodes_with_weights[user]))
            temp_list.sort(key=operator.itemgetter(1), reverse=True)
            all_communities_sorted_with_weight[comm] = temp_list

        total_info_dict = OrderedDict()
        for comm, users_of_communities_with_weight in all_communities_sorted_with_weight.items():
            temp_list = [(a[0], a[1][1], a[1][0]) for a in users_of_communities_with_weight]
            temp_list = temp_list[0:10]
            total_info_dict[comm] = temp_list

        # create separate dataframes for each community and calculate top results for hashtags, links and media
        if self.dataframe is not None:
            for comm, community_members in total_info_dict.items():
                list_of_ids = []
                for member in community_members:
                    list_of_ids.append(member[0])
                comm_dataframe = self.dataframe[self.dataframe.u_id.isin(list_of_ids)]
                top_10_hashtags = get_top_n_hashtags(10, comm_dataframe, give_freq=True)
                top_10_media = get_top_n_media(10, comm_dataframe, give_freq=True)
                top_10_urls = get_top_n_urls(10, comm_dataframe, give_freq=True)
                top_10_locations = get_top_n_locations(10, comm_dataframe, give_freq=True)
                total_info_dict[comm] = {'top_users': total_info_dict[comm], 'top_10_hashtags': top_10_hashtags,
                                         'top_10_media': top_10_media, 'top_10_urls': top_10_urls,
                                         'state_fips': top_10_locations}

        # create string containing file-information
        print('Creating Info-File')
        outstring = 'Information on Dataset:' + '\n\n'

        outstring += '   Name: ' + self.name_of_graph + '\n'
        outstring += '   Number of nodes: ' + str(self.graph.number_of_nodes())+ '\n'
        outstring += '   Number of edges: ' + str(self.graph.number_of_edges())+ '\n'
        if self.graph.number_of_nodes() > 0:
            outstring += '   Average degree: ' + str(float(sum(self.graph.degree().values())) / float(self.graph.number_of_nodes()))+ '\n'
            avg_sum = 0
            for _, data in self.graph.nodes(data=True):
                avg_sum += data['weight']

            outstring += '   Average weight: ' + str(float(avg_sum) / float(self.graph.number_of_nodes()))+ '\n\n'

        if self.dataframe is not None:
            # TODO: So far: Nur of times tweeted - To add: Nr of times retweeted
            analyze_info = analyze_dataframe(self.dataframe, True)
            outstring += '   Top 10 users:' + '\n'
            for (user, name), weight in analyze_info['users']:
                outstring += '      ' + str(name) + '(' + str(user) + ') - Count: ' + str(weight) + '\n'
            outstring += '\n'
            outstring += '   Top 10 hashtags \n'
            for hashtag, weight in analyze_info['hashtags']:
                outstring += '      ' + str(hashtag) + ' - Count: ' + str(weight) + '\n'
            outstring += '\n'

            outstring += '   Top 10 Urls \n'
            for url, weight in analyze_info['urls']:
                outstring += '      ' + str(url) + ' - Count: ' + str(weight) + '\n'
            outstring += '\n'

            outstring += '   Top 10 media (Percentage of total who have media: ' + str(
                analyze_info['media_perc']) + ')\n'
            for media, weight in analyze_info['media']:
                outstring += '      ' + str(media) + ' - Count: ' + str(weight) + '\n'
            outstring += '\n'

            outstring += '   Top 10 locations FIPS (Percentage of total: ' + str(analyze_info['stats_perc']) + ')\n'
            for (_, fips), weight in analyze_info['state_fips']:
                outstring += '      ' + str(fips) + ' - Count: ' + str(weight) + '\n'
            outstring += '\n'

            outstring += '   Percentage of retweets: ' + str(analyze_info['rt_perc']) + '\n'
            outstring += '\n'
            outstring += '   Percentage of quotes: ' + str(analyze_info['qt_perc']) + '\n'
            outstring += '\n'
            outstring += '   Percentage of answers: ' + str(analyze_info['reply_perc']) + '\n'
            outstring += '\n'
            outstring += '   Percentage of demographic statistics: ' + str(analyze_info['stats_perc']) + '\n'
            outstring += '\n'
            outstring += '   Percentage of geographic information: ' + str(analyze_info['geo_perc']) + '\n'
            outstring += '\n\n'
            outstring += 'Communities (Ordered after size): \n'
            outstring += 'Number of communities: ' + str(len(communities)) + '\n'

        for comm, info_dict in total_info_dict.items():

            outstring += '\n'
            outstring += 'Community ' + str(comm) + ':' + '\n'

            if 'top_users' in info_dict:
                if info_dict['top_users']:
                    outstring += '   Top 10 users:' + '\n'
                    for (screen_id, label, weight) in info_dict['top_users']:
                        outstring += '      ' + label + '(' + str(screen_id) + ')' + ' - Count: ' + str(weight) + '\n'
                    outstring += '\n'
            if 'top_10_hashtags' in info_dict:
                if info_dict['top_10_hashtags']:
                    outstring += '   Top 10 hashtags' + '\n'
                    for hashtag, weight in info_dict['top_10_hashtags']:
                        outstring += '      ' + str(hashtag) + ' - Count: ' + str(weight) + '\n'
                    outstring += '\n'
            if 'top_10_media' in info_dict:
                if info_dict['top_10_media']:
                    outstring += '   Top 10 media' + '\n'
                    for media, weight in info_dict['top_10_media']:
                        outstring += '      ' + str(media) + ' - Count: ' + str(weight) + '\n'
                    outstring += '\n'
            if 'top_10_urls' in info_dict:
                if info_dict['top_10_urls']:
                    outstring += '   Top 10 Urls' + '\n'
                    for url, weight in info_dict['top_10_urls']:
                        outstring += '      ' + str(url) + ' - Count: ' + str(weight) + '\n'
                    outstring += '\n'

            if 'state_fips' in info_dict:
                if info_dict['state_fips']:
                    outstring += '   Top 10 States' + '\n'
                    for (fips,name), weight in info_dict['state_fips']:
                        outstring += '      ' + str(name) + ' - Count: ' + str(weight) + '\n'
                    outstring += '\n'

        with open(path_to_file, 'w') as file_out:
            file_out.writelines(outstring)

    def create_graphs_from_dataframe(self, on_key, path_to_csv):
        """
        Method to quickly generate graphs on QT, RT or hashtags. If the method write_out_community_user_info should be 
        applied, the graph needs to be generated with this method or else there will be no underlying dataframe 
        to gather information from.

        
        :param str on_key: On which key should the graph be generated. Possible are retweeted('RT'), quoted('QT') or hashtags('hashtags')
        
        :param str path_to_csv: Path to Csv-File containing twitter-information
        
        """
        assert on_key == 'RT' or on_key == 'QT' or on_key == 'hashtag', print('Graph not known')

        print('Loading file')
        dataframe = pd.read_csv(path_to_csv, low_memory=False)

        if on_key == 'RT':
            print('Creating Retweet Graph')
            dataframe = dataframe[dataframe.RT == 1]
            self.dataframe = dataframe
            for row in dataframe.itertuples():
                self.add_node(row.r_uid, row.r_screen_name)
                self.add_edge(row.r_uid, row.r_screen_name, row.u_id, row.screen_name)
            self.add_stats(degree=True, betweenness=False, closeness=False)
            self.print_info()

        elif on_key == 'QT':
            print('Creating Quoting Graph')
            dataframe = dataframe[dataframe.QT == 1]
            self.dataframe = dataframe
            for row in dataframe.itertuples():
                self.add_node(row.q_uid, row.q_screen_name)
                self.add_edge(row.q_uid, row.q_screen_name, row.u_id, row.screen_name)
            self.add_stats(degree=True, betweenness=False, closeness=False)
            self.print_info()


        elif on_key == 'hashtag':
            print('Creating Common-Hashtag Graph')

            dataframe = dataframe[dataframe.hashtags != '[]']
            self.dataframe = dataframe

            hashtags_nr = dict()
            iter = 1

            for row in dataframe.itertuples():
                hashtags = eval(row.hashtags)
                if len(hashtags) > 1:
                    for hashtag in hashtags:
                        if str(hashtag) not in hashtags_nr:
                            hashtags_nr[str(hashtag)] = iter
                            nr = iter
                            iter += 1
                        else:
                            nr = hashtags_nr[str(hashtag)]
                        self.add_node(nr, str(hashtag))
                    combos = itertools.combinations(hashtags, 2)
                    for combo in combos:
                        nr_1 = hashtags_nr[combo[0]]
                        nr_2 = hashtags_nr[combo[1]]
                        self.add_edge(nr_1, str(combo[0]), nr_2, str(combo[1]))
            self.add_stats(degree=True, betweenness=False, closeness=False)
            self.print_info()


    def draw_graph(self,
                   output_path,
                   max_size_of_nodes=100,
                   min_size_of_nodes=5,
                   dpi=1000,
                   layout_algorithm='graphviz',
                   display_communities=True,
                   layout_iterations=1000,
                   adjust_sizes=True,
                   linlog_mode=False,
                   draw_edges=True,
                   edge_line_widths=0.2,
                   include_node_labels=True,
                   label_font_size=1,
                   node_line_size=0.2):
        """
        Wrapper function to plot the graph-object represented by this class.
        
        :param str output_path: Path to destination of plot
        
        :param int max_size_of_nodes: Maximum size of a node
        
        :param int min_size_of_nodes: Minimum size of a node
        
        :param int dpi: dots per inch of the output-file
        
        :param str layout_algorithm: Which layout algorithm to use. either 'forceatlas2' or 'graphviz'
        
        :param bool display_communities: Color all members of a community in the same color
        
        :param int layout_iterations: Number of iterations that the layout-algorithm gets applied
        
        :param bool adjust_sizes: Adjust the layout to the size of the nodes == No overlapping
        
        :param bool linlog_mode: Calculate layout with log
        
        :param bool draw_edges: Draw the edges or not
        
        :param float edge_line_widths: thickness of the edges
        
        :param bool include_node_labels: draw the node labels or not
        
        :param float label_font_size: size of label font
        
        :param float node_line_size: thickness of the node borderline
        
        """

        # Make sure no other layout is chosen than the specified
        assert layout_algorithm == 'force' or layout_algorithm == 'graphviz', print("Unknown Layout algorithm")
        assert dpi <= 1000, print("No more than 1000 dpi allowed")

        print("Printing graph to " + output_path)

        # Apply edge_line_widths to all edges
        size_of_nodes = [(max_size_of_nodes + min_size_of_nodes / 2)] * len(self.graph.nodes())
        label_of_nodes = dict()
        edge_line_widths = [edge_line_widths] * len(self.graph.nodes())

        # Calculate smallest and biggest node
        t = 0
        smallest_node_weight = 10
        biggest_node_weight = 10
        for node, data in self.graph.nodes(data=True):
            if data['weight'] < smallest_node_weight:
                smallest_node_weight = data['weight']
            if data['weight'] > biggest_node_weight:
                biggest_node_weight = data['weight']

        # According to actual weight-size of smallest and biggest nodes, calculate relative size in plot according to
        # specified max_size_of_nodes and min_size_of_nodes
        for node, data in self.graph.nodes(data=True):
            size_of_nodes[t] = min_size_of_nodes + (
                ((data['weight'] - smallest_node_weight) * (max_size_of_nodes - min_size_of_nodes)) / (
                    biggest_node_weight - smallest_node_weight))
            label_of_nodes[node] = data['label']
            t += 1

        # Calculate communities if not already done
        if display_communities:
            if not self.community_partitions:
                self._get_communities()
            values = [self.community_partitions.get(node) for node in self.graph.nodes()]
        else:
            values = []

        # Apply layout algorithm
        if layout_algorithm == 'force':
            layout = forceatlas2_networkx_layout(self.graph, niter=layout_iterations, adjustSizes=adjust_sizes,
                                                 linlogMode=linlog_mode,
                                                 sizes=size_of_nodes)
        elif layout_algorithm == 'graphviz':
            try:
                layout = graphviz_layout(self.graph, prog='neato', args='-Goverlap=true')
            except:
                print('Error calculating layout...try with smaller graph')


        # Write titel of plot
        graph_label = '"' + self.name_of_graph + '"' + '\n \n' + self.pruning_information.to_string()

        # Create legend to community color
        legend_dict = OrderedDict()
        for number in values:
            name = 'Community ' + str(number)
            legend_dict[name] = number

        if len(legend_dict) > 20:
            temp = list(islice(legend_dict, 20))
            temp_ordered = OrderedDict()
            for t in temp:
                temp_ordered[t] = legend_dict[t]
            legend_dict = temp_ordered

        paired = plt.get_cmap('Paired')

        if values:
            cNorm = colors.Normalize(vmin=0, vmax=max(values))
            scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=paired)

            f = plt.figure(1)
            ax = f.add_subplot(1, 1, 1)
            for label in legend_dict:
                ax.plot([0], [0], color=scalarMap.to_rgba(legend_dict[label]), label=label)

            plt.legend(loc='center left', prop={'size': 6},bbox_to_anchor=(-0.15, 0.5))

            # If graph-object not empty, draw nodes
            nx.draw_networkx_nodes(self.graph, pos=layout, node_size=size_of_nodes, node_color=values,
                                   linewidths=node_line_size, cmap=paired, ax=ax)

            t = plt.gca()
            t.collections[0].set_edgecolor("#000000")

            plt.axis("off")

            # Draw edges and labels
            if draw_edges:
                nx.draw_networkx_edges(self.graph, pos=layout, arrows=False, width=edge_line_widths)
            if include_node_labels:
                nx.draw_networkx_labels(self.graph, pos=layout, labels=label_of_nodes, font_size=label_font_size,
                                        font_weight='bold')
        # Plot and save the graph
        plt.suptitle(graph_label, size=6)
        plt.savefig(output_path, format="PNG", dpi=dpi)
        print("Writing graph to file successfull")
        plt.close()


"""
The following methods __btwn_pool, __partitions and calculate_betweenness where taken from
https://blog.dominodatalab.com/social-network-analysis-with-networkx/ (21.4.17 - 13:24)

Author: Manojit Nandi, 14.7.15
Modified: Lenz Baumann 21.4.17
"""

def _btwn_pool(G_tuple):
    """
    Wrapper for the method nx.betweenness_centrality_source.
    :param G_tuple: nodes of graph G 
    :return dict:  nodes with their betweenness centrality
    """
    return nx.betweenness_centrality_source(*G_tuple)


def _partitions(nodes, n):
    """
    Splits the nodes up into n different partitions
    :param nodes: 
    :param int n: 
    :return tuple: the partitions
    """
    nodes_iter = iter(nodes)
    while True:
        partition = tuple(itertools.islice(nodes_iter, n))
        if not partition:
            return
        yield partition


def calculate_betweenness(graph):
    """
    Calculates the betweeness of all nodes of the graph in parallel.
    ATTENTION: May take a long time
    
    :param nx.Graph graph: 
    
    :return list of int: Returns the betweenness for each node
     
    """
    p = Pool(processes=None)
    part_generator = 4 * len(p._pool)
    node_partitions = list(_partitions(graph.nodes(), int(len(graph) / part_generator)))
    num_partitions = len(node_partitions)

    bet_map = p.map(_btwn_pool,
                    zip([graph] * num_partitions,
                        [True] * num_partitions,
                        [None] * num_partitions,
                        node_partitions))

    bt_c = bet_map[0]
    for bt in bet_map[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    p.close()
    return bt_c


