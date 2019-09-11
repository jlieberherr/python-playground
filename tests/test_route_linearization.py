import unittest

from scripts.route_linearization import linearize_stops_in_multiple_routes


class RouteAggregationTest(unittest.TestCase):

    def test_linearize_multiple_routes_trivial_graph(self):
        sort_index_per_stop = linearize_stops_in_multiple_routes({1: set()})
        self.assertEquals(sort_index_per_stop, {1: 1})

    def test_linearize_multiple_routes_almost_trivial_graph(self):
        sort_index_per_stop = linearize_stops_in_multiple_routes({1: {2}, 2: set()})
        self.assertEquals(sort_index_per_stop, {1: 1, 2: 2})

    def test_linearize_multiple_routes_non_trivial_graph(self):
        sort_index_per_stop = linearize_stops_in_multiple_routes(
            {1: {2}, 2: {3}, 3: {4, 7}, 4: set(), 5: {6}, 6: {2}, 7: set()}
        )
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[1])
        self.assertTrue(sort_index_per_stop[6] == (sort_index_per_stop[5] + 1))
        self.assertTrue(sort_index_per_stop[2] > sort_index_per_stop[6])
        self.assertTrue(sort_index_per_stop[3] == (sort_index_per_stop[2] + 1))
        self.assertTrue(sort_index_per_stop[4] > sort_index_per_stop[3])
        self.assertTrue(sort_index_per_stop[7] > sort_index_per_stop[3])

    def test_linearize_multiple_routes_non_trivial_graph_extended(self):
        sort_index_per_stop = linearize_stops_in_multiple_routes(
            {1: {2}, 2: {3}, 3: {4, 7}, 4: set(), 5: {6}, 6: {2}, 7: {9}, 8: {7}, 9: {10}, 10: set()}
        )
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
