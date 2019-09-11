import unittest

from scripts.route_linearization import linearize_multiple_routes


class RouteAggregationTest(unittest.TestCase):

    def test_linearize_multiple_routes_trivial_graph(self):
        sort_index_per_stop = linearize_multiple_routes({1}, {}, {})
        self.assertEquals(sort_index_per_stop, {1: 1})

    def test_linearize_multiple_routes_almost_trivial_graph(self):
        sort_index_per_stop = linearize_multiple_routes({1}, {1: {2}}, {2: {1}})
        self.assertEquals(sort_index_per_stop, {1: 1, 2: 2})

    def test_linearize_multiple_routes_non_trivial_graph(self):
        sort_index_per_stop = linearize_multiple_routes(
            {1, 5},
            {1: {2}, 2: {3}, 3: {4, 7}, 5: {6}, 6: {2}},
            {2: {1, 6}, 3: {2}, 4: {3}, 6: {5}, 7: {3}})
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[1])
        self.assertTrue(sort_index_per_stop[6] == (sort_index_per_stop[5] + 1))
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[6])
        self.assertTrue(sort_index_per_stop[3] == (sort_index_per_stop[2] + 1))
        self.assertTrue(sort_index_per_stop[4] > sort_index_per_stop[3])
        self.assertTrue(sort_index_per_stop[7] > sort_index_per_stop[3])

    def test_linearize_multiple_routes_non_trivial_graph_extended(self):
        sort_index_per_stop = linearize_multiple_routes(
            {1, 5, 8},
            {1: {2}, 2: {3}, 3: {4, 7}, 5: {6}, 6: {2}, 7: {9}, 8: {7}, 9: {10}},
            {2: {1, 6}, 3: {2}, 4: {3}, 6: {5}, 7: {3, 8}, 9: {7}, 10: {9}})
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[1])
        self.assertTrue(sort_index_per_stop[6] == (sort_index_per_stop[5] + 1))
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[6])
        self.assertTrue(sort_index_per_stop[3] == (sort_index_per_stop[2] + 1))
        self.assertTrue(sort_index_per_stop[4] > sort_index_per_stop[3])
        self.assertTrue(sort_index_per_stop[7] > sort_index_per_stop[3])
        self.assertTrue(sort_index_per_stop[7] > sort_index_per_stop[8])
        self.assertTrue(sort_index_per_stop[9] == (sort_index_per_stop[7] + 1))
        self.assertTrue(sort_index_per_stop[10] == (sort_index_per_stop[9] + 1))


if __name__ == '__main__':
    unittest.main()
