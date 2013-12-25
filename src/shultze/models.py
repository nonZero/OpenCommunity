from django.db import models
from issues.models import Issue
from communities.models import Community
from pyvotecore.condorcet import CondorcetHelper
from pyvotecore.schulze_by_graph import SchulzeNPRByGraph
from pyvotecore.schulze_method import SchulzeMethod #TODO: remove this when iteritems bug is solved
import itertools

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


#TODO: Reconsider abstract graph structure models.

#class Graph(models.Model):
#    """
#    Abstract graph class
#    Graph level general functionality should go here
#    """
#    class Meta:
#        abstract = True
#
#    def get_nodes_query(self):
#        return Node.objects.filter(graph=self)
#
#
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
#
#
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


class IssuesGraph(models.Model):
    """
    Graph-Issues class
    Graph level general functionality should go here, one-to-one relation with OpenCommunity Community
    """
    community = models.ForeignKey(Community, related_name="shultze_issues_graph")
    
    def initialize_graph(self):
        """
        Initialize candidates graph by community issues table.
        This should happen only once!
        """
        candidates = list(self.community.issues.all())
        candidate_nodes = []
        for candidate in candidates:
            candidate_nodes.append(IssueNode.objects.create(graph=self, issue=candidate))
        for pair in itertools.permutations(candidate_nodes, 2):
            IssueEdge.objects.create(graph=self, from_node=pair[0], to_node=pair[1], weight = 0)
    
    def add_ballots(self, ballots, tie_breaker=None, ballot_notation=None, reverse=False):
        """
        Add ballots of ordered issues.
        Ballots are translated to their complementary graph using PyVoteCoreAssistance and the graph's 
        edges values are added/deducted from the IssuesGraph instance.
        
        Example:
          input = [{'ballot': [[1], [2], [3], [4], [5]], 'count': 3},
           {'ballot': [[5], [2], [3], [4], [1]], 'count': 9},
           {'ballot': [[5], [1], [3], [4], [1]], 'count': 8},
           {'ballot': [[3], [2], [4], [1], [5]], 'count': 5},
           {'ballot': [[1], [2], [3], [4], [5]], 'count': 5}]
        
          g.add_ballots(input)
        
        use reverse=True to deduct the ballot from the IssuesGraph, reversing it's effect.
        """
        output = SchulzeMethod(ballots, ballot_notation="grouping").as_dict() #TODO: remove this line when iteritems bug is solved
        assistance = PyVoteCoreAssistance()
        assistance.add_ballot(ballots, tie_breaker, ballot_notation)
        for edge_key in assistance.pairs.keys():
            try:
                from_node = IssueNode.objects.get(issue_id = edge_key[0])
            except IssueNode.DoesNotExist:
                try:
                    new_issue = Issue.objects.get(id = edge_key[0])
                    from_node = self.add_node(new_issue)
                except Issue.DoesNotExist:
                    raise  # TODO: decide on proper exception
            try:
                to_node = IssueNode.objects.get(issue_id = edge_key[1])
            except IssueNode.DoesNotExist:
                try:
                    new_issue = Issue.objects.get(id = edge_key[1])
                    to_node = self.add_node(new_issue)
                except Issue.DoesNotExist:
                    raise  # TODO: decide on proper exception
            edge = IssueEdge.objects.get(graph=self, from_node=from_node, to_node=to_node)
            if reverse:
                edge.weight -= assistance.pairs[edge_key]
            else:
                edge.weight += assistance.pairs[edge_key]
            edge.save()

    def add_node(self, candidate):
        node = IssueNode.objects.create(graph=self, issue=candidate)
        for other_node in IssueNode.objects.filter(graph=self).exclude(issue=candidate):
            IssueEdge.objects.create(graph=self, from_node=node, to_node=other_node, weight = 0)
            IssueEdge.objects.create(graph=self, from_node=other_node, to_node=node, weight = 0)
        return node
    
    def get_edges_dict(self):
        """
        Return the graph's edges in the form of an edges dictionary.
        example:
          {
              ('a', 'b'): 8,
              ('b', 'a'): 3,
              ('a', 'c'): 3,
              ('c', 'a'): 4,
              ('b', 'c'): 6,
              ('c', 'b'): 3,
          }
        """
        edges_dict = dict()
        for edge in IssueEdge.objects.filter(graph=self):
            edges_dict[(edge.from_node.id, edge.to_node.id)] = edge.weight
        return edges_dict
    
    def get_schulze_npr_results(self):
        input = self.get_edges_dict()
        output = SchulzeNPRByGraph(input).as_dict()
        return output

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


def process_vote_stub(community_id, current_order, prev_order=[]):
    """
    Vote processing function
      Find the appropriate IssuesGraph for community_id
    """
    try:
        community_instance = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        raise
    try:
        graph = IssuesGraph.objects.get(community=community_instance)
    except IssuesGraph.DoesNotExist:
        raise  # initialize a new graph here?
    except IssuesGraph.MultipleObjectsReturned:
        raise  # there should be only one! TODO: decide on proper exception
    if prev_order:
        graph.add_ballots(prev_order,reverse=True)
    graph.add_ballots(current_order)
    return