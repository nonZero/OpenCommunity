from django.db import models
from issues.models import Issue
from communities.models import Community
from pyvotecore.condorcet import CondorcetHelper


# Not a django model!
class PyVoteCoreAssistance(CondorcetHelper):
    """
    Mainly CondorcetHelper
    """
    def add_ballot(self, ballots, tie_breaker=None, ballot_notation=None):
        for ballot in ballots:
            if "count" not in ballot:
                ballot["count"] = 1
        self.standardize_ballots(ballots, ballot_notation)
        self.graph = self.ballots_into_graph(self.candidates, self.ballots)
        self.pairs = self.edge_weights(self.graph)


class Graph(models.Model):
    """
    Abstract graph class
    Graph level general functionality should go here
    """
    class Meta:
        abstract = True

    def get_nodes_query(self):
        return Node.objects.filter(graph=self)

#TODO: Reconsider abstract graph structure models.

#class Node(models.Model):
#    """
#    Abstract graph node class
#    Node level functionality
#    related queries:
#        node.in_edges
#        node.out_edges
#    """
#    graph = models.ForeignKey(Graph, verbose_name=_("Graph"), related_name="nodes")
#    
#    class Meta:
#        abstract = True


#class Edge(models.Model):
#    """
#    Abstract graph directed edge class
#    Simple directed edge with numeric weight
#    """
#    graph = models.ForeignKey(Graph, verbose_name=_("Graph"), related_name="edges")
#    from_node = models.ForeignKey(Node, verbose_name=_("From node"), related_name="out_edges")
#    to_node = models.ForeignKey(Node, verbose_name=_("To node"), related_name="in_edges")
#    weight = models.IntegerField(_("Weight"), default=0)
#    
#    class Meta:
#        abstract = True


class IssuesGraph(Graph):
    """
    Graph-Issues class
    Graph level general functionality should go here, one-to-one relation with OpenCommunity Community
    """
    community = models.ForeignKey(Community, related_name="shultze_issues_graph")

    def add_ballot(self, ballots, tie_breaker=None, ballot_notation=None):
        assistance = PyVoteCoreAssistance()
        assistance.add_ballot(ballots, tie_breaker, ballot_notation)
        for edge in assistance.pairs.keys():
            from_node = IssueNode.objects.get(issue = edge[0]) #by name or by pk?
            to_node = IssueNode.objects.get(issue = edge[1]) #by name or by pk?
            edge = Edge.objects.get(from_node=from_node, to_node=to_node)
            edge.weight += assistance.pairs[edge]

    def initialize_graph(self):
        """
        Initialize candidates graph by community issues table.
        This should happen only once!
        """
        candidates = list(self.community.issues.all())
        for candidate in candidates:
            IssueNode.objecs.create(issue = candidate)
        for pair in itertools.permutations(candidates, 2):
            Edge.objects.create(from_node=pair[0], to_node=pair[1], weight = 0)


class IssueNode(models.Model):
    """
    Issue-node class
    Node level functionality, one-to-one relation with OpenCommunity Issue
    related queries:
        node.in_edges
        node.out_edges
    """
    graph = models.ForeignKey(IssuesGraph, related_name="nodes")
    issue = models.ForeignKey(Issue, related_name="shultze_graph_node")


class IssueEdge(models.Model):
    """
    Abstract graph directed edge class
    Simple directed edge with numeric weight
    """
    graph = models.ForeignKey(IssuesGraph, related_name="edges")
    from_node = models.ForeignKey(IssueNode, related_name="out_edges")
    to_node = models.ForeignKey(IssueNode, related_name="in_edges")
    weight = models.IntegerField(default=0)