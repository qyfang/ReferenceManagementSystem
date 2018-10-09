# -*- coding: UTF-8 -*- 
import networkx as nx

from networkx.algorithms.community import k_clique_communities

from data.models import Reference

class ReferenceNetwork(object):
    def __init__(self):
        self.graph = nx.DiGraph()
        nx.set_node_attributes(self.graph, '', 'selfid')
        nx.set_node_attributes(self.graph, '', 'url')
        nx.set_node_attributes(self.graph, '', 'title')
        nx.set_node_attributes(self.graph, [], 'authors')
        nx.set_node_attributes(self.graph, [], 'keywords')
        nx.set_node_attributes(self.graph, '', 'abstract')
        nx.set_node_attributes(self.graph, [], 'referids')
        nx.set_node_attributes(self.graph, 0, 'weight')
        nx.set_node_attributes(self.graph, [], 'communities')

    def generateNode(self):
        references = Reference.objects.all()
        for reference in references:
            if reference.selfid == '':
                continue
            attr = {}
            attr['selfid'] = reference.selfid
            attr['url'] = reference.url
            attr['title'] = reference.title
            attr['authors'] = reference.authors.split(',')
            attr['keywords'] = reference.keywords.split(',')
            attr['abstract'] = reference.abstract
            attr['referids'] = reference.referids.split(',')
            self.graph.add_node(attr['selfid'], **attr)

    def generateEdge(self):
        nodes = self.graph.node
        for n in nodes:
            selfid = nodes[n]['selfid']
            referids = nodes[n]['referids']
            for referid in referids:
                if referid in nodes:
                    self.graph.add_edge(selfid, referid)

    def generateNetwork(self):
        self.generateNode()
        self.generateEdge()

    def executeKClique(self, k):
        udgraph = self.graph.to_undirected()
        communities = k_clique_communities(udgraph, k)
        nodes = self.graph.node
        communitynum = -1

        for n in nodes:
            nodes[n]['communities'] = []

        coms = {}
        for community in communities:
            communitynum += 1
            com = []
            for n in community:
                nodes[n]['communities'].append(communitynum)
                com.append(n)
            coms[communitynum] = com
        return coms

    def executePageRank(self):
        pr = nx.pagerank(self.graph)
        maxpr = max(pr.values())
        minpr = min(pr.values())
        nodes = self.graph.node
        
        for n in nodes:
            nodes[n]['weight'] = (pr[n] - minpr) / (maxpr - minpr)

        rank = sorted(pr.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

        return rank