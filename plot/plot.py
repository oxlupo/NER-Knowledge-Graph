import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import json
import re
from bs4 import BeautifulSoup, NavigableString, Tag, Doctype
import requests
import lxml.html as lh
from collections import defaultdict
import itertools

data = open('check.json', 'r')
check_json = json.load(data)

def visualize_graph(pairs, accuracy, c1='red', c2='blue', c3='orange'):
    k_graph = nx.from_pandas_edgelist(pairs, 'source', 'target',
                                      create_using=nx.MultiDiGraph())
    ner_list = check_json.keys()
    node_deg = nx.degree(k_graph)
    layout = nx.spring_layout(k_graph, k=0.15, iterations=20)
    plt.figure(num=None, figsize=(50, 40), dpi=80, facecolor='grey')
    val_map = {}
    for ner in pairs['target'].values:
        if ner in ner_list:
            val_map.update({f"{ner}": "green"})
        else:
            val_map.update({f"{ner}": "black"})
    values = [val_map.get(node, "green") for node in k_graph.nodes()]

    nx.draw_networkx(
        k_graph,
        node_size=[int(deg[1]) * 1000 for deg in node_deg],
        arrowsize=20,
        linewidths=1.5,
        pos=layout,
        edge_color=c1,
        edgecolors=c2,
        node_color=values,
        font_color='white'
    )
    labels = dict(zip(list(zip(pairs.source, pairs.target)),
                      pairs['edge'].tolist()))
    nx.draw_networkx_edge_labels(k_graph, pos=layout, edge_labels=labels,
                                 font_color='red')
    plt.title(f"accuracy between green node: {accuracy}", fontdict={'fontsize': 40})

    plt.axis('off')
    plt.show()

#######################################################################
html = open("html/amoot.html").read()
soup = BeautifulSoup(html, 'lxml')

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def traverse_html(soup, graph: nx.Graph, counter, parent=None) -> None:

    for content in soup.contents:
        # if content.name is not None:
            try:
                # name_count = counter.get(content.name)
                # if parent is not None:
                graph.add_node(str(content))
                    # elem = soup.find(string=re.compile(soup.text))
                tex = soup.text.strip()
                elem = soup.find(text=re.compile(tex))
                if elem is not None:
                    print(elem)
                    print(xpath_soup(elem))
                    graph.add_edge(parent, str(xpath_soup(elem)))
                    # graph.add_edge(parent, content.name if not name_count else f'{content.name}_{name_count}')
                counter[content.name] += 1
                traverse_html(content, graph, counter, content.name)
            except AttributeError:
                pass


def traverse_html_1(soup, graph: nx.Graph, counter, parent=None) -> None:

    for content in soup.contents:
            try:
                if isinstance(content, Tag):
                    childs = content.findChildren(recursive=False)
                    graph_name = xpath_soup(content)
                    if graph_name in graph:
                        pass
                    else:
                        graph.add_node(graph_name)
                    graph.add_edge(parent, graph_name)
                    # nx.draw(graph, with_labels=True)
                elif isinstance(content, Doctype):
                    continue
                else:
                    if isinstance(content, NavigableString):
                        continue
                    else:
                        childs = content.findChildren(recursive=False)
                if not childs == []:
                        for ch in childs:
                            if isinstance(ch, Tag):
                                graph.add_node(xpath_soup(ch), xpath=xpath_soup(ch))
                                graph.add_edge(xpath_soup(content), xpath_soup(ch))
                                # child = ch.findChildren(recursive=False)
                                # nx.draw(graph, with_labels=True)
                                # if not child == []:
                                traverse_html_1(ch, graph, counter, xpath_soup(ch))
                            elif isinstance(ch, NavigableString):
                                continue
                        tex = soup.text.strip()
                        elem = soup.find(text=re.compile(tex))
                        if elem is not None:
                            print(elem)
                            print(xpath_soup(elem))
                        #     graph.add_edge(parent, str(xpath_soup(elem)))
            except Exception:
                print(Exception)


full_graph = nx.DiGraph()
traverse_html_1(soup, full_graph, defaultdict(int), 'root')
# nx.draw(full_graph, with_labels=True)
cluster = nx.clustering(full_graph)
is_attracting_component = nx.is_attracting_component(full_graph)
number_attracting_components = nx.number_attracting_components(full_graph)
attracting_components = nx.attracting_components(full_graph)
# subgraph = []
# for k in attracting_components:
#     k = list(k)
#     subgraph.append(k[0])
# nodes = full_graph.nodes()
# removed_node = []
# for node in nodes:
#     if not node in subgraph:
#         removed_node.append(node)
#         # full_graph.remove_node(node)
# full_graph.remove_nodes_from(removed_node)
nx.draw(full_graph, with_labels=True)
# print(removed_node)
# print(nodes)
# attracting_components = nx.attracting_components(full_graph)
# subgraph = []
# for graph in attracting_components:
#     subgraph.append(str(graph))
degree = full_graph.degree()
print(degree)

# print(degree['/html/body/div/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span'])
# all_deg = []
# for deg in degree:
#     deg_splited = deg[0].split("_")
#     all_deg.append(deg_splited[0])
# data = (dict((l, all_deg.count(l)) for l in all_deg))
# sorted_list = dict(sorted(data.items(), key=lambda item: item[1]))
de = list(filter(lambda x: x[1] if x[1] > 1 else False, degree))
# with_out_children = [k for k, v in full_graph.out_degree().iteritems() if v == 0]
# print(de)
# print(degree)
# print(cluster)
plt.show()
def getMCS(self, G_source, G_new):

    matching_graph = nx.Graph()
    for n1, n2, attr in G_new.edges(data=True):
        if G_source.has_edge(n1, n2):
            matching_graph.add_edge(n1, n2, weight=1)

    graphs = list(nx.connected_component_subgraphs(matching_graph))

    mcs_length = 0
    mcs_graph = nx.Graph()
    for i, graph in enumerate(graphs):

        if len(graph.nodes()) > mcs_length:
            mcs_length = len(graph.nodes())
            mcs_graph = graph
    return mcs_graph

# G = nx.complete_graph(25)
# graph = nx.Graph()
# print(nx.clustering(G, 0))
# i = nx.clustering(G)
# node_deg = nx.degree(G)
# layout = nx.spring_layout(G, k=0.15, iterations=20)
#
# nx.draw_networkx(
#     G,
#     node_size=[45],
#     arrowsize=20,
#     linewidths=1.5,
#     pos=layout,
#     edge_color="green",
#     edgecolors="blue",
#     node_color="blue",
#     font_color='white'
# )
# plt.show()

# elem_tree = lh.parse("test.html")
# input_string = ["ASUS Dual NVIDIA GeForce RTX 3050 OC Edition Gaming Graphics Card - PCIe 4.0, 8GB GDDR6 Memory, HDMI 2.1, DisplayPort 1.4a, 2-Slot Design, Axial-tech Fan Design, 0dB Technology, Steel Bracket"]
#
# for i in input_string:
#     xpath = "//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div[2]/div/div/div[1]/h2"
#     node = elem_tree.xpath(xpath.format(i))[0]
#
#     print('{0} -> {1}'.format(i, elem_tree.getpath(node)))
#
# page = requests.get('https://www.nike.com/de/w/damen-5e1x6')
# tree = html.fromstring(page.content)
# t = elem_tree.xpath('//div[@class="sg-row"]/text()')
# buyers = tree.xpath('//a[@class="product-card__link-overlay"]/text()')
# print(buyers)
