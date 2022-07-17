from bs4 import BeautifulSoup, NavigableString, Tag, Doctype
import requests
import lxml.html as lh
from collections import defaultdict
import networkx as nx
import json
import matplotlib.pyplot as plt
import re
import extruct


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
html = open('test.html').read()
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
degree = full_graph.degree()
print(degree)