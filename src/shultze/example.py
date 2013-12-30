from shultze.models import *
g = IssuesGraph.objects.all()[0]
for e in g.edges.all():
    print e.from_node_id, e.to_node_id, e.weight

input = [{'ballot': [[1], [2], [3], [4], [5]], 'count': 3},
 {'ballot': [[5], [2], [3], [4], [1]], 'count': 9},
 {'ballot': [[5], [1], [3], [4], [1]], 'count': 8},
 {'ballot': [[3], [2], [4], [1], [5]], 'count': 5},
 {'ballot': [[1], [2], [3], [4], [5]], 'count': 5}]
 
g.add_ballots(input)
