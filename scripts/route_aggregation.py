import csv
import sys
from collections import defaultdict

"""A script for aggregating routes with common stops."""


def aggregate_routes(route_per_id, nb_subsequent_stops=3):
    """Aggregates the routes if they have at least nb_subsequent common consecutive stops."""
    routes_per_subsequent_stop_tuples = get_routes_per_subsequent_stop_tuples(route_per_id, nb_subsequent_stops)
    route_group_per_route = {}
    for route in route_per_id:
        route_group_per_route[route] = {route}
    for routes_to_aggregate in routes_per_subsequent_stop_tuples.values():
        routes_to_aggregate_list = list(routes_to_aggregate)
        nb_routes = len(routes_to_aggregate_list)
        for ind in range(nb_routes):
            for j in range(ind, nb_routes):
                route_1 = routes_to_aggregate_list[ind]
                route_2 = routes_to_aggregate_list[j]
                route_group_1 = route_group_per_route[route_1]
                route_group_2 = route_group_per_route[route_2]
                if route_group_1 is not route_group_2:
                    new_route_group = route_group_1.union(route_group_2)
                    for a_route in new_route_group:
                        route_group_per_route[a_route] = new_route_group
    return frozenset([frozenset(s) for s in route_group_per_route.values()])


def get_routes_per_subsequent_stop_tuples(route_per_id, nb_subsequent_stops):
    res = dict()
    for route_id, route in route_per_id.items():
        for stop_sequence in get_subsequent_stop_tuples(route, nb_subsequent_stops):
            temp = res.get(stop_sequence, set())
            temp.add(route_id)
            res[stop_sequence] = temp
    return res


def get_subsequent_stop_tuples(route_stops, nb_subsequent_stops):
    res = set()
    for ind in range(len(route_stops) - nb_subsequent_stops + 1):
        res.add(route_stops[ind: ind + nb_subsequent_stops])
    return res


def get_routes_from_visum_att_file(path_to_visum_att_file):
    """Creates the routes from a Visum-TIMEPROFILEITEM-attribute-file."""
    with open(path_to_visum_att_file) as f:
        for _ in range(12):
            f.next()
        _route_per_id = defaultdict(list)
        reader = csv.DictReader(f, delimiter=";")
        for tpi in reader:
            _route_per_id[int(tpi["TIMEPROFILEID"])] += [int(tpi[r"LINEROUTEITEM\STOPPOINT\STOPAREA\STOP\NO"])]
    res = {}
    for tp_id in _route_per_id:
        res[tp_id] = tuple(_route_per_id[tp_id])
    return res


if __name__ == "__main__":
    path_to_att_file = sys.argv[1]
    route_per_id_from_visum = get_routes_from_visum_att_file(path_to_att_file)
    print "#timeprofiles: {}".format(len(route_per_id_from_visum))
    print "#timeprofileitems: {}".format(sum([len(e) for e in route_per_id_from_visum.values()]))
    aggregated_routes = aggregate_routes(route_per_id_from_visum, nb_subsequent_stops=3)
    print "#timeprofile-groups: {}".format(len(aggregated_routes))
    for i, gr in enumerate(aggregated_routes):
        for fzp in gr:
            print "{};{}".format(i, fzp)
