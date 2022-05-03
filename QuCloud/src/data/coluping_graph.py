#! /usr/bin/env python3

import time
import numpy as np
import os.path
from typing import Tuple, List
import logging

log = logging.getLogger(__name__)

def change_Graph_to_List(graph):
    List=[]
    List_edge=[]
    List_node=[]
    node_list=[]
    for i,j in graph.getEdges():
        List.append([i,j])
        List_edge.append(float(graph.getEdgeWeight(i,j)))
    for i in graph.getVertices():
        List_node.append(float(graph.vertList[i].getValue()))
        node_list.append("node"+str(i))
    return List, List_edge, List_node, node_list

class Vertex:
    def __init__(self,key,value=0):
        self.id = key
        self.error_value = value
        self.connectedTo = {}
    
    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
    
    def __str__(self):
        return str(self.id) +': error_value is '+ str(self.error_value) + ' connectedTo: '+str([x.id for x in self.connectedTo])
    
    def getConnections(self):
        return [x.id for x in self.connectedTo]
    
    def getId(self):
        return self.id
    
    def getValue(self):
        return self.error_value
    
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.edgeList = {}
        self.numVertices = 0
        self.numberEdges = 0
        
    def addVertex(self,key,value):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,value)
        self.vertList[key]=newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
    
    def __contains__(self,n):
        return n in self.vertList
    
    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],cost)
        self.vertList[t].addNeighbor(self.vertList[f],cost)
        self.edgeList[(f,t)] = cost
        self.numberEdges += 1
    
    def getVertices(self):
        return self.vertList.keys()
    
    def getEdges(self):
        return self.edgeList.keys()

    def getEdgeWeight(self,f,t):
        return self.vertList[f].getWeight(self.vertList[t])

    def __iter__(self):
        return iter(self.vertList.values())



if __name__ == "main":
    Vertex_error = {"Q0" : 0.014, "Q1" : 0.035, "Q2" : 0.033, "Q3" : 0.033, "Q4" : 0.030}               #量子位数
    Edge_error = {(0,1) : 0.005, (1,2) : 0.012, (1,3) : 0.01, (3,4) : 0.013}
    graph=Graph()
    for vertex in Vertex_error:
        vertex_id = int(vertex[1])
        graph.addVertex(vertex_id,Vertex_error[vertex])
    for edge in Edge_error:
        node0,node1 = edge
        graph.addEdge(node0,node1,Edge_error[edge])
    