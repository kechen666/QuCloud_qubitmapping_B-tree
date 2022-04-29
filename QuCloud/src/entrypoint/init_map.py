from QuCloud.src.data.qcdata import QCData
from QuCloud.src.data.coluping_graph import Graph

import json
import logging
import time
import os
from typing import Dict, List, Optional, Any

__all__ = ["init_mapping"]

log = logging.getLogger(__name__)

def init_mapping(path_file : str,
                output : str,
                loglevel : int, 
                log_path : str):
    if path_file:
        qcdata = QCData(path_file, )
    else:
        qcdata = QCData()
    Vertex_error = qcdata.Vertex_error
    Edge_error = qcdata.Edge_error
    graph = get_graph(Vertex_error, Edge_error)
    List, List_edge, List_node, node_list = change_Graph_to_List(graph)
    print("List",List)
    print("List_edge",List_edge)
    print("List_node",List_node)
    print("node_list",node_list)


def get_graph(Vertex_error, Edge_error):
    graph=Graph()
    for vertex in Vertex_error:
        vertex_id = int(vertex[1])
        graph.addVertex(vertex_id,Vertex_error[vertex])
    for edge in Edge_error:
        node0,node1 = edge
        graph.addEdge(node0,node1,Edge_error[edge])
    return graph

def change_Graph_to_List(graph):
    List=[]
    List_edge=[]
    List_node=[]
    node_list=[]
    for i,j in graph.getEdges():
        List.append([i,j])
        List_edge.append(graph.getEdgeWeight(i,j))
    for i in graph.getVertices():
        List_node.append(graph.vertList[i].getValue())
        node_list.append("node"+str(i))
    return List, List_edge, List_node, node_list

if __name__ == "__main__":
    init_mapping()
