import csv
import sys
from collections import defaultdict
from collections import deque

"""A script to sort the vertices in a connected directed graph in a linear order."""


def linearize_multiple_routes(stops_without_predecessors, successors_per_stop, predecessors_per_stop):
    """
    Sorts the stops in a linear order.

    Restrictions:
        - Loops are not allowed.
        - The undirected graph must be connected.

    Args:
        stops_without_predecessors (set): set of stops without predecessors.
        successors_per_stop (dict): set of successors per stop.
        predecessors_per_stop (dict): set of predecessors per stop.

    Returns:
        (dict) sort index per stop.
    """

    print "stops without predecessors: {}".format(stops_without_predecessors)

    # some consistency checks
    for key, value in successors_per_stop.iteritems():
        for s in value:
            assert key in predecessors_per_stop[s]

    for key, value in predecessors_per_stop.iteritems():
        for p in value:
            assert key in successors_per_stop[p]

    all_stops = stops_without_predecessors.union(successors_per_stop.keys()).union(predecessors_per_stop.keys())

    # assure that there are no loops
    for _stop in all_stops:
        if _stop in predecessors_per_stop.keys() and _stop in successors_per_stop.keys():
            intersection = set.intersection(predecessors_per_stop[_stop], successors_per_stop[_stop])
            assert not intersection

    # init
    sort_index_per_stop = {}
    queue = deque(stops_without_predecessors)

    # main loop
    def process_stop(stop, ind):
        all_predecessors_marked = True
        for before_stop in predecessors_per_stop.get(stop, []):
            if before_stop not in sort_index_per_stop.keys():
                all_predecessors_marked = False
                break
        if all_predecessors_marked:
            if stop not in sort_index_per_stop.keys():
                sort_index_per_stop[stop] = ind
                ind += 1
            for next_stop in successors_per_stop.get(stop, []):
                ind = process_stop(next_stop, ind)
        else:
            if queue:
                return process_stop(queue.popleft(), ind)
        return ind

    # start process
    process_stop(queue.popleft(), 1)
    for x in sorted([(nr, _stop) for _stop, nr in sort_index_per_stop.iteritems()]):
        print "{}, predecessor: {}, successor: {}".format(x, list(predecessors_per_stop.get(x[1], [])),
                                                          list(successors_per_stop.get(x[1], [])))
    assert len(sort_index_per_stop) == len(all_stops)
    return sort_index_per_stop


def get_data_from_file(path_in):
    """Extracts the data from a file, which can be produce for example by the timeprofileitem list in Visum."""
    list_per_id = defaultdict(list)
    with open(path_in) as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            # Columns:
            # "Id": id of the route.
            # "Richtung": direction of the route (used to decide in which order stops should be interpreted.
            # "Name": name of the stop
            list_per_id[row["Id"], row["Richtung"]] += [row["Name"]]
    for route_id, direction in list_per_id.keys():
        if direction == "R":
            list_per_id[(route_id, direction)] = list(reversed(list_per_id[(route_id, direction)]))
    all_stops = set()
    for a_list in list_per_id.values():
        all_stops = all_stops.union(set(a_list))
    print "nb stops: {}".format(len(all_stops))
    predecessors_list = defaultdict(list)
    successors_list = defaultdict(list)
    for a_list in list_per_id.values():
        for i in range(len(a_list)):
            before = a_list[i - 1] if i > 0 else None
            now = a_list[i]
            after = a_list[i + 1] if i < len(a_list) - 1 else None
            if before:
                predecessors_list[now] += [before]
            if after:
                successors_list[now] += [after]
    predecessors_per_stop = defaultdict(set, {k: set(l) for k, l in predecessors_list.iteritems()})
    successors_per_stop = defaultdict(set, {k: set(l) for k, l in successors_list.iteritems()})
    stops_without_predecessors = all_stops.difference(predecessors_per_stop.keys())
    return stops_without_predecessors, successors_per_stop, predecessors_per_stop


if __name__ == "__main__":

    _path_in = sys.argv[1]
    _path_out = sys.argv[2]

    _sort_index_per_stop = linearize_multiple_routes(*get_data_from_file(_path_in))

    with open(_path_out, "wb") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["index_sorted", "stop"])
        for k, v in sorted(_sort_index_per_stop.iteritems(), key=lambda x: x[1]):
            writer.writerow([v, k])
