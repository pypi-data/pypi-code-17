from unittest import TestCase
from ...examples import example_graph_1
from ...paths_functions import *
from nose.tools import eq_
import pandas as pd
import networkx

class TestPath(TestCase):
    '''
    test class for paths_function.py
    '''
    # run functions in class and then test outputs
    nodes, edges = example_graph_1()
    nodes_df, edges_df = get_node_edge_data(nodes, edges)
    nodes_list, edges_tuple = get_node_edge_lists(nodes_df, edges_df)
    graph, nodes_df = get_graph(nodes_df, edges_df)
    paths_list = get_node_simple_paths(graph, nodes_list, 1, 4)
    weight_dict = get_node_weights(graph, nodes_list)

    def test_get_simple_paths_result(self):
        '''
        test get_simple_paths_result
        '''
        results = get_simple_paths_result(self.nodes, self.edges, 4)
        eq_(round(results.node_score[0], 2), .96)

    def test_get_node_edge_data_nodes(self):
        '''
        test get_node_edge_data, nodes output
        '''
        eq_(self.nodes_df.columns[0], 'node')

    def test_get_node_edge_data_edges(self):
        '''
        test get_node_edge_data, edges output
        '''
        eq_(self.edges_df.columns[0], 'node_a')

    def test_get_node_edge_lists_nodes(self):
        '''
        test get_node_edge_lists, nodes output
        '''
        self.assertItemsEqual(self.nodes_list, [1, 2, 3, 4])

    def test_get_node_edge_lists_edges(self):
        '''
        test get_node_edge_lists, edges output
        '''
        eq_(self.edges_tuple[0], (1, 2))

    def test_get_graph_graph(self):
        '''
        test get_graph, graph output
        '''
        self.assertIsInstance(self.graph, networkx.digraph.DiGraph)

    def test_get_node_simple_paths(self):
        '''
        test simple paths output of node 1
        '''
        test_paths_list = [[1, 2], [1, 3, 2], [1, 2, 4, 3], [1, 3], [1, 2, 4], [1, 3, 2, 4]]
        self.assertItemsEqual(self.paths_list, test_paths_list)

    def test_get_node_weights(self):
        '''
        test node 1 weight
        '''
        eq_(self.weight_dict[1], 1/float(3))

    def test_get_node_score(self):
        '''
        test value of node 1
        '''
        value = get_node_score(self.paths_list, self.weight_dict)
        eq_(value, .96)

    def test_get_graph_score(self):
        '''
        test score of node 1
        '''
        node_scores = get_graph_score(self.graph, 4)
        eq_(node_scores.node_score[0], .96)
    