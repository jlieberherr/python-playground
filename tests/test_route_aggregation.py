import unittest

from scripts.route_aggregation import aggregate_routes, get_routes_per_subsequent_stop_tuples, \
    get_subsequent_stop_tuples

ROUTE_PER_ID = {
    1: (1, 2, 3),
    2: (1, 2, 3, 7),
    3: (1, 2, 3, 4, 5, 6),
    4: (16, 1, 2, 3, 4),
    5: (4, 5, 6, 8),
    6: (9, 10, 11, 12),
    7: (10, 11, 12),
    8: (13, 14, 15),
}


class RouteAggregationTests(unittest.TestCase):
    def test_aggregate_routes_3(self):
        aggregated_routes = aggregate_routes(ROUTE_PER_ID)
        print aggregated_routes
        self.assertEquals(3, len(aggregated_routes))
        self.assertTrue({1, 2, 3, 4, 5} in aggregated_routes)
        self.assertTrue({6, 7} in aggregated_routes)
        self.assertTrue({8} in aggregated_routes)

    def test_aggregate_routes_4(self):
        aggregated_routes = aggregate_routes(ROUTE_PER_ID, nb_subsequent_stops=4)
        print aggregated_routes
        self.assertTrue({1} in aggregated_routes)
        self.assertTrue({2} in aggregated_routes)
        self.assertTrue({3, 4} in aggregated_routes)
        self.assertTrue({5} in aggregated_routes)
        self.assertTrue({6} in aggregated_routes)
        self.assertTrue({7} in aggregated_routes)
        self.assertTrue({8} in aggregated_routes)

    def test_aggregate_routes_5(self):
        aggregated_routes = aggregate_routes(ROUTE_PER_ID, nb_subsequent_stops=5)
        print aggregated_routes
        self.assertTrue({1} in aggregated_routes)
        self.assertTrue({2} in aggregated_routes)
        self.assertTrue({3} in aggregated_routes)
        self.assertTrue({4} in aggregated_routes)
        self.assertTrue({5} in aggregated_routes)
        self.assertTrue({6} in aggregated_routes)
        self.assertTrue({7} in aggregated_routes)
        self.assertTrue({8} in aggregated_routes)

    def test_get_routes_per_subsequent_stop_tuples(self):
        routes_per_subsequent_stop_tuples = get_routes_per_subsequent_stop_tuples(ROUTE_PER_ID, 3)
        self.assertEquals({1, 2, 3, 4}, routes_per_subsequent_stop_tuples[(1, 2, 3)])
        self.assertEquals({3, 4}, routes_per_subsequent_stop_tuples[(2, 3, 4)])
        self.assertEquals({2}, routes_per_subsequent_stop_tuples[(2, 3, 7)])
        self.assertEquals({5}, routes_per_subsequent_stop_tuples[(5, 6, 8)])
        self.assertTrue((1, 2, 4) not in routes_per_subsequent_stop_tuples)

    def test_get_subsequent_stop_tuples(self):
        subsequent_stop_tuples = get_subsequent_stop_tuples((1, 2, 3, 4, 5, 6), 3)
        self.assertEquals({(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)}, subsequent_stop_tuples)

    def test_get_subsequent_stop_tuples_short(self):
        subsequent_stop_tuples = get_subsequent_stop_tuples((1, 2), 3)
        self.assertEquals(set(), subsequent_stop_tuples)


if __name__ == '__main__':
    unittest.main()
